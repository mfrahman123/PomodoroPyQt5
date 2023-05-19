import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QTimer, Qt
import pygame

pomodoro_duration = 60 # For demonstration purposes, reduced to 5 seconds
break_duration = 5  # For demonstration purposes, reduced to 5 seconds

class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout(self)  # Create a QVBoxLayout as the main layout

        self.timer_box = QLabel(self)  # Create a QLabel for the timer box
        self.timer_box.setStyleSheet("background-color: red")  # Set initial background color to red
        self.timer_box.setFixedSize(50, 50)  # Set the width and height of the colored box
        layout.addStretch()  # Add a stretchable space to push the timer box to the top
        layout.addWidget(self.timer_box, alignment=Qt.AlignHCenter)  # Center the timer box horizontally
        layout.addStretch()  # Add another stretchable space

        button_layout = QHBoxLayout()  # Create a QHBoxLayout for the buttons
        layout.addLayout(button_layout)  # Add the button layout to the main layout

        self.start_button = QPushButton("Start", self)  # Create the Start button
        self.start_button.clicked.connect(self.start_timer)  # Connect the button's clicked event to start_timer method
        button_layout.addWidget(self.start_button)  # Add the Start button to the button layout

        self.stop_button = QPushButton("Stop", self)  # Create the Stop button
        self.stop_button.clicked.connect(self.stop_timer)  # Connect the button's clicked event to stop_timer method
        button_layout.addWidget(self.stop_button)  # Add the Stop button to the button layout
        self.stop_button.hide()  # Hide the Stop button initially

        self.notification_label = QLabel(self)  # Create a QLabel for the notification label
        layout.addWidget(self.notification_label)  # Add the notification label to the layout

        self.pomodoro_timer = QTimer(self)  # Create a QTimer for the pomodoro timer
        self.pomodoro_timer.timeout.connect(self.on_pomodoro_timeout)  # Connect the timer's timeout event to on_pomodoro_timeout method

        self.break_timer = QTimer(self)  # Create a QTimer for the break timer
        self.break_timer.timeout.connect(self.on_break_timeout)  # Connect the timer's timeout event to on_break_timeout method

        pygame.mixer.init()  # Initialize the pygame mixer
        pygame.mixer.music.load("notification_sound.wav")  # Load the notification sound

    def start_timer(self):
        self.start_button.hide()  # Hide the Start button
        self.stop_button.show()  # Show the Stop button

        self.start_pomodoro()  # Start the pomodoro timer

    def start_pomodoro(self):
        self.timer_box.setStyleSheet("background-color: red")  # Set the timer box background color to red
        self.pomodoro_timer.start(pomodoro_duration * 1000)  # Start the pomodoro timer in milliseconds

    def on_pomodoro_timeout(self):
        self.pomodoro_timer.stop()  # Stop the pomodoro timer
        self.timer_box.setStyleSheet("background-color: green")  # Set the timer box background color to green
        pygame.mixer.music.play()  # Play the notification sound
        self.notification_label.setText("Pomodoro completed!")  # Set the notification label text
        self.break_timer.start(break_duration * 1000)  # Start the break timer in milliseconds

    def on_break_timeout(self):
        self.break_timer.stop()  # Stop the break timer
        self.timer_box.setStyleSheet("background-color: red")  # Set the timer box background color to red
        pygame.mixer.music.play()  # Play the notification sound
        self.notification_label.setText("Break completed!")  # Set the notification label text
        self.start_pomodoro()  # Start a new pomodoro

    def stop_timer(self):
        self.stop_button.hide()  # Hide the Stop button
        self.start_button.show()  # Show the Start button

        self.pomodoro_timer.stop()  # Stop the pomodoro timer
        self.break_timer.stop()  # Stop the break timer
        self.timer_box.setStyleSheet("background-color: red")  # Set the timer box background color to red
        self.notification_label.clear()  # Clear the notification label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer = PomodoroTimer()
    timer.show()
    sys.exit(app.exec_())
