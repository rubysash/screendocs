import sys
import platform
from PyQt5 import QtWidgets, QtCore, QtGui
import pyautogui
import datetime

VERSION = 0.24


"""
Screen Capture Utility in Python
1. Activate Selection
2. Drag mouse over area you want
3. CTRL + L to lock selection
4. use OS as normal and CTRL + P when you want a screen capture
5. CTRL + L again to lock/move selection
6. CTRL + Q to quit.


TODO:
select capture anywhere instead of 3 separate capture areas.

Work around is to put area you want on the screen where captures work

Add Keyword so I can generate filenames based on subject + time vs time

"""


class Overlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.is_active = False
        self.locked = False
        self.selection_finalized = False
        self.begin = QtCore.QPoint(0, 0)
        self.end = QtCore.QPoint(0, 0)
        self.initUI()

    def initUI(self):
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

        # Span the overlay across all monitors
        virtual_desktop = QtWidgets.QApplication.desktop().screenGeometry()
        self.setGeometry(virtual_desktop)
        self.setWindowOpacity(0.3)  # Slightly visible for interaction
        print("Overlay initialized to span all monitors")

    def updateLockState(self):
        if self.locked:
            self.setWindowOpacity(0.4)  # More visible when locked
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            self.setWindowFlags(self.base_flags | QtCore.Qt.WindowTransparentForInput)
        else:
            self.setWindowOpacity(0.4)  # Normal visibility when unlocked
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
            self.setWindowFlags(self.base_flags)
        self.show()

    def paintEvent(self, event):
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
        super().mousePressEvent(event)
        self.is_active = True
        self.selection_finalized = False  # Reset selection finalized on new press
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.is_active:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.is_active:
            self.is_active = False
            self.selection_finalized = True  # Set selection as finalized
            self.capture_area = (self.begin, self.end)
            self.update()
            print(f"Mouse released at {self.end}, capture area set.")

    def toggle_lock(self):
        self.locked = not self.locked
        self.updateLockState()
        print(f"Selection {'locked' if self.locked else 'unlocked'}.")

    def capture_screen(self):
        if self.selection_finalized:
            print("Attempting to capture...")
            self.perform_capture()
        else:
            print("No valid selection finalized, cannot capture.")

    def perform_capture(self):
        print("Starting capture process...")
        begin_global = self.mapToGlobal(self.begin)
        end_global = self.mapToGlobal(self.end)
        x1, y1 = min(begin_global.x(), end_global.x()), min(
            begin_global.y(), end_global.y()
        )
        x2, y2 = max(begin_global.x(), end_global.x()), max(
            begin_global.y(), end_global.y()
        )
        width, height = x2 - x1, y2 - y1

        print(f"Calculated region: ({x1}, {y1}, {width}, {height})")

        if width > 0 and height > 0:
            self.hide()  # Hide overlay for capture
            QtCore.QTimer.singleShot(
                100, lambda: self.do_capture(x1, y1, width, height)
            )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Capture Error",
                "No valid capture area selected. Please make a selection before capturing.",
            )
            print("Invalid dimensions for capture: width or height are zero.")

    def do_capture(self, x1, y1, width, height):
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot.save(f"screen_capture_{timestamp}.png")
        print(f"Captured at {timestamp}")
        self.show()  # Show overlay after capture


class ControlWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.overlay = None  # Initialize with no overlay
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Screen Capture Tool v{VERSION}")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(400, 200)
        layout = QtWidgets.QVBoxLayout(self)

        self.activate_button = QtWidgets.QPushButton(
            "Activate Selection (Ctrl + Shift + S)", self
        )
        self.activate_button.clicked.connect(self.show_overlays)
        layout.addWidget(self.activate_button)

        self.capture_button = QtWidgets.QPushButton(
            "Capture Screen (Pause/Ctrl + P)", self
        )
        self.capture_button.clicked.connect(self.trigger_capture)
        layout.addWidget(self.capture_button)

        self.lock_button = QtWidgets.QPushButton(
            "Lock/Unlock Selection (Ctrl + L)", self
        )
        self.lock_button.clicked.connect(self.toggle_overlay_lock)
        layout.addWidget(self.lock_button)

        self.quit_button = QtWidgets.QPushButton("Quit (Ctrl + Q)", self)
        self.quit_button.clicked.connect(QtWidgets.QApplication.quit)
        layout.addWidget(self.quit_button)

    def show_overlays(self):
        if not self.overlay:  # Create the overlay if it doesn't exist
            self.overlay = Overlay(self)
            self.overlay.show()
            print("Overlay initialized to span all monitors")
        else:
            self.overlay.show()  # If already created, just show it

    def toggle_overlay_lock(self):
        if self.overlay:
            self.overlay.toggle_lock()

    def trigger_capture(self):
        if self.overlay and self.overlay.selection_finalized:
            self.overlay.capture_screen()
        else:
            print("No valid selection or overlay not created")


def setup_shortcuts(window):
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    control_window = ControlWindow()
    setup_shortcuts(control_window)
    control_window.show()
    sys.exit(app.exec_())
