from PyQt6 import QtWidgets, QtCore, QtGui

class ImageDisplay(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; background: #f0f0f0;")
        
        # Инициализация всех переменных (ОБЯЗАТЕЛЬНО)
        self._original_pixmap = None
        self._current_ratio = None
        self._zoom_factor = 1.0
        self._offset = QtCore.QPointF(0, 0)
        self._last_mouse_pos = None
        self._free_mode = False 
        self._show_overlay = True

    def set_overlay_visible(self, visible):
        self._show_overlay = visible
        self.update()

    def set_image(self, pixmap):
        self._original_pixmap = pixmap
        self._offset = QtCore.QPointF(0, 0)
        self.update()

    def set_ratio(self, ratio_text):
        ratios = {
            "Оригинал": None,
            "1:1": 1.0,
            "4:3": 4/3,
            "16:9": 16/9
        }
        self._current_ratio = ratios.get(ratio_text)
        self.update()

    def set_zoom(self, value):
        self._zoom_factor = value / 100.0
        self.update()

    def set_free_mode(self, state):
        # state приходит как 0 (Unchecked) или 2 (Checked)
        self._free_mode = bool(state)
        if not self._free_mode:
            self._offset = QtCore.QPointF(0, 0)
        self.update()

    def mousePressEvent(self, event):
        if self._free_mode and event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._last_mouse_pos = event.position()
            self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self._free_mode and self._last_mouse_pos is not None:
            delta = event.position() - self._last_mouse_pos
            self._offset += delta
            self._last_mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        self._last_mouse_pos = None
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def paintEvent(self, event):
        if not self._original_pixmap:
            super().paintEvent(event)
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        view_size = self.size()
        pix_size = self._original_pixmap.size()
        pix_size.scale(view_size - QtCore.QSize(40, 40), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        
        tw, th = pix_size.width() * self._zoom_factor, pix_size.height() * self._zoom_factor
        
        rect_center = self.rect().center()
        dest_rect = QtCore.QRectF(0, 0, tw, th)
        dest_rect.moveCenter(QtCore.QPointF(rect_center) + self._offset)

        painter.drawPixmap(dest_rect.toRect(), self._original_pixmap)

        # Рисуем рамку ТОЛЬКО если флаг True и выбрано соотношение
        if self._show_overlay and self._current_ratio:
            self._draw_fixed_crop_overlay(painter)
        
        painter.end()

    def _draw_fixed_crop_overlay(self, painter):
        view_rect = self.rect().adjusted(20, 20, -20, -20)
        vw, vh = view_rect.width(), view_rect.height()
        
        if vw / vh > self._current_ratio:
            cw, ch = vh * self._current_ratio, vh
        else:
            cw, ch = vw, vw / self._current_ratio
            
        crop_rect = QtCore.QRectF(0, 0, cw, ch)
        crop_rect.moveCenter(QtCore.QPointF(self.rect().center()))
        
        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(self.rect()))
        path.addRect(crop_rect)
        
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        painter.setPen(QtGui.QPen(QtGui.QColor("#00FF00"), 2))
        painter.drawRect(crop_rect)

    def wheelEvent(self, event):
        if not self._original_pixmap:
            return

        # 1. Запоминаем позицию курсора относительно виджета
        mouse_pos = event.position()
        
        # 2. Направление и шаг зума
        delta = event.angleDelta().y()
        zoom_step = 0.1  # 10%
        old_zoom = self._zoom_factor
        
        if delta > 0:
            new_zoom = old_zoom + zoom_step
        else:
            new_zoom = old_zoom - zoom_step
            
        # Ограничения (100% - 500%)
        new_zoom = max(1.0, min(new_zoom, 5.0))
        
        if new_zoom == old_zoom:
            return

        # --- МАТЕМАТИКА УМНОГО ЗУМА ---
        # Находим центр текущей картинки на экране
        rect_center = QtCore.QPointF(self.rect().center()) + self._offset
        
        # Вектор от центра картинки до курсора
        dist_to_cursor = mouse_pos - rect_center
        
        # На сколько реально изменился масштаб
        zoom_ratio = new_zoom / old_zoom
        
        # Корректируем смещение: сдвигаем картинку так, чтобы точка под мышкой не уплыла
        # Новое смещение = Старое смещение - (Вектор до курсора * разница масштаба - Вектор до курсора)
        self._offset -= dist_to_cursor * (zoom_ratio - 1)

        # Применяем новый зум
        self.set_zoom(int(new_zoom * 100))
        
        # Синхронизируем слайдер в UI
        parent_logic = self.window()
        if hasattr(parent_logic, 'slider_zoom'):
            parent_logic.slider_zoom.blockSignals(True) # Чтобы не было зацикливания
            parent_logic.slider_zoom.setValue(int(new_zoom * 100))
            parent_logic.slider_zoom.blockSignals(False)
            if hasattr(parent_logic, 'update_zoom_label'):
                parent_logic.update_zoom_label(int(new_zoom * 100))
    
    def get_transform_params(self):
        """Возвращает все данные, необходимые для финальной обрезки"""
        return {
            "ratio": self._current_ratio,
            "zoom": self._zoom_factor,
            "offset": self._offset,
            "view_size": self.size()
        }
    
    def update_from_pil(self, pil_image):
        """Конвертирует PIL Image в QPixmap и отображает его"""
        # Превращаем PIL в данные, которые понимает Qt
        data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QtGui.QImage(data, pil_image.size[0], pil_image.size[1], QtGui.QImage.Format.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        
        # Сбрасываем параметры отображения, так как картинка уже обрезана
        self._offset = QtCore.QPointF(0, 0)
        self._zoom_factor = 1.0
        
        self.set_image(pixmap)