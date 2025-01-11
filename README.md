# Screen Capture Tool v0.25

A powerful, lightweight screen capture utility built with PyQt5 that allows you to capture specific regions across multiple monitors with keyboard shortcuts and selection locking.

Better than other tools because it saves the screens with a session name, on the selection you chose.   Easy to have time stamped files relating to a specific session, great for documentation.

Wrote because manually clicking capture over and over and redrawing the area you are capturing (such as during a presentation) is tedious.   This allows you to hotkey the capture on a specific section as often as needed and to continue using your computer like normal until ready for another capture.   It's great for taking notes when you are being trained.

It saves images, not video, so actual storage space is tiny.

## Features

- Cross-monitor screen region selection, multiple monitors are ok to select if you desire.
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

Launch the application from environment by running:
```python
python main.py
```
or run the `start.bat` as a shortcut from anywhere to load the venv for you.

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

## Todo
- Add timed capture so popup menus on other focus can be captured too.

## Requirements

- Python 3.12.3
- PyQt5 5.15.10
- Windows 11 (primary support)
- Virtual environment recommended

## License

GNU General Public License v3.0
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
Note: This software uses PyQt5, which is licensed under GPL v3. As such,
any distribution of this software must also comply with the GPL v3 license.

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
