from PyQt6 import QtWidgets, QtCore
from display_image import ImageDisplay

class SimpleAppGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image2Pixel")
        self.resize(1100, 700)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        # Левая панель параметров
        left_panel = QtWidgets.QVBoxLayout()
        
        self.btn_load = QtWidgets.QPushButton("📂 Загрузить изображение")
        self.btn_reset = QtWidgets.QPushButton("🔄 Сбросить изменения")
        # Стилизуем её чуть иначе, чтобы она выделялась
        self.btn_reset.setStyleSheet("color: #c0392b; font-weight: bold;")
        # Блок трансформации
        self.group_crop = QtWidgets.QGroupBox("Кадрирование")
        crop_layout = QtWidgets.QVBoxLayout()
        self.combo_ratio = QtWidgets.QComboBox()
        self.combo_ratio.addItems(["Оригинал", "1:1", "4:3", "16:9"])
        self.check_free_mode = QtWidgets.QCheckBox("Свободный подгон")
        self.label_zoom = QtWidgets.QLabel("Масштаб: 100%")
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_zoom.setRange(100, 500)
        self.btn_apply = QtWidgets.QPushButton("✂️ Применить кроп")
        
        crop_layout.addWidget(QtWidgets.QLabel("Соотношение сторон:"))
        crop_layout.addWidget(self.combo_ratio)
        crop_layout.addWidget(self.check_free_mode)
        crop_layout.addWidget(self.label_zoom)
        crop_layout.addWidget(self.slider_zoom)
        crop_layout.addWidget(self.btn_apply)
        self.group_crop.setLayout(crop_layout)

        # Блок пикселизации
        self.group_pixel = QtWidgets.QGroupBox("Эффекты")
        pixel_layout = QtWidgets.QVBoxLayout()
        self.label_pixel = QtWidgets.QLabel("Пикселизация: Выкл")
        self.slider_pixel = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_pixel.setRange(0, 200)
        self.btn_pixel_apply = QtWidgets.QPushButton("👾 Пикселизировать")
        
        pixel_layout.addWidget(self.label_pixel)
        pixel_layout.addWidget(self.slider_pixel)
        pixel_layout.addWidget(self.btn_pixel_apply)
        self.group_pixel.setLayout(pixel_layout)

        # Блок сохранения
        self.combo_ext = QtWidgets.QComboBox()
        self.combo_ext.addItems(["JPG", "PNG", "WebP"])
        self.btn_save = QtWidgets.QPushButton("💾 Сохранить результат")

        left_panel.addWidget(self.btn_load)
        left_panel.addWidget(self.btn_reset)
        left_panel.addWidget(self.group_crop)
        left_panel.addWidget(self.group_pixel)
        left_panel.addStretch()
        left_panel.addWidget(QtWidgets.QLabel("Формат сохранения:"))
        left_panel.addWidget(self.combo_ext)
        left_panel.addWidget(self.btn_save)

        # Правая панель (Отображение)
        right_layout = QtWidgets.QVBoxLayout()
        self.image_display = ImageDisplay()
        
        self.info_label = QtWidgets.QLabel("Файл не загружен")
        self.info_label.setStyleSheet("""
            background: #2c3e50; 
            color: white; 
            padding: 8px; 
            font-family: 'Consolas';
            border-bottom-right-radius: 5px;
        """)
        
        right_layout.addWidget(self.image_display, 1)
        right_layout.addWidget(self.info_label)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_layout, 4)