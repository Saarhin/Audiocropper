import sys
import os
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QWidget,
                               QVBoxLayout, QToolBar, QStackedWidget, QLineEdit, QHBoxLayout)
from PySide6.QtCore import QTimer, Qt, QTime
from PySide6.QtGui import QAction, QIcon

from audio_recorder import AudioRecorder

AUDIO_FOLDER = "recordings"

class RecordPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.record_button = QPushButton("Record")
        self.timer_label = QLabel("00:00")
        self.timer_label.setVisible(False)
        self.input_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter filename")
        self.save_button = QPushButton("Save")
        self.delete_button = QPushButton("Delete")

        self.name_input.setVisible(False)
        self.save_button.setVisible(False)
        self.delete_button.setVisible(False)

        self.input_layout.addWidget(self.name_input)
        self.input_layout.addWidget(self.save_button)
        self.input_layout.addWidget(self.delete_button)

        self.layout.addWidget(self.record_button)
        self.layout.addWidget(self.timer_label)
        self.layout.addLayout(self.input_layout)

        self.record_button.clicked.connect(self.toggle_recording)
        self.save_button.clicked.connect(self.save_recording)
        self.delete_button.clicked.connect(self.delete_recording)

        self.recording = False
        self.timer = QTimer()
        self.time = QTime(0, 0)
        self.timer.timeout.connect(self.update_timer)
        self.recorder = None

    def toggle_recording(self):
        if not self.recording:
            self.record_button.setText("Recording...")
            self.timer_label.setVisible(True)
            self.time = QTime(0, 0)
            self.timer_label.setText("00:00")
            self.timer.start(1000)
            self.recording = True
            self.recorder = AudioRecorder()
            self.recorder.start_recording()
        else:
            self.timer.stop()
            self.recording = False
            self.record_button.setVisible(False)
            self.timer_label.setVisible(False)
            self.name_input.setVisible(True)
            self.save_button.setVisible(True)
            self.delete_button.setVisible(True)
            self.recorder.stop_recording()

    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.timer_label.setText(self.time.toString("mm:ss"))

    def save_recording(self):
        name = self.name_input.text().strip()
        if name:
            os.makedirs(AUDIO_FOLDER, exist_ok=True)
            self.recorder.save(name)
        self.reset_ui()

    def delete_recording(self):
        self.reset_ui()

    def reset_ui(self):
        self.record_button.setText("Record")
        self.record_button.setVisible(True)
        self.name_input.setVisible(False)
        self.save_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.name_input.clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Recorder")
        self.setMinimumSize(600, 400)

        self.stack = QStackedWidget()
        self.record_page = RecordPage()
        self.stack.addWidget(self.record_page)

        # Placeholder for play page
        self.play_page = QLabel("Play Page (Coming Soon)", alignment=Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(self.play_page)

        self.setCentralWidget(self.stack)

        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        record_action = QAction(QIcon(), "Record", self)
        play_action = QAction(QIcon(), "Play", self)

        record_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.record_page))
        play_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.play_page))

        self.toolbar.addAction(record_action)
        self.toolbar.addAction(play_action)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: white;
            }
            QPushButton, QLineEdit {
                background-color: #2e2e2e;
                color: white;
                border: 1px solid #444;
                padding: 6px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
            QToolBar {
                background-color: #1e1e1e;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
