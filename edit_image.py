"""
Image Cropping Module - Handles crop transformations
"""

from PIL import Image
from typing import Tuple


def process_crop(
    image_path: str, 
    ratio: float, 
    zoom: float, 
    offset, 
    view_size
) -> Image.Image:
    """
    Crop an image based on aspect ratio, zoom, and offset parameters
    
    This function translates GUI coordinates (view_size, zoom, offset) into
    actual pixel coordinates for cropping the original image.
    
    Args:
        image_path (str): Path to the source image file
        ratio (float): Target aspect ratio (width/height)
        zoom (float): Zoom factor (1.0 = 100%, 1.5 = 150%, etc.)
        offset (QPointF): Pan offset from center in GUI coordinates
        view_size (QSize): Size of the display widget
        
    Returns:
        PIL.Image: Cropped image
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image cannot be opened or parameters are invalid
    """
    # Validate inputs
    if ratio <= 0:
        raise ValueError(f"Invalid aspect ratio: {ratio}")
    if zoom <= 0:
        raise ValueError(f"Invalid zoom factor: {zoom}")
    
    with Image.open(image_path) as img:
        img_w, img_h = img.size
        
        # Validate image dimensions
        if img_w <= 0 or img_h <= 0:
            raise ValueError(f"Invalid image dimensions: {img_w}x{img_h}")
        
        # Calculate display scale factor
        # This is how Qt fits the image into the widget (KeepAspectRatio)
        padding = 40
        scale_fit = min(
            (view_size.width() - padding) / img_w, 
            (view_size.height() - padding) / img_h
        )
        
        # Total scale includes both fit-to-window and user zoom
        total_scale = scale_fit * zoom
        
        if total_scale <= 0:
            raise ValueError(f"Invalid total scale: {total_scale}")
        
        # Calculate crop frame size in GUI coordinates
        vw = view_size.width() - padding
        vh = view_size.height() - padding
        
        if vw / vh > ratio:
            cw = vh * ratio
            ch = vh
        else:
            cw = vw
            ch = vw / ratio
            
        # Convert crop dimensions to original image pixels
        crop_w_orig = cw / total_scale
        crop_h_orig = ch / total_scale
        
        # Calculate crop center in original image coordinates
        # Offset is inverted because GUI moves image, not crop frame
        offset_x_orig = offset.x() / total_scale
        offset_y_orig = offset.y() / total_scale
        
        center_x = img_w / 2 - offset_x_orig
        center_y = img_h / 2 - offset_y_orig
        
        # Calculate crop box coordinates (left, top, right, bottom)
        left = center_x - crop_w_orig / 2
        top = center_y - crop_h_orig / 2
        right = center_x + crop_w_orig / 2
        bottom = center_y + crop_h_orig / 2
        
        # Clamp to image boundaries to avoid errors
        left = max(0, left)
        top = max(0, top)
        right = min(img_w, right)
        bottom = min(img_h, bottom)
        
        # Validate crop box
        if right <= left or bottom <= top:
            raise ValueError(
                f"Invalid crop box: ({left}, {top}, {right}, {bottom})"
            )
        
        # Perform crop
        cropped_img = img.crop((left, top, right, bottom))
        
        return cropped_img


def validate_image_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate if a file is a valid image
    
    Args:
        file_path (str): Path to file to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True, ""
    except FileNotFoundError:
        return False, "File not found"
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"