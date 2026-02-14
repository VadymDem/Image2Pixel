"""
Image Display Widget - Custom QLabel with interactive crop and zoom
"""

from PyQt6 import QtWidgets, QtCore, QtGui


class ImageDisplay(QtWidgets.QLabel):
    """
    Custom QLabel widget for displaying images with interactive crop overlay,
    zoom, and pan capabilities.
    """
    
    # Constants
    BORDER_PADDING = 40
    OVERLAY_OPACITY = 100  # 0-255
    CROP_BORDER_COLOR = "#00FF00"
    CROP_BORDER_WIDTH = 2
    MIN_ZOOM = 1.0
    MAX_ZOOM = 5.0
    ZOOM_STEP = 0.1
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; background: #f0f0f0;")
        
        # Initialize all state variables
        self._original_pixmap = None
        self._current_ratio = None
        self._zoom_factor = 1.0
        self._offset = QtCore.QPointF(0, 0)
        self._last_mouse_pos = None
        self._free_mode = False 
        self._show_overlay = True

    def set_overlay_visible(self, visible):
        """
        Toggle crop overlay visibility
        
        Args:
            visible (bool): Whether to show the crop overlay
        """
        self._show_overlay = visible
        self.update()

    def set_image(self, pixmap):
        """
        Set a new image to display
        
        Args:
            pixmap (QPixmap): The image to display
        """
        self._original_pixmap = pixmap
        self._offset = QtCore.QPointF(0, 0)
        self.update()

    def set_ratio(self, ratio_text):
        """
        Set the aspect ratio for cropping
        
        Args:
            ratio_text (str): Ratio name (e.g., "1:1", "16:9")
        """
        ratios = {
            "Original": None,
            "Оригинал": None,
            "1:1": 1.0,
            "4:3": 4/3,
            "16:9": 16/9
        }
        self._current_ratio = ratios.get(ratio_text)
        self.update()

    def set_zoom(self, value):
        """
        Set zoom level
        
        Args:
            value (int): Zoom percentage (100-500)
        """
        self._zoom_factor = value / 100.0
        self.update()

    def set_free_mode(self, state):
        """
        Toggle free pan mode
        
        Args:
            state (int): Qt check state (0=unchecked, 2=checked)
        """
        self._free_mode = bool(state)
        if not self._free_mode:
            self._offset = QtCore.QPointF(0, 0)
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse press for panning"""
        if self._free_mode and event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._last_mouse_pos = event.position()
            self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        """Handle mouse move for panning"""
        if self._free_mode and self._last_mouse_pos is not None:
            delta = event.position() - self._last_mouse_pos
            self._offset += delta
            self._last_mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release after panning"""
        self._last_mouse_pos = None
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def wheelEvent(self, event):
        """
        Handle mouse wheel for zooming
        Implements smart zoom that keeps the point under cursor stationary
        """
        if not self._original_pixmap:
            return

        # Get mouse position relative to widget
        mouse_pos = event.position()
        
        # Determine zoom direction
        delta = event.angleDelta().y()
        old_zoom = self._zoom_factor
        
        if delta > 0:
            new_zoom = old_zoom + self.ZOOM_STEP
        else:
            new_zoom = old_zoom - self.ZOOM_STEP
            
        # Clamp zoom to valid range
        new_zoom = max(self.MIN_ZOOM, min(new_zoom, self.MAX_ZOOM))
        
        if new_zoom == old_zoom:
            return

        # Smart zoom mathematics: keep point under cursor stationary
        # Find current image center on screen
        rect_center = QtCore.QPointF(self.rect().center()) + self._offset
        
        # Vector from image center to cursor
        dist_to_cursor = mouse_pos - rect_center
        
        # Calculate zoom ratio
        zoom_ratio = new_zoom / old_zoom
        
        # Adjust offset so point under cursor doesn't move
        # New offset = Old offset - (Vector to cursor * zoom change - Vector to cursor)
        self._offset -= dist_to_cursor * (zoom_ratio - 1)

        # Apply new zoom
        self.set_zoom(int(new_zoom * 100))
        
        # Sync slider in parent UI
        self._sync_zoom_slider(int(new_zoom * 100))
    
    def _sync_zoom_slider(self, zoom_value):
        """Synchronize zoom slider in parent window without triggering signals"""
        parent_logic = self.window()
        if hasattr(parent_logic, 'slider_zoom'):
            parent_logic.slider_zoom.blockSignals(True)
            parent_logic.slider_zoom.setValue(zoom_value)
            parent_logic.slider_zoom.blockSignals(False)
            if hasattr(parent_logic, 'update_zoom_label'):
                parent_logic.update_zoom_label(zoom_value)

    def paintEvent(self, event):
        """Custom paint event to draw image and crop overlay"""
        if not self._original_pixmap:
            super().paintEvent(event)
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        # Calculate scaled image size to fit widget
        view_size = self.size()
        pix_size = self._original_pixmap.size()
        pix_size.scale(
            view_size - QtCore.QSize(self.BORDER_PADDING, self.BORDER_PADDING), 
            QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
        
        # Apply zoom factor
        tw = pix_size.width() * self._zoom_factor
        th = pix_size.height() * self._zoom_factor
        
        # Center image with offset
        rect_center = self.rect().center()
        dest_rect = QtCore.QRectF(0, 0, tw, th)
        dest_rect.moveCenter(QtCore.QPointF(rect_center) + self._offset)

        # Draw image
        painter.drawPixmap(dest_rect.toRect(), self._original_pixmap)

        # Draw crop overlay if enabled and ratio is selected
        if self._show_overlay and self._current_ratio:
            self._draw_fixed_crop_overlay(painter)
        
        painter.end()

    def _draw_fixed_crop_overlay(self, painter):
        """
        Draw the crop overlay with dimmed areas outside crop region
        
        Args:
            painter (QPainter): Qt painter object
        """
        # Calculate view rectangle with padding
        view_rect = self.rect().adjusted(
            self.BORDER_PADDING // 2, 
            self.BORDER_PADDING // 2, 
            -self.BORDER_PADDING // 2, 
            -self.BORDER_PADDING // 2
        )
        vw = view_rect.width()
        vh = view_rect.height()
        
        # Calculate crop rectangle based on aspect ratio
        if vw / vh > self._current_ratio:
            cw = vh * self._current_ratio
            ch = vh
        else:
            cw = vw
            ch = vw / self._current_ratio
            
        crop_rect = QtCore.QRectF(0, 0, cw, ch)
        crop_rect.moveCenter(QtCore.QPointF(self.rect().center()))
        
        # Create path with dimmed overlay (everything except crop area)
        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(self.rect()))
        path.addRect(crop_rect)
        
        # Draw dimmed overlay
        painter.setBrush(QtGui.QColor(0, 0, 0, self.OVERLAY_OPACITY))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        # Draw crop border
        painter.setPen(QtGui.QPen(
            QtGui.QColor(self.CROP_BORDER_COLOR), 
            self.CROP_BORDER_WIDTH
        ))
        painter.drawRect(crop_rect)

    def get_transform_params(self):
        """
        Get current transformation parameters for cropping
        
        Returns:
            dict: Dictionary containing ratio, zoom, offset, and view_size
        """
        return {
            "ratio": self._current_ratio,
            "zoom": self._zoom_factor,
            "offset": self._offset,
            "view_size": self.size()
        }
    
    def update_from_pil(self, pil_image):
        """
        Convert PIL Image to QPixmap and display it
        
        Args:
            pil_image (PIL.Image): Image to display
        """
        # Convert PIL to Qt-compatible format
        data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QtGui.QImage(
            data, 
            pil_image.size[0], 
            pil_image.size[1], 
            QtGui.QImage.Format.Format_RGBA8888
        )
        pixmap = QtGui.QPixmap.fromImage(qimage)
        
        # Reset display parameters since image is already processed
        self._offset = QtCore.QPointF(0, 0)
        self._zoom_factor = 1.0
        
        self.set_image(pixmap)