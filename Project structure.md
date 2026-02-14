# Project Structure

## Overview
Image2Pixel is organized into modular Python files, each with a specific responsibility.


```
image2pixel/
│
├── main.py            # Application entry point and logic
├── gui.py             # GUI layout and widgets
├── display_image.py   # Custom image display widget
├── edit_image.py      # Crop transformation logic
├── pixel_transform.py # Pixelation effect implementation
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## File Descriptions

### Core Application Files

#### `main.py` (Entry Point)
- **Purpose:** Application logic and user interaction handling
- **Key Class:** `AppLogic(SimpleAppGui)`
- **Responsibilities:**
  - Connect UI signals to handlers
  - Manage application state
  - Handle file loading/saving
  - Coordinate crop and pixelation operations
  - Error handling and user feedback

**Key Methods:**
- `load_image()` - Load image from file
- `apply_transform()` - Apply crop transformation
- `apply_pixel()` - Apply pixelation effect
- `save_image()` - Save processed image
- `reset_image()` - Reset to original state

#### `gui.py` (User Interface)
- **Purpose:** GUI layout and widget creation
- **Key Class:** `SimpleAppGui(QMainWindow)`
- **Responsibilities:**
  - Create all UI widgets
  - Define layout structure
  - Set up styling and tooltips
  - No business logic (separation of concerns)

**UI Sections:**
- Left panel: Controls (crop, pixelation, save)
- Right panel: Image display and info bar

#### `display_image.py` (Interactive Display)
- **Purpose:** Custom image widget with interactive features
- **Key Class:** `ImageDisplay(QLabel)`
- **Responsibilities:**
  - Display images with zoom and pan
  - Draw crop overlay
  - Handle mouse interactions
  - Coordinate transformations

**Key Features:**
- Smart zoom (keeps cursor point stationary)
- Pan with mouse drag
- Crop preview overlay
- Real-time visual feedback

#### `edit_image.py` (Crop Processing)
- **Purpose:** Image cropping calculations
- **Key Function:** `process_crop()`
- **Responsibilities:**
  - Translate GUI coordinates to image pixels
  - Calculate crop boundaries
  - Apply crop transformation
  - Validate parameters

**Algorithm:**
1. Calculate display scale factor
2. Determine crop frame size
3. Convert to original image coordinates
4. Apply crop with PIL

#### `pixel_transform.py` (Pixelation Effect)
- **Purpose:** Pixelation effect implementation
- **Key Function:** `apply_pixelate()`
- **Responsibilities:**
  - Apply pixel art effect
  - Maintain aspect ratio
  - Preserve image quality where possible

**Algorithm:**
1. Downscale to grid size (segments × proportional height)
2. Upscale back to original using nearest-neighbor
3. Result: blocky pixel art effect

### Configuration Files

#### `requirements.txt`
Lists Python dependencies:

PyQt6>=6.4.0
Pillow>=9.0.0


#### `setup.py`
Package distribution configuration for pip installation.

#### `.gitignore`
Specifies files Git should ignore:
- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Output images (`.jpg`, `.png`, etc.)

### Documentation Files

#### `README.md`
Main project documentation:
- Features overview
- Installation instructions
- Basic usage guide
- Project structure
- Contribution info

#### `CHANGELOG.md`
Version history:
- Release notes for each version
- New features
- Bug fixes
- Breaking changes

#### `CONTRIBUTING.md`
Guidelines for contributors:
- Code style requirements
- Commit message format
- Pull request process
- Development setup

#### `USAGE_EXAMPLES.md`
Detailed usage examples:
- Common workflows
- Social media formats
- Advanced techniques
- Troubleshooting

#### `RELEASE_CHECKLIST.md`
Pre-release verification:
- Code quality checks
- Testing requirements
- Documentation completeness
- GitHub setup steps

#### `LICENSE`
MIT License - open source, permissive license.

## Architecture Principles

### Separation of Concerns
- **GUI (`gui.py`)**: Only UI layout, no logic
- **Logic (`main.py`)**: Application flow, no GUI details
- **Display (`display_image.py`)**: Visual interactions
- **Processing (`edit_image.py`, `pixel_transform.py`)**: Pure image operations

### Benefits:
- Easy to test individual components
- Changes to one part don't break others
- Clear responsibility boundaries
- Easy to extend with new features

### Data Flow


User Action → GUI Signal → AppLogic Handler → Image Processing → Display Update


**Example Flow (Crop):**
1. User clicks "Apply Crop" button
2. GUI emits signal
3. `AppLogic.apply_transform()` called
4. Gets parameters from `ImageDisplay.get_transform_params()`
5. Calls `process_crop()` with parameters
6. Updates `self.image_after_crop`
7. Calls `refresh_display()` to show result

### State Management

**Application State Variables:**
- `current_file_path`: Original file location
- `last_processed_image`: Currently displayed image
- `image_after_crop`: Clean crop (before pixelation)

**Display State Variables:**
- `_original_pixmap`: Source image for display
- `_current_ratio`: Selected aspect ratio
- `_zoom_factor`: Current zoom level (1.0-5.0)
- `_offset`: Pan offset from center
- `_free_mode`: Pan mode enabled/disabled
- `_show_overlay`: Crop overlay visibility

## Extending the Project

### Adding New Features

#### 1. New Image Effect
**Example:** Add a blur effect

python
# Create new file: blur_effect.py
from PIL import Image, ImageFilter

def apply_blur(image: Image.Image, radius: int) -> Image.Image:
    """Apply Gaussian blur"""
    return image.filter(ImageFilter.GaussianBlur(radius))

# Update gui.py
# Add blur slider widget

# Update main.py
# Add apply_blur() method
def apply_blur(self):
    if self.image_after_crop is None:
        return
    radius = self.slider_blur.value()
    self.last_processed_image = blur_effect.apply_blur(
        self.image_after_crop, 
        radius
    )
    self.refresh_display()


#### 2. New Aspect Ratio
**Example:** Add 9:16 (Instagram Story)

python
# In display_image.py, update set_ratio():
def set_ratio(self, ratio_text):
    ratios = {
        # ... existing ratios ...
        "9:16": 9/16,  # Add this line
    }
    self._current_ratio = ratios.get(ratio_text)
    self.update()

# In gui.py, update combo box:
self.combo_ratio.addItems([
    "Original", "1:1", "4:3", "16:9", "9:16"  # Add "9:16"
])


#### 3. New Export Format
**Example:** Add TIFF support

python
# In gui.py:
self.combo_ext.addItems(["JPG", "PNG", "WebP", "TIFF"])

# main.py already handles this automatically via Pillow


## Testing Strategy

### Manual Testing Checklist
1. Load various image formats
2. Test each aspect ratio
3. Test zoom at extremes (100%, 500%)
4. Test pan in all directions
5. Test pixelation at various levels
6. Test save in each format
7. Test reset functionality
8. Test error cases (invalid files, etc.)

### Future: Automated Testing
python
# Example unit test structure
import unittest
from pixel_transform import apply_pixelate
from PIL import Image

class TestPixelation(unittest.TestCase):
    def test_pixelate_valid_input(self):
        img = Image.new('RGB', (100, 100), 'red')
        result = apply_pixelate(img, 10)
        self.assertEqual(result.size, (100, 100))
    
    def test_pixelate_invalid_segments(self):
        img = Image.new('RGB', (100, 100), 'red')
        with self.assertRaises(ValueError):
            apply_pixelate(img, -1)


## Performance Considerations

### Image Loading
- Large images (>4000px) may take time to load
- PIL handles most formats efficiently
- No optimization currently implemented

### Crop Operation
- Fast - simple PIL crop operation
- Scales well with image size

### Pixelation
- Scales with image size
- Two resize operations per effect
- BOX resampling is fast and high-quality

### Future Optimizations
- Lazy loading for batch processing
- Caching intermediate results
- Threading for large images
- Preview mode with lower resolution

## Dependencies Explanation

### PyQt6
- **Purpose:** GUI framework
- **Why PyQt6:** Modern, cross-platform, well-documented
- **Alternatives:** tkinter (simpler but less capable), wxPython

### Pillow (PIL)
- **Purpose:** Image processing
- **Why Pillow:** Industry standard, comprehensive, fast
- **Alternatives:** OpenCV (overkill for this), scikit-image

## Build and Distribution

### Development

python main.py  # Run directly


### Distribution Options

#### 1. Source Distribution

python setup.py sdist
pip install dist/image2pixel-1.0.0.tar.gz


#### 2. PyPI Upload

pip install twine
python setup.py sdist
twine upload dist/*


#### 3. Executable (PyInstaller)

pip install pyinstaller
pyinstaller --onefile --windowed main.py


## Code Style

### Followed Standards
- PEP 8 compliance
- Google-style docstrings
- Type hints where beneficial
- Constants for magic numbers
- Meaningful variable names

### Example:
python
# Good
CROP_BORDER_WIDTH = 2
OVERLAY_OPACITY = 100

def apply_crop(image: Image.Image, ratio: float) -> Image.Image:
    """
    Apply crop transformation
    
    Args:
        image: Source PIL Image
        ratio: Aspect ratio (width/height)
        
    Returns:
        Cropped PIL Image
    """
    pass

# Avoid
w = 2  # What is 'w'?
o = 100  # What is 'o'?

def crop(i, r):  # No type hints, no docstring
    pass




This structure provides:
- ✅ Modularity
- ✅ Maintainability  
- ✅ Extensibility
- ✅ Clear separation of concerns

- ✅ Comprehensive documentation
