"""
Image2Pixel - Main Application Logic
A PyQt6-based image cropping and pixelation tool
"""

import sys
import os
from pathlib import Path
from PyQt6 import QtWidgets, QtGui
from gui import SimpleAppGui
from edit_image import process_crop
from pixel_transform import apply_pixelate
from PIL import Image


class AppLogic(SimpleAppGui):
    """Main application logic handling user interactions and image processing"""
    
    # Constants
    DEFAULT_ZOOM = 100
    MIN_ZOOM = 100
    MAX_ZOOM = 500
    
    def __init__(self):
        super().__init__()
        self.current_file_path = None 
        self.last_processed_image = None 
        self.image_after_crop = None 

        self._connect_signals()

    def _connect_signals(self):
        """Connect all UI signals to their handlers"""
        # Button connections
        self.btn_load.clicked.connect(self.load_image)
        self.btn_apply.clicked.connect(self.apply_transform)
        self.btn_pixel_apply.clicked.connect(self.apply_pixel)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_reset.clicked.connect(self.reset_image)

        # UI control signals
        self.combo_ratio.currentTextChanged.connect(self.image_display.set_ratio)
        self.combo_ratio.activated.connect(lambda: self.image_display.set_overlay_visible(True))
        
        self.slider_zoom.valueChanged.connect(self.update_zoom_label) 
        self.slider_zoom.valueChanged.connect(self.image_display.set_zoom)
        self.check_free_mode.stateChanged.connect(self.image_display.set_free_mode)
        self.slider_pixel.valueChanged.connect(self.update_pixel_label)

    def update_zoom_label(self, value):
        """Update zoom label text with current zoom percentage"""
        self.label_zoom.setText(f"Zoom: {value}%")

    def update_pixel_label(self, value):
        """Update pixelation label text"""
        text = "Pixelation: Off" if value == 0 else f"Pixelation: {value} segments"
        self.label_pixel.setText(text)

    def update_info_status(self, width, height):
        """Update status bar with current image info"""
        if self.current_file_path:
            name = Path(self.current_file_path).name
            self.info_label.setText(f" 📂 {name}  |  📏 {width} x {height} px")

    def load_image(self):
        """Load an image file and display it"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Open Image", 
            "", 
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        
        if not file_path:
            return
            
        try:
            # Validate file exists and is readable
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Try to open with PIL first to validate it's a valid image
            img = Image.open(file_path)
            img.verify()  # Verify it's actually an image
            
            # Reopen after verify (verify closes the file)
            img = Image.open(file_path)
            
            self.current_file_path = file_path
            self.last_processed_image = img
            self.image_after_crop = img
            
            # Load into Qt
            pixmap = QtGui.QPixmap(file_path)
            if pixmap.isNull():
                raise ValueError("Failed to load image into Qt")
                
            self.image_display.set_image(pixmap)
            self.image_display.set_overlay_visible(True)
            self.update_info_status(pixmap.width(), pixmap.height())
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Error Loading Image", 
                f"Failed to load image:\n{str(e)}"
            )

    def apply_transform(self):
        """Apply crop transformation to the original image"""
        if not self.current_file_path:
            QtWidgets.QMessageBox.information(
                self, 
                "No Image", 
                "Please load an image first"
            )
            return
            
        params = self.image_display.get_transform_params()
        
        if params["ratio"] is None:
            QtWidgets.QMessageBox.information(
                self, 
                "No Aspect Ratio", 
                "Please select an aspect ratio first"
            )
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
            
            # Hide crop overlay and dimming
            self.image_display.set_overlay_visible(False)
            
            # Reset crop UI controls
            self._reset_crop_controls()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Crop Error", 
                f"Failed to crop image:\n{str(e)}"
            )

    def apply_pixel(self):
        """Apply pixelation effect to the cropped image"""
        if self.image_after_crop is None:
            QtWidgets.QMessageBox.information(
                self, 
                "No Image", 
                "Please crop an image first"
            )
            return
        
        val = self.slider_pixel.value()
        
        try:
            if val == 0:
                # Reset to clean crop when slider is at 0
                self.last_processed_image = self.image_after_crop.copy()
            else:
                # Always pixelate from clean crop to avoid cumulative blur
                self.last_processed_image = apply_pixelate(self.image_after_crop, val)
            
            self.refresh_display()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Pixelation Error", 
                f"Failed to apply pixelation:\n{str(e)}"
            )

    def refresh_display(self):
        """Synchronize PIL Image to display"""
        if self.last_processed_image is None:
            return
            
        self.image_display.update_from_pil(self.last_processed_image)
        self.update_info_status(
            self.last_processed_image.width, 
            self.last_processed_image.height
        )

    def save_image(self):
        """Save the processed image to file"""
        if self.last_processed_image is None:
            QtWidgets.QMessageBox.information(
                self, 
                "No Image", 
                "No processed image to save"
            )
            return
            
        ext = self.combo_ext.currentText().lower()
        default_name = f"result.{ext}"
        
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Save Image", 
            default_name, 
            f"*.{ext}"
        )
        
        if not path:
            return
            
        try:
            # Ensure path has correct extension
            if not path.lower().endswith(f".{ext}"):
                path = f"{path}.{ext}"
                
            self.last_processed_image.save(path)
            QtWidgets.QMessageBox.information(
                self, 
                "Success", 
                f"Image saved successfully to:\n{path}"
            )
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Save Error", 
                f"Failed to save image:\n{str(e)}"
            )

    def reset_image(self):
        """Reset all transformations and reload original image"""
        if not self.current_file_path:
            return

        try:
            original_img = Image.open(self.current_file_path)
            pixmap = QtGui.QPixmap(self.current_file_path)
            
            self.image_display.set_image(pixmap)
            self.last_processed_image = original_img
            self.image_after_crop = original_img
            
            # Show crop overlay again
            self.image_display.set_overlay_visible(True)
            
            # Reset all UI controls
            self._reset_crop_controls()
            self._reset_pixel_controls()
            
            self.update_info_status(pixmap.width(), pixmap.height())
            self.image_display.set_zoom(self.DEFAULT_ZOOM)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Reset Error", 
                f"Failed to reset image:\n{str(e)}"
            )

    def _reset_crop_controls(self):
        """Reset crop-related UI controls to default state"""
        self.slider_zoom.blockSignals(True)
        self.slider_zoom.setValue(self.DEFAULT_ZOOM)
        self.update_zoom_label(self.DEFAULT_ZOOM)
        self.slider_zoom.blockSignals(False)
        
        self.check_free_mode.setChecked(False)
        
        self.combo_ratio.blockSignals(True)
        self.combo_ratio.setCurrentIndex(0)
        self.combo_ratio.blockSignals(False)

    def _reset_pixel_controls(self):
        """Reset pixelation-related UI controls to default state"""
        self.slider_pixel.blockSignals(True)
        self.slider_pixel.setValue(0)
        self.update_pixel_label(0)
        self.slider_pixel.blockSignals(False)


def main():
    """Application entry point"""
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Image2Pixel")
    app.setOrganizationName("Image2Pixel")
    
    window = AppLogic()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()