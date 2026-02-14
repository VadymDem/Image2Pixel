"""
Pixelation Effect Module - Applies pixel art style transformations
"""

from PIL import Image


def apply_pixelate(image: Image.Image, segments_count: int) -> Image.Image:
    """
    Apply pixelation effect to an image
    
    The algorithm works by:
    1. Downscaling the image to a grid size (segments_count x proportional_height)
    2. Upscaling back to original size using nearest-neighbor interpolation
    
    This creates the characteristic "pixel art" look where groups of pixels
    share the same color.
    
    Args:
        image (PIL.Image): Source image to pixelate
        segments_count (int): Number of pixel segments along width
                             Higher values = less pixelation
                             Typical range: 8-200
        
    Returns:
        PIL.Image: Pixelated image at original resolution
        
    Raises:
        ValueError: If segments_count is invalid
        
    Examples:
        >>> img = Image.open("photo.jpg")
        >>> pixelated = apply_pixelate(img, 32)  # 32 segments = heavy pixelation
        >>> pixelated = apply_pixelate(img, 128) # 128 segments = light pixelation
    """
    # Validate input
    if segments_count <= 0:
        raise ValueError(f"segments_count must be positive, got {segments_count}")
    
    if not isinstance(image, Image.Image):
        raise TypeError(f"Expected PIL Image, got {type(image)}")

    # Store original dimensions
    original_size = image.size
    
    # Calculate downscaled dimensions
    # Width becomes segments_count, height scales proportionally
    w, h = original_size
    
    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid image dimensions: {w}x{h}")
    
    aspect_ratio = h / w
    small_w = segments_count
    small_h = max(1, int(small_w * aspect_ratio))  # Ensure at least 1 pixel height
    
    try:
        # Step 1: Downscale to create pixel grid
        # BOX resampling averages colors within each segment for better quality
        small_img = image.resize(
            (small_w, small_h), 
            resample=Image.Resampling.BOX
        )
        
        # Step 2: Upscale back to original size
        # NEAREST interpolation preserves sharp pixel boundaries
        pixelated = small_img.resize(
            original_size, 
            resample=Image.Resampling.NEAREST
        )
        
        return pixelated
        
    except Exception as e:
        raise RuntimeError(f"Pixelation failed: {str(e)}") from e


def get_recommended_segment_count(image: Image.Image, intensity: str = "medium") -> int:
    """
    Get recommended segment count based on image size and desired intensity
    
    Args:
        image (PIL.Image): Source image
        intensity (str): Desired effect intensity ("light", "medium", "heavy")
        
    Returns:
        int: Recommended segments_count value
        
    Raises:
        ValueError: If intensity is not recognized
    """
    intensity_map = {
        "light": 0.15,    # 15% of width
        "medium": 0.08,   # 8% of width  
        "heavy": 0.04,    # 4% of width
    }
    
    if intensity not in intensity_map:
        raise ValueError(
            f"Unknown intensity '{intensity}'. "
            f"Use: {', '.join(intensity_map.keys())}"
        )
    
    width = image.size[0]
    segments = max(8, int(width * intensity_map[intensity]))
    
    return segments