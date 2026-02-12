import sys
import os
from PyQt6 import QtWidgets, QtGui
from gui import SimpleAppGui
from edit_image import process_crop

class AppLogic(SimpleAppGui):
    def __init__(self):
        super().__init__()
        self.current_file_path = None 
        
        # Подключаем кнопки
        self.btn_load.clicked.connect(self.load_image)
        self.btn_apply.clicked.connect(self.apply_transform)
        # Если добавил кнопку Reset в gui.py:
        # self.btn_reset.clicked.connect(self.reset_image)
        
        # Сигналы интерфейса
        self.combo_ratio.currentTextChanged.connect(self.image_display.set_ratio)
        self.slider_zoom.valueChanged.connect(self.update_zoom_label) # ОШИБКА БЫЛА ЗДЕСЬ
        self.slider_zoom.valueChanged.connect(self.image_display.set_zoom)
        self.check_free_mode.stateChanged.connect(self.image_display.set_free_mode)

    def update_zoom_label(self, value):
        self.label_zoom.setText(f"Масштаб: {value}%")

    def update_info_status(self, file_path, width, height):
        name = os.path.basename(file_path)
        # Название файла + Размеры в пикселях
        self.info_label.setText(f" 📂 Файл: {name}   |   📏 Размер: {width} x {height} px")

    # Обнови метод load_image:
    def load_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Выберите изображение", 
            "", 
            "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self.current_file_path = file_path 
            pixmap = QtGui.QPixmap(file_path)
            if not pixmap.isNull():
                self.image_display.set_image(pixmap)
                self.slider_zoom.setValue(100)
                # ОБНОВЛЯЕМ ИНФО
                self.update_info_status(file_path, pixmap.width(), pixmap.height())

    def apply_transform(self):
        if not self.current_file_path:
            return

        params = self.image_display.get_transform_params()
        if params["ratio"] is None:
            return

        try:
            # Обработка через Pillow в edit_image.py
            cropped_pil = process_crop(
                self.current_file_path,
                params["ratio"],
                params["zoom"],
                params["offset"],
                params["view_size"]
            )
            
            # Обновляем экран результатом
            self.image_display.update_from_pil(cropped_pil)
            # ОБНОВЛЯЕМ ИНФО (берем размеры у Pillow объекта)
            self.update_info_status(self.current_file_path, cropped_pil.width, cropped_pil.height)
        
            # Сбрасываем ползунки в нейтральное положение
            self.slider_zoom.blockSignals(True)
            self.slider_zoom.setValue(100)
            self.update_zoom_label(100)
            self.slider_zoom.blockSignals(False)
            self.check_free_mode.setChecked(False)
            
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppLogic()
    window.show()
    sys.exit(app.exec())