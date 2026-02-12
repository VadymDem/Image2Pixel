import sys
import os
from PyQt6 import QtWidgets, QtGui
from gui import SimpleAppGui
from edit_image import process_crop
from pixel_transform import apply_pixelate
from PIL import Image

class AppLogic(SimpleAppGui):
    def __init__(self):
        super().__init__()
        self.current_file_path = None 
        self.last_processed_image = None 
        self.image_after_crop = None 

        # Подключаем кнопки
        self.btn_load.clicked.connect(self.load_image)
        self.btn_apply.clicked.connect(self.apply_transform)
        self.btn_pixel_apply.clicked.connect(self.apply_pixel)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_reset.clicked.connect(self.reset_image)

        # Сигналы интерфейса
        self.combo_ratio.currentTextChanged.connect(self.image_display.set_ratio)
        # Если пользователь выбирает новый ратио — показываем рамку снова
        self.combo_ratio.activated.connect(lambda: self.image_display.set_overlay_visible(True))
        
        self.slider_zoom.valueChanged.connect(self.update_zoom_label) 
        self.slider_zoom.valueChanged.connect(self.image_display.set_zoom)
        self.check_free_mode.stateChanged.connect(self.image_display.set_free_mode)
        self.slider_pixel.valueChanged.connect(self.update_pixel_label)

    def update_zoom_label(self, value):
        self.label_zoom.setText(f"Масштаб: {value}%")

    def update_pixel_label(self, value):
        self.label_pixel.setText("Пикселизация: Выкл" if value == 0 else f"Пикселизация: {value} сегм.")

    def update_info_status(self, width, height):
        if self.current_file_path:
            name = os.path.basename(self.current_file_path)
            self.info_label.setText(f" 📂 {name}  |  📏 {width} x {height} px")

    def load_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self.current_file_path = file_path 
            img = Image.open(file_path)
            self.last_processed_image = img
            self.image_after_crop = img
            pixmap = QtGui.QPixmap(file_path)
            if not pixmap.isNull():
                self.image_display.set_image(pixmap)
                self.image_display.set_overlay_visible(True)
                self.update_info_status(pixmap.width(), pixmap.height())

    def apply_transform(self):
        """Функция КРОПА (работает с исходным файлом)"""
        if not self.current_file_path: return
        params = self.image_display.get_transform_params()
        if params["ratio"] is None:
            QtWidgets.QMessageBox.information(self, "Инфо", "Выберите соотношение сторон")
            return

        try:
            cropped = process_crop(
                self.current_file_path,
                params["ratio"],
                params["zoom"],
                params["offset"],
                params["view_size"]
            )
            self.image_after_crop = cropped
            self.last_processed_image = cropped
            self.refresh_display()
            
            # --- СКРЫВАЕМ РАМКУ И ЗАТЕНЕНИЕ ---
            self.image_display.set_overlay_visible(False)
            
            # Сброс инструментов кропа в UI
            self.slider_zoom.blockSignals(True)
            self.slider_zoom.setValue(100)
            self.update_zoom_label(100)
            self.slider_zoom.blockSignals(False)
            
            self.check_free_mode.setChecked(False)
            
            # Сбрасываем выбор в комбобоксе, чтобы не висело старое значение
            self.combo_ratio.blockSignals(True)
            self.combo_ratio.setCurrentIndex(0)
            self.combo_ratio.blockSignals(False)
            
        except Exception as e:
            print(f"Ошибка кропа: {e}")

    def apply_pixel(self):
        """Обновленная логика пикселизации"""
        if self.image_after_crop is None: return
        
        val = self.slider_pixel.value()
        
        if val == 0:
            # Если ползунок на "Выкл", возвращаем дефолтное состояние (чистый кроп)
            self.last_processed_image = self.image_after_crop.copy()
            print("Эффекты сброшены до чистого кропа.")
        else:
            try:
                # Пикселизируем всегда ОТ чистого кропа, чтобы не "мылить" уже пиксельную картинку
                self.last_processed_image = apply_pixelate(self.image_after_crop, val)
            except Exception as e:
                print(f"Ошибка пикселизации: {e}")
        
        self.refresh_display()

    def refresh_display(self):
        """Синхронизация PIL Image -> Экран"""
        self.image_display.update_from_pil(self.last_processed_image)
        self.update_info_status(self.last_processed_image.width, self.last_processed_image.height)

    def save_image(self):
        if self.last_processed_image is None: return
        ext = self.combo_ext.currentText().lower()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить", f"result.{ext}", f"*.{ext}")
        if path:
            self.last_processed_image.save(path)
            QtWidgets.QMessageBox.information(self, "ОК", "Файл сохранен!")

    def reset_image(self):
        if not self.current_file_path:
            return

        try:
            original_img = Image.open(self.current_file_path)
            pixmap = QtGui.QPixmap(self.current_file_path)
            self.image_display.set_image(pixmap)
            self.last_processed_image = original_img
            self.image_after_crop = original_img
            # Показываем рамку обратно
            self.image_display.set_overlay_visible(True)
            
            # Сброс UI
            self.slider_zoom.blockSignals(True)
            self.slider_zoom.setValue(100)
            self.update_zoom_label(100)
            self.slider_zoom.blockSignals(False)
            
            self.slider_pixel.blockSignals(True)
            self.slider_pixel.setValue(0)
            self.update_pixel_label(0)
            self.slider_pixel.blockSignals(False)
            
            self.check_free_mode.setChecked(False)
            
            self.combo_ratio.blockSignals(True)
            self.combo_ratio.setCurrentIndex(0)
            self.combo_ratio.blockSignals(False)
            
            self.update_info_status(pixmap.width(), pixmap.height())
            self.image_display.set_zoom(100)
            
            print("Сброшено.")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка сброса", f"{e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppLogic()
    window.show()
    sys.exit(app.exec())