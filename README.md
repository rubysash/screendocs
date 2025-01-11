# Screen Capture Tool v0.25

A powerful, lightweight screen capture utility built with PyQt5 that allows you to capture specific regions across multiple monitors with keyboard shortcuts and selection locking.

## Features

- Cross-monitor screen region selection
- Lock/unlock capture regions for repeated screenshots
- Keyboard shortcuts for all major functions
- Session-based naming with automatic timestamps
- Stay-on-top functionality
- Semi-transparent overlay with visual feedback
- Support for Windows 11 (primary) and other platforms

## Installation

1. Create and activate a virtual environment:
```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```python
pip install -r requirements.txt
```

## Usage

Launch the application by running:
```python
python main.py
```

### Basic Workflow

1. **Start Selection**: Click "Activate Selection" or press `Ctrl + Shift + S`
2. **Select Region**: Click and drag to select the desired capture area
3. **Name Session**: Enter a name for your capture session (allows letters, numbers, dash, dot)
4. **Lock Selection**: Press `Ctrl + L` to lock the current selection
5. **Capture Screen**: Press `Ctrl + P` or `Pause` to capture
6. **Multiple Captures**: Keep capturing with same selection using `Ctrl + P`
7. **Modify Selection**: Press `Ctrl + L` to unlock and make a new selection
8. **Exit**: Press `Ctrl + Q` to quit

### Keyboard Shortcuts

- `Ctrl + Shift + S`: Activate selection overlay
- `Ctrl + P` or `Pause`: Capture screen
- `Ctrl + L`: Lock/unlock selection
- `Ctrl + Q`: Quit application

### Visual Indicators

- **Red Border**: Active selection (unlocked)
- **Green Border**: Locked selection
- Selection area becomes click-through when locked
- Semi-transparent overlay indicates non-selected areas

### File Naming

Screenshots are saved automatically with the format:
```
{session-name}-{YYYY-MM-DD_HH-MM-SS}.png
```

## Use Cases

### Single Screenshot
1. Launch application
2. Press `Ctrl + Shift + S`
3. Select region
4. Enter session name (e.g., "documentation")
5. Press `Ctrl + P` to capture
6. Press `Ctrl + Q` to exit

### Repeated Screenshots of Same Region
1. Launch application
2. Press `Ctrl + Shift + S`
3. Select region
4. Enter session name (e.g., "tutorial")
5. Press `Ctrl + L` to lock selection
6. Press `Ctrl + P` for each capture needed
7. Press `Ctrl + L` to unlock when done
8. Press `Ctrl + Q` to exit

### Multiple Regions in One Session
1. Launch application
2. Press `Ctrl + Shift + S`
3. Select first region
4. Enter session name (e.g., "comparison")
5. Capture with `Ctrl + P`
6. Press `Ctrl + Shift + S` for new selection
7. Select new region
8. Capture with `Ctrl + P`
9. Repeat as needed
10. Press `Ctrl + Q` to exit

## Notes

- The tool remains on top of other windows for easy access
- Selection can span across multiple monitors
- Locked selections persist until manually unlocked
- Invalid session names will prompt for correction
- Each capture includes a timestamp for easy organization

## Requirements

- Python 3.12.3
- PyQt5 5.15.10
- Windows 11 (primary support)
- Virtual environment recommended

## License

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

### Contribution Guidelines

- Write clear, descriptive commit messages
- Follow existing code style and conventions
- Add comments for complex logic
- Update documentation as needed
- Add tests for new features
- Ensure all tests pass before submitting PR
