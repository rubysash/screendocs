"""
Overlay Module for Screen Capture Tool.

This module provides a transparent overlay window for selecting screen regions to capture.
It handles mouse events for selection, keyboard shortcuts for capture control,
and manages the capture process with session naming. The overlay can span multiple
monitors and supports locking the selection area.

The module provides functionality for:
- Creating a transparent overlay across all monitors
- Handling mouse-based selection of screen regions
- Managing capture session names
- Performing screen captures of selected regions
- Supporting locked/unlocked states for selection areas

Remember:  Qt uses camelCase, pep8 uses snake_case.
"""

import re
import platform
import datetime

from PyQt5 import QtWidgets, QtCore, QtGui


class Overlay(QtWidgets.QWidget):
    """
    A transparent overlay widget for selecting and capturing screen regions.

    This class creates a transparent window that spans all available monitors and
    allows users to select regions for screen capture. It handles mouse events,
    maintains selection state, and manages the capture process including session
    naming and file saving.

    Attributes:
        is_active (bool): Whether selection is currently active
        locked (bool): Whether the selection is locked
        selection_finalized (bool): Whether selection process is complete
        begin (QPoint): Starting point of selection
        end (QPoint): Ending point of selection
        control_window (ControlWindow): Reference to main control window
        session_name (str): Name of current capture session
        base_flags (Qt.WindowFlags): Base window flags for the overlay
    """

    def __init__(self, parent=None, control_window=None):
        """
        Initialize the overlay widget.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
            control_window (ControlWindow, optional): Reference to main control window.
                Defaults to None.
        """
        super(Overlay, self).__init__(parent)
        self.is_active = False
        self.locked = False
        self.selection_finalized = False
        self.begin = QtCore.QPoint(0, 0)
        self.end = QtCore.QPoint(0, 0)
        self.control_window = control_window
        self.session_name = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface components for the overlay.

        Sets up window flags, attributes, and geometry to create a transparent
        overlay that spans all available monitors. Configures window properties
        for proper display on different operating systems.
        """
        self.base_flags = (
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )
        self.setWindowFlags(self.base_flags)
        if platform.system() == "Windows":
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        else:
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

        # Get the QScreen objects for all monitors
        screens = QtWidgets.QApplication.screens()

        # Find the bounding rectangle that contains all screens
        min_x = min(screen.geometry().left() for screen in screens)
        min_y = min(screen.geometry().top() for screen in screens)
        max_x = max(screen.geometry().right() for screen in screens)
        max_y = max(screen.geometry().bottom() for screen in screens)

        # Create a rectangle that spans all monitors
        total_geometry = QtCore.QRect(min_x, min_y, max_x - min_x, max_y - min_y)

        self.setGeometry(total_geometry)
        self.setWindowOpacity(0.3)
        print(f"Overlay initialized with geometry: {total_geometry}")
        print(f"Number of screens detected: {len(screens)}")
        for i, screen in enumerate(screens):
            print(f"Screen {i} geometry: {screen.geometry()}")

    def sanitize_session_name(self, name):
        """
        Sanitize the session name to ensure it's file-system safe.

        Args:
            name (str): The proposed session name

        Returns:
            str or None: Sanitized name if valid, None if invalid
        """
        if not name:
            return None

        # Remove any characters that aren't alphanumeric, dash, or dot
        sanitized = re.sub(r"[^A-Za-z0-9\-\.]", "-", name)

        # Replace multiple consecutive dashes with a single dash
        sanitized = re.sub(r"-+", "-", sanitized)

        # Remove leading/trailing dashes and dots
        sanitized = sanitized.strip("-.")

        # Check if the name is just dots or empty after sanitization
        if not sanitized or all(c == "." for c in sanitized):
            return None

        return sanitized

    def prompt_session_name(self):
        """
        Prompt user for session name and store it.

        Returns:
            bool: True if valid name provided, False if cancelled
        """
        while self.session_name is None:
            name, ok = QtWidgets.QInputDialog.getText(
                self,
                "Session Name",
                "Enter a session name (letters, numbers, dash, dot only):",
            )
            if not ok:
                self.selection_finalized = False
                print("Selection cancelled - no session name provided")
                return False

            self.session_name = self.sanitize_session_name(name)
            if self.session_name is None:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please use only letters, numbers, dash (-) and dot (.). Name cannot be empty or just dots.",
                )
        return True

    def toggle_lock(self):
        """
        Toggle the locked state of the overlay.

        Switches between locked and unlocked states, updating the visual appearance
        and behavior of the overlay accordingly.
        """
        self.locked = not self.locked
        if not self.locked:
            self.session_name = None
            self.selection_finalized = False
        self.updateLockState()
        if not self.locked and self.control_window:
            self.control_window.activateWindow()
            self.control_window.raise_()
        print(f"Selection {'locked' if self.locked else 'unlocked'}.")

    def perform_capture(self):
        """
        Prepare and initiate the screen capture process.

        Calculates global screen coordinates and initiates the capture
        if selection is valid and session name is set.
        """
        print("Starting capture process...")
        begin_global = self.mapToGlobal(self.begin)
        end_global = self.mapToGlobal(self.end)

        # Calculate global screen coordinates
        x1, y1 = min(begin_global.x(), end_global.x()), min(
            begin_global.y(), end_global.y()
        )
        x2, y2 = max(begin_global.x(), end_global.x()), max(
            begin_global.y(), end_global.y()
        )
        width, height = x2 - x1, y2 - y1

        print(
            f"Selection coordinates - Begin: ({begin_global.x()}, {begin_global.y()}), End: ({end_global.x()}, {end_global.y()})"
        )
        print(f"Calculated region: ({x1}, {y1}, {width}, {height})")

        if width > 0 and height > 0 and self.session_name:
            self.hide()  # Hide overlay for capture
            # Add small delay to ensure overlay is fully hidden and capture variables
            captured_coords = (x1, y1, width, height)  # Capture variables for lambda
            QtCore.QTimer.singleShot(
                100, lambda coords=captured_coords: self.do_capture(*coords)
            )
        else:
            if not self.session_name:
                msg = "No session name set. Please unlock and create a new selection."
            else:
                msg = "No valid capture area selected. Please make a selection before capturing."

            QtWidgets.QMessageBox.warning(self, "Capture Error", msg)
            print("Invalid capture parameters")

    def delayed_capture(self):
        """
        Handle delayed capture timer execution.

        Executes the capture operation with stored coordinates after a delay.
        This method is triggered by a QTimer to ensure the overlay is fully hidden
        before capture.
        """
        if hasattr(self, "capture_coords"):
            x1, y1, width, height = self.capture_coords
            self.do_capture(x1, y1, width, height)

    def do_capture(self, x1, y1, width, height):
        """
        Perform the actual screen capture operation.

        Args:
            x1 (int): X-coordinate of the top-left corner
            y1 (int): Y-coordinate of the top-left corner
            width (int): Width of the capture area
            height (int): Height of the capture area

        Creates a screenshot of the specified region and saves it as a PNG file
        with timestamp in the filename. Shows error message if capture fails.
        """
        print(
            f"DEBUG: Starting capture with coordinates: x={x1}, y={y1}, width={width}, height={height}"
        )
        try:
            print(
                f"Starting capture with coordinates: x={x1}, y={y1}, width={width}, height={height}"
            )

            # Create a pixmap to hold the screenshot
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(0, x1, y1, width, height)

            # Save the screenshot with session name
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{self.session_name}-{timestamp}.png"
            screenshot.save(filename, "PNG")
            print(f"Captured at {timestamp} - Saved as {filename}")

        except Exception as e:
            print(f"Error during capture: {str(e)}")
            QtWidgets.QMessageBox.warning(
                self, "Capture Error", f"Failed to capture screenshot: {str(e)}"
            )
        finally:
            self.show()  # Always show overlay after capture attempt

    def capture_screen(self):
        """
        Initiate the screen capture process.

        Checks if selection is finalized before attempting capture.
        If selection is not finalized, logs an error message.
        """
        if self.selection_finalized:
            print("Attempting to capture...")
            self.perform_capture()
        else:
            print("No valid selection finalized, cannot capture.")

    def updateLockState(self):
        """
        Update the overlay's appearance and behavior based on lock state.

        When locked:
            - Increases opacity
            - Makes selection area transparent to mouse events
            - Allows clicks to pass through except in selection area
        When unlocked:
            - Returns to normal opacity
            - Clears masks
            - Enables interaction for new selections
        """
        if self.locked:
            self.setWindowOpacity(0.4)  # More visible when locked
            # Only make the selection area transparent to mouse events
            selection_rect = QtCore.QRect(self.begin, self.end).normalized()
            region = QtGui.QRegion(self.rect())
            region = region.subtracted(QtGui.QRegion(selection_rect))
            self.setMask(region)
            # Allow mouse events to pass through the overlay except in selection area
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            self.setWindowFlags(self.base_flags | QtCore.Qt.WindowTransparentForInput)
        else:
            self.setWindowOpacity(0.4)  # Normal visibility when unlocked
            # Clear any mask when unlocked
            self.clearMask()
            # Allow interaction for making new selections
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
            self.setWindowFlags(self.base_flags)
        self.show()

    def paintEvent(self, event):
        """
        Handle the painting of the overlay window.

        Args:
            event (QPaintEvent): The paint event

        Draws the semi-transparent background and the selection rectangle with
        appropriate border color based on lock state (green for locked, red for active).
        """
        super().paintEvent(event)
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # Entire widget size
        rect = self.rect()

        # Drawing the semi-transparent background
        qp.setBrush(
            QtGui.QBrush(QtGui.QColor(0, 0, 0, 51))
        )  # set opacity level, lower is more transparent
        qp.setPen(QtCore.Qt.NoPen)
        qp.drawRect(rect)

        # Define the selected area rectangle from begin to end points
        selection_rect = QtCore.QRect(self.begin, self.end).normalized()

        # Clear the selected area to make it fully transparent
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        qp.fillRect(selection_rect, QtCore.Qt.transparent)

        # Redraw the border around the selected area
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        if self.locked:
            qp.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0), 5))  # Green border for locked
        else:
            qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 5))  # Red border for active
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(selection_rect)

    def mousePressEvent(self, event):
        """
        Handle mouse press events for starting selection.

        Args:
            event (QMouseEvent): The mouse press event

        Initializes a new selection area at the pressed position and
        sets focus to the overlay window.
        """
        super().mousePressEvent(event)
        self.is_active = True
        self.selection_finalized = False  # Reset selection finalized on new press
        self.begin = event.pos()
        self.end = self.begin
        # Set focus during mouse selection
        self.activateWindow()
        self.setFocus(QtCore.Qt.MouseFocusReason)
        self.update()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for updating selection area.

        Args:
            event (QMouseEvent): The mouse move event

        Updates the end point of the selection area as the mouse moves,
        but only if selection is currently active.
        """
        super().mouseMoveEvent(event)
        if self.is_active:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for selection completion.

        Args:
            event (QMouseEvent): The mouse release event

        Finalizes the selection area and prompts for session name if not locked.
        """
        super().mouseReleaseEvent(event)
        if self.is_active:
            self.is_active = False
            self.selection_finalized = True
            self.capture_area = (self.begin, self.end)

            if not self.locked:
                self.prompt_session_name()

            if not self.locked and self.control_window:
                self.control_window.activateWindow()
                self.control_window.raise_()

            self.clearFocus()
            self.update()
            print(f"Mouse released at {self.end}, capture area set.")
