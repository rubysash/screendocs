"""
Screen Capture Utility in Python
A Qt-based utility for capturing screen regions with keyboard shortcuts.

The application provides functionality to:
1. Activate Selection
2. Drag mouse over desired area
3. Use CTRL + L to lock selection
4. Use OS normally and CTRL + P for screen capture
5. Use CTRL + L again to lock/move selection
6. Use CTRL + Q to quit

TODO:
- Select capture anywhere instead of 3 separate capture areas
- Add Keyword for generating filenames based on subject + time vs time
"""

import sys
from PyQt5 import QtWidgets, QtGui
from control_window import ControlWindow

def setup_shortcuts(window):
    """
    Configure keyboard shortcuts for the application.

    Args:
        window (ControlWindow): The main window instance to which shortcuts will be added.

    Shortcuts configured:
        - Ctrl+Shift+S: Show overlay for selection
        - Pause/Ctrl+P: Trigger screen capture
        - Ctrl+L: Toggle overlay lock
        - Ctrl+Q: Quit application
    """
    # Define shortcuts
    QtWidgets.QShortcut(
        QtGui.QKeySequence("Ctrl+Shift+S"), window, activated=window.show_overlays
    )
    QtWidgets.QShortcut(
        QtGui.QKeySequence("Pause"), window, activated=window.trigger_capture
    )
    QtWidgets.QShortcut(
        QtGui.QKeySequence("Ctrl+P"), window, activated=window.trigger_capture
    )
    QtWidgets.QShortcut(
        QtGui.QKeySequence("Ctrl+L"), window, activated=window.toggle_overlay_lock
    )
    QtWidgets.QShortcut(
        QtGui.QKeySequence("Ctrl+Q"), window, activated=QtWidgets.QApplication.quit
    )

def main():
    """
    Initialize and launch the screen capture application.
    
    Creates the main QApplication instance, sets up the control window,
    configures keyboard shortcuts, and starts the application event loop.
    
    Returns:
        int: Application exit code
    """
    app = QtWidgets.QApplication(sys.argv)
    control_window = ControlWindow()
    setup_shortcuts(control_window)
    control_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()