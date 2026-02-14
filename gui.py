"""
GUI Layout - Main window interface for Image2Pixel
"""

from PyQt6 import QtWidgets, QtCore
from display_image import ImageDisplay


class SimpleAppGui(QtWidgets.QMainWindow):
    """Main GUI window with controls and image display"""
    
    # UI Constants
    WINDOW_TITLE = "Image2Pixel - Crop & Pixelate Tool"
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 700
    
    # Zoom range
    ZOOM_MIN = 100
    ZOOM_MAX = 500
    
    # Pixelation range  
    PIXEL_MIN = 0
    PIXEL_MAX = 200
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_widgets()
        self._setup_layout()

    def _setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(central_widget)

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main action buttons
        self.btn_load = QtWidgets.QPushButton("📂 Load Image")
        self.btn_reset = QtWidgets.QPushButton("🔄 Reset All")
        self.btn_reset.setStyleSheet("color: #c0392b; font-weight: bold;")
        
        # Crop controls
        self._create_crop_widgets()
        
        # Pixelation controls
        self._create_pixel_widgets()
        
        # Save controls
        self._create_save_widgets()
        
        # Image display
        self.image_display = ImageDisplay()
        
        # Info label
        self.info_label = QtWidgets.QLabel("No image loaded")
        self.info_label.setStyleSheet("""
            background: #2c3e50; 
            color: white; 
            padding: 8px; 
            font-family: 'Consolas', 'Monaco', monospace;
            border-bottom-right-radius: 5px;
        """)

    def _create_crop_widgets(self):
        """Create crop-related widgets"""
        self.group_crop = QtWidgets.QGroupBox("Cropping")
        crop_layout = QtWidgets.QVBoxLayout()
        
        # Aspect ratio selector
        self.combo_ratio = QtWidgets.QComboBox()
        self.combo_ratio.addItems(["Original", "1:1", "4:3", "16:9"])
        
        # Free positioning mode
        self.check_free_mode = QtWidgets.QCheckBox("Free Positioning")
        self.check_free_mode.setToolTip(
            "Enable to freely pan the image.\n"
            "Use mouse drag to reposition."
        )
        
        # Zoom controls
        self.label_zoom = QtWidgets.QLabel("Zoom: 100%")
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_zoom.setRange(self.ZOOM_MIN, self.ZOOM_MAX)
        self.slider_zoom.setValue(self.ZOOM_MIN)
        self.slider_zoom.setToolTip("Use mouse wheel for precise zoom control")
        
        # Apply button
        self.btn_apply = QtWidgets.QPushButton("✂️ Apply Crop")
        self.btn_apply.setStyleSheet("font-weight: bold; padding: 6px;")
        
        # Add to layout
        crop_layout.addWidget(QtWidgets.QLabel("Aspect Ratio:"))
        crop_layout.addWidget(self.combo_ratio)
        crop_layout.addWidget(self.check_free_mode)
        crop_layout.addWidget(self.label_zoom)
        crop_layout.addWidget(self.slider_zoom)
        crop_layout.addWidget(self.btn_apply)
        
        self.group_crop.setLayout(crop_layout)

    def _create_pixel_widgets(self):
        """Create pixelation effect widgets"""
        self.group_pixel = QtWidgets.QGroupBox("Effects")
        pixel_layout = QtWidgets.QVBoxLayout()
        
        # Pixelation controls
        self.label_pixel = QtWidgets.QLabel("Pixelation: Off")
        self.slider_pixel = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_pixel.setRange(self.PIXEL_MIN, self.PIXEL_MAX)
        self.slider_pixel.setValue(self.PIXEL_MIN)
        self.slider_pixel.setToolTip(
            "Adjust pixelation intensity.\n"
            "Higher values = more pixelated effect"
        )
        
        # Apply button
        self.btn_pixel_apply = QtWidgets.QPushButton("👾 Apply Pixelation")
        
        # Add to layout
        pixel_layout.addWidget(self.label_pixel)
        pixel_layout.addWidget(self.slider_pixel)
        pixel_layout.addWidget(self.btn_pixel_apply)
        
        self.group_pixel.setLayout(pixel_layout)

    def _create_save_widgets(self):
        """Create save/export widgets"""
        self.combo_ext = QtWidgets.QComboBox()
        self.combo_ext.addItems(["JPG", "PNG", "WebP"])
        self.combo_ext.setCurrentIndex(1)  # Default to PNG
        
        self.btn_save = QtWidgets.QPushButton("💾 Save Result")
        self.btn_save.setStyleSheet(
            "background: #27ae60; color: white; font-weight: bold; padding: 8px;"
        )

    def _setup_layout(self):
        """Arrange all widgets in the main layout"""
        # Left panel - controls
        left_panel = QtWidgets.QVBoxLayout()
        
        left_panel.addWidget(self.btn_load)
        left_panel.addWidget(self.btn_reset)
        left_panel.addSpacing(10)
        left_panel.addWidget(self.group_crop)
        left_panel.addSpacing(10)
        left_panel.addWidget(self.group_pixel)
        left_panel.addStretch()
        left_panel.addWidget(QtWidgets.QLabel("Save Format:"))
        left_panel.addWidget(self.combo_ext)
        left_panel.addWidget(self.btn_save)

        # Right panel - image display
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.image_display, 1)
        right_layout.addWidget(self.info_label)

        # Combine panels (1:4 ratio)
        self.main_layout.addLayout(left_panel, 1)
        self.main_layout.addLayout(right_layout, 4)