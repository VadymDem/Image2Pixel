from PIL import Image

def apply_pixelate(image, segments_count):
    """
    image: PIL Image
    segments_count: количество сегментов по ширине (например, 64)
    """
    if segments_count <= 0:
        return image

    # Запоминаем исходный размер
    original_size = image.size
    
    # Вычисляем размер маленькой картинки (иконки)
    # Ширина будет равна количеству сегментов
    w, h = original_size
    ratio = h / w
    small_w = segments_count
    small_h = int(small_w * ratio)
    
    # 1. Сжимаем до размеров сетки пикселизации
    # Используем BOX или BILINEAR для усреднения цветов внутри сегментов
    small_img = image.resize((small_w, small_h), resample=Image.Resampling.BOX)
    
    # 2. Растягиваем обратно до оригинального размера
    # Используем NEAREST, чтобы сохранить четкие границы "пикселей"
    pixelated = small_img.resize(original_size, resample=Image.Resampling.NEAREST)
    
    return pixelated