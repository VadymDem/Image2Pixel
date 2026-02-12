from PyQt6 import QtWidgets, QtCore
from display_image import ImageDisplay  # Импортируем наш новый класс

class SimpleAppGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image2Pixel")
        self.resize(1000, 600)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        # Корректировка позиции и масштабирование 
        self.check_free_mode = QtWidgets.QCheckBox("Свободный подгон")
                
        self.label_zoom = QtWidgets.QLabel("Масштаб: 100%")
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_zoom.setRange(100, 500)
        self.slider_zoom.setValue(100)

        self.btn_apply = QtWidgets.QPushButton("Применить трансформацию")

        # Левая панель параметров
        left_panel = QtWidgets.QVBoxLayout()
        self.btn_load = QtWidgets.QPushButton("Загрузить изображение")
        self.combo_ratio = QtWidgets.QComboBox()
        self.combo_ratio.addItems(["Оригинал", "1:1", "4:3", "16:9"])
        self.combo_ext = QtWidgets.QComboBox()
        self.combo_ext.addItems(["JPG", "PNG", "WebP"])
        self.btn_save = QtWidgets.QPushButton("Сохранить результат как...")

        left_panel.addWidget(self.btn_load)
        left_panel.addWidget(QtWidgets.QLabel("Соотношение сторон:"))
        left_panel.addWidget(self.combo_ratio)
        left_panel.addWidget(QtWidgets.QLabel("Расширение:"))
        left_panel.addWidget(self.combo_ext)
        left_panel.addWidget(self.check_free_mode)
        left_panel.addWidget(self.label_zoom)
        left_panel.addWidget(self.slider_zoom)
        left_panel.insertWidget(1, self.btn_apply)
        left_panel.addStretch()
        left_panel.addWidget(self.btn_save)

        # ИСПОЛЬЗУЕМ НАШ НОВЫЙ ВИДЖЕТ
        self.image_display = ImageDisplay()
        self.info_label = QtWidgets.QLabel("Файл не загружен")
        self.info_label.setStyleSheet("background: #e0e0e0; padding: 5px; font-weight: bold; border-top: 1px solid #ccc;")
        self.info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        # Создаем вертикальный слой для правой части, чтобы прижать инфо к низу
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.image_display, 1) # Картинка занимает всё место
        right_layout.addWidget(self.info_label)       # Полоска снизу

        # В основном слое заменяем старое добавление:
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_layout, 4) # Добавляем слой вместо одного виджета
