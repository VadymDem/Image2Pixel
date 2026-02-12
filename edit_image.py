from PIL import Image

def process_crop(image_path, ratio, zoom, offset, view_size):
    """
    image_path: путь к файлу
    ratio: целевое соотношение (например, 1.0 или 1.77)
    zoom: фактор масштаба (1.0, 1.5 и т.д.)
    offset: смещение QPointF(x, y) из GUI
    view_size: размер виджета QLabel (QSize), чтобы рассчитать пропорции
    """
    with Image.open(image_path) as img:
        img_w, img_h = img.size
        
        # 1. Считаем масштаб отображения (как Qt вписал картинку в окно)
        # Мы использовали KeepAspectRatio. Находим коэффициент "экран / оригинал"
        scale_fit = min((view_size.width() - 40) / img_w, (view_size.height() - 40) / img_h)
        
        # Общий масштаб (вписывание + пользовательский зум)
        total_scale = scale_fit * zoom
        
        # 2. Определяем размер рамки обрезки на экране
        vw, vh = view_rect_w = view_size.width() - 40, view_size.height() - 40
        if vw / vh > ratio:
            cw, ch = vh * ratio, vh
        else:
            cw, ch = vw, vw / ratio
            
        # 3. Пересчитываем размеры рамки в пиксели оригинала
        crop_w_orig = cw / total_scale
        crop_h_orig = ch / total_scale
        
        # 4. Находим центр обрезки относительно центра изображения
        # Смещение в GUI (offset) нужно инвертировать и масштабировать
        offset_x_orig = offset.x() / total_scale
        offset_y_orig = offset.y() / total_scale
        
        center_x = img_w / 2 - offset_x_orig
        center_y = img_h / 2 - offset_y_orig
        
        # 5. Вычисляем координаты углов (Left, Top, Right, Bottom)
        left = center_x - crop_w_orig / 2
        top = center_y - crop_h_orig / 2
        right = center_x + crop_w_orig / 2
        bottom = center_y + crop_h_orig / 2
        
        # Обрезаем
        cropped_img = img.crop((left, top, right, bottom))
        
        return cropped_img