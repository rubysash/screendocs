"""
Control window module for the Screen Capture Tool application.
Provides the main user interface controls for screen capture functionality.
"""

# pylint: disable=no-member
from PyQt5 import QtWidgets, QtCore
from overlay import Overlay

VERSION = 0.25

class ControlWindow(QtWidgets.QWidget):
    """
    Main control window class that provides the user interface for the screen capture tool.
    Contains buttons for activating selection, capturing screen, locking/unlocking selection,
    and quitting the application.
    """

    def __init__(self):
        """Initialize the control window with default settings."""
        super().__init__()
        self.overlay = None  # Initialize with no overlay
        self.init_ui()

    def init_ui(self):
        """Initialize and setup the user interface components."""
        self.setWindowTitle(f"Screen Capture Tool v{VERSION}")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(400, 200)
        layout = QtWidgets.QVBoxLayout(self)

        # Create and configure buttons
        self._setup_buttons(layout)

    def _setup_buttons(self, layout):
        """Setup all control buttons with their respective configurations."""
        buttons = [
            ("Activate Selection (Ctrl + Shift + S)", self.show_overlays),
            ("Capture Screen (Pause/Ctrl + P)", self.trigger_capture),
            ("Lock/Unlock Selection (Ctrl + L)", self.toggle_overlay_lock),
            ("Quit (Ctrl + Q)", QtWidgets.QApplication.quit)
        ]

        for text, callback in buttons:
            button = QtWidgets.QPushButton(text, self)
            button.clicked.connect(callback)
            layout.addWidget(button)

    def show_overlays(self):
        """Show the overlay for screen capture selection."""
        if not self.overlay:
            self.overlay = Overlay(control_window=self)
            self.overlay.show()
            print("Overlay initialized to span all monitors")
        else:
            self.overlay.show()

    def toggle_overlay_lock(self):
        """Toggle the locked state of the overlay."""
        if self.overlay:
            self.overlay.toggle_lock()

    def trigger_capture(self):
        """Trigger the screen capture if a valid selection exists."""
        if self.overlay and self.overlay.selection_finalized:
            self.overlay.capture_screen()
        else:
            print("No valid selection or overlay not created")
