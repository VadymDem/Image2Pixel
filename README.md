# Image2Pixel 🎨

A powerful and user-friendly desktop application for cropping and pixelating images with real-time preview.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features ✨

- **🖼️ Interactive Image Cropping**
  - Multiple aspect ratios (1:1, 4:3, 16:9, or original)
  - Real-time crop preview with overlay
  - Zoom and pan controls (100%-500%)
  - Mouse wheel zoom with smart anchor point
  - Free positioning mode for precise control

- **👾 Pixelation Effects**
  - Adjustable pixelation intensity (0-200 segments)
  - Real-time preview
  - Pixel art style rendering

- **💾 Export Options**
  - Multiple format support (JPG, PNG, WebP)
  - Preserves quality
  - One-click save

## Screenshots

*Coming soon*

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start

1. Clone the repository:

git clone https://github.com/yourusername/image2pixel.git
cd image2pixel


2. Install dependencies:

pip install -r requirements.txt


3. Run the application:

python main.py


### Alternative Installation

If you prefer using a virtual environment:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py


## Usage Guide 📖

### Basic Workflow

1. **Load Image**: Click "📂 Load Image" and select your image file
2. **Crop (Optional)**:
   - Select an aspect ratio from the dropdown
   - Use the zoom slider or mouse wheel to adjust zoom
   - Enable "Free Positioning" to pan the image
   - Click "✂️ Apply Crop" when ready
3. **Pixelate (Optional)**:
   - Adjust the pixelation slider (0 = off)
   - Click "👾 Apply Pixelation" to preview
4. **Save**: Choose format and click "💾 Save Result"

### Keyboard & Mouse Controls

- **Mouse Wheel**: Zoom in/out (when "Free Positioning" is enabled)
- **Left Click + Drag**: Pan image (when "Free Positioning" is enabled)
- **Reset Button**: Restore original image and reset all settings

### Tips & Tricks 💡

- **Smart Zoom**: The zoom function keeps the point under your cursor stationary, making it easy to zoom into specific areas
- **Non-destructive Workflow**: Pixelation is always applied to the cropped image, not the pixelated version, preventing quality loss
- **Live Preview**: The overlay shows exactly what will be cropped before you apply

## Project Structure


image2pixel/
├── main.py              # Application entry point and logic
├── gui.py               # GUI layout and widgets
├── display_image.py     # Custom image display widget
├── edit_image.py        # Crop transformation logic
├── pixel_transform.py   # Pixelation effect implementation
├── requirements.txt     # Python dependencies
└── README.md           # This file


## Technical Details

### Architecture

- **GUI Framework**: PyQt6 for cross-platform desktop interface
- **Image Processing**: Pillow (PIL) for image manipulation
- **Design Pattern**: Separation of concerns - GUI, logic, and image processing are modular

### Key Components

- **ImageDisplay**: Custom QLabel widget with interactive crop overlay
- **AppLogic**: Main application controller managing state and user interactions
- **Image Processing**: Efficient algorithms for crop calculation and pixelation

## Troubleshooting 🔧

### Common Issues

**Application won't start:**
- Ensure Python 3.8+ is installed: `python --version`
- Verify dependencies are installed: `pip list | grep -E "PyQt6|Pillow"`

**Image won't load:**
- Check file format is supported (PNG, JPG, JPEG, WebP, BMP)
- Verify file is not corrupted
- Check file permissions

**Pixelation not working:**
- Make sure you've applied crop first
- Try adjusting the slider value
- Check that the image is loaded

### Performance Tips

- For large images (>4000px), cropping first will improve pixelation speed
- WebP format offers best compression for saving
- PNG format preserves quality best for further editing

## Contributing 🤝

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Test on multiple platforms if possible

## Roadmap 🗺️

- [ ] Batch processing support
- [ ] Additional filters and effects
- [ ] Preset crop ratios (Instagram, Twitter, etc.)
- [ ] Undo/Redo functionality
- [ ] Command-line interface
- [ ] Drag-and-drop file support
- [ ] Recent files menu

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- PyQt6 framework for the excellent GUI toolkit
- Pillow team for powerful image processing capabilities
- All contributors and users of this project

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide detailed information about your problem (OS, Python version, error messages)

## Changelog

### Version 1.0.0 (Initial Release)
- Interactive image cropping with aspect ratios
- Pixelation effects
- Multi-format export
- Real-time preview
- Zoom and pan controls



Made with ❤️ by [Vadym Demianov https://github.com/VadymDem]