from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QRadialGradient, QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import time

class RingProgressBar(QWidget):
    def __init__(self, parent=None):
        super(RingProgressBar, self).__init__(parent)
        self.value = 0
        self.specific_number = 0  # Add a member variable for specific number
        self.setFixedSize(100, 100)  # Set a fixed size for the ring progress bar
        self.picture = QPixmap("FILE_PATH_HERE/Atreggies.png").scaled(69, 53)  # UPDATE OWN FILE PATH FOR THE ICON, YOU CAN ALSO CHANGE THE ICON TO WHAT EVER PICTURE YOU WANT

    def setValue(self, value, specific_number):
        self.value = value
        self.specific_number = specific_number
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        if self.specific_number != "INACTIVE":
            # Draw the picture in the center
            picture_rect = self.picture.rect()
            picture_rect.moveCenter(QPoint(int(width / 2), int(height / 2)-5))
            painter.drawPixmap(picture_rect, self.picture)

        # Draw the background circle without any outline
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 200, 200, 0))  # Gray background color with full transparency
        painter.drawEllipse(0, 0, width, height)

        # Draw the background circle with the same gradient as the progress bar
        gradient = QRadialGradient(width / 2, height / 2, width / 2)
        gradient.setColorAt(1, QColor(100, 100, 100, 100))  # Outer color
        gradient.setColorAt(0.93, QColor(100, 100, 100, 100))  # Outer color
        gradient.setColorAt(0.92, QColor(0, 0, 0, 0))  # Outer color
        gradient.setColorAt(0, QColor(0, 0, 0, 0))    # Inner color (transparent)

        # Set the gradient as the brush for the background circle
        painter.setBrush(QBrush(gradient))

        # Draw the background circle without the little black lines
        painter.drawEllipse(0, 0, width, height)

        # Draw the progress ring with the same gradient
        gradient = QRadialGradient(width / 2, height / 2, width / 2)
        gradient.setColorAt(1, QColor(255, 200, 79, 255))  # Outer color
        gradient.setColorAt(0.93, QColor(255, 200, 79, 255))  # Outer color
        gradient.setColorAt(0.92, QColor(0, 0, 0, 0))  # Outer color
        gradient.setColorAt(0, QColor(0, 0, 0, 0))    # Inner color (transparent)

        # Set the gradient as the brush for the progress ring
        painter.setBrush(QBrush(gradient))

        # Calculate the progress span based on the percentage value
        progress_span = int((360 * self.value) / 100)

        # Adjust the starting angle to start from the bottom middle and draw clockwise
        start_angle = 270 * 16  # 270 degrees corresponds to the bottom middle

        # Draw the progress pie slice with the same gradient
        painter.setPen(Qt.NoPen)
        painter.drawPie(0, 0, width, height, start_angle, -progress_span * 16)

        # Draw specific_number in the middle of the progress bar if it's not "INACTIVE"
        if self.specific_number != "INACTIVE":
            painter.setPen(QColor(255, 255, 255))  # Set text color to white
            painter.setFont(QFont('Arial', 8))  # Set font for the text

            if self.specific_number == "0:00:00":  # Check if specific number is "0:00:00"
                text = "ARRIVED"
            else:
                text = str(self.specific_number)  # Convert to string if necessary
            
            text_rect = painter.fontMetrics().boundingRect(text)  # Get bounding rectangle for the text
            text_width = text_rect.width()  # Get width of the text
            text_height = text_rect.height()  # Get height of the text

            # Calculate the position to center the text vertically
            text_x = int((width - text_width) / 2)  # Convert to integer
            text_y = int((height + text_height) / 2) + 27  # Convert to integer
            painter.drawText(QPoint(int(text_x), int(text_y)), text)  # Convert to integer
        else:
            # Draw "INACTIVE" text in the middle of the progress bar
            painter.setPen(QColor(255, 255, 255))  # Set text color to white
            painter.setFont(QFont('Arial', 8))  # Set font for the text
            text = "INACTIVE"
            text_rect = painter.fontMetrics().boundingRect(text)  # Get bounding rectangle for the text
            text_width = text_rect.width()  # Get width of the text
            text_height = text_rect.height()  # Get height of the text

            # Calculate the position to center the text vertically
            text_x = int((width - text_width) / 2)  # Convert to integer
            text_y = int((height + text_height) / 2) + 27  # Convert to integer
            painter.drawText(QPoint(int(text_x), int(text_y)), text)  # Convert to integer




class DraggableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Rockets Tracker")
        self.setGeometry(1815, -245, 400, 150)  #CHANGE THE FIRST 2 NUMBERS HERE TO CHANGE WHERE THE WIDGET OPENS ON START UP

        # Make the window fully transparent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # Create labels to display the numbers, time left in seconds, and rocket durations
        self.labels = [QLabel("", self) for _ in range(3)]
        self.times_left_labels = [QLabel("", self) for _ in range(3)]
        self.duration_labels = [QLabel("", self) for _ in range(3)]
        self.progress_rings = [RingProgressBar(self) for _ in range(3)]

        # Create a container for each rocket slot
        container_layouts = []
        for i in range(3):
            container = QWidget(self)
            container_layout = QVBoxLayout(container)
            container_layout.addWidget(self.labels[i])
            container_layout.addWidget(self.times_left_labels[i])
            container_layout.addWidget(self.duration_labels[i])
            container_layout.addWidget(self.progress_rings[i])
            container.setLayout(container_layout)
            container_layouts.append(container)

        # Create the layout for the circular progress bars
        progress_layout = QHBoxLayout()
        for container in container_layouts:
            progress_layout.addWidget(container)

        # Create a refresh button
        self.refresh_button = QPushButton(self)
        self.refresh_button.setIcon(QIcon('FILE_PATH_HERE/Refresh.png'))  # CHANGE FILE PATH HERE
        self.refresh_button.setFixedSize(32, 32)  # Set the size of the refresh button
        self.refresh_button.setToolTip('Refresh Webpage')  # Set the tooltip text
        self.refresh_button.setStyleSheet(
            "QPushButton { border: none; background-color: transparent; }"  # Remove border and background color
        )
        self.refresh_button.clicked.connect(self.refresh_webpage)  # Connect the clicked signal to the refresh_webpage method

        # Connect hover events to change the icon
        self.refresh_button.enterEvent = self.refresh_button_hover_enter
        self.refresh_button.leaveEvent = self.refresh_button_hover_leave

        # Add the refresh button to the layout
        progress_layout.addWidget(self.refresh_button)

        # Set the layout for the widget
        self.setLayout(progress_layout)

        # Initialize Selenium webdriver with Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://wasmegg-carpet.netlify.app/rockets-tracker/')

        # Flags to track whether "Load Player Data" button has been clicked
        self.load_button_clicked = False

        # Flag to track whether a refresh is in progress
        self.refresh_in_progress = False

        # Call the function to update the numbers, time left, and print duration in seconds
        self.update_numbers()

    # Function to change the refresh button icon on hover enter
    def refresh_button_hover_enter(self, event):
        self.refresh_button.setIcon(QIcon('FILE_PATH_HERE/Refresh hover.png')) # CHANGE FILE PATH HERE

    # Function to change the refresh button icon on hover leave
    def refresh_button_hover_leave(self, event):
        self.refresh_button.setIcon(QIcon('FILE_PATH_HERE/Refresh.png')) # CHANGE FILE PATH HERE

    def update_numbers(self):
        try:
            # Wait for the input field to become available
            input_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "playerId"))
            )

            # Input the player ID if not clicked before
            if not self.load_button_clicked:
                input_field.send_keys("YOUR PLAYER ID") #PUT YOUR OWN PLAYER ID HERE

                # Click "Load Player Data" button and wait for the page to load
                load_button_xpath = "//button[contains(text(), 'Load Player Data')]"
                load_button = self.driver.find_element(By.XPATH, load_button_xpath)
                load_button.click()
                self.load_button_clicked = True

            # Wait for the specific number elements to become available
            specific_number_xpath = "//div[@class='mt-1 text-gray-700 text-sm font-medium tabular-nums']"
            specific_number_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, specific_number_xpath))
            )

            # Wait for the time left elements to become available
            time_left_xpath = "//div[@class='mt-1 text-gray-700 text-sm font-medium tabular-nums']"
            time_left_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, time_left_xpath))
            )

            # Wait for the duration elements to become available
            duration_xpath = "//div[contains(@class, 'text-gray-500') and contains(@class, 'text-xs') and contains(text(), 'Duration')]"
            duration_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, duration_xpath))
            )

            # Retrieve and update the displayed numbers, time left, and print duration in seconds
            for i, (label, time_left_label, duration_label, progress_ring) in enumerate(
                zip(self.labels, self.times_left_labels, self.duration_labels, self.progress_rings)
            ):
                if i < len(specific_number_elements):
                    specific_number = specific_number_elements[i].text
                    time_left = self.convert_time_to_seconds(time_left_elements[i].text)
                    duration_str = duration_elements[i].text.split(': ')[-1]
                    duration_seconds = self.convert_duration_to_seconds(duration_str)

                    if duration_seconds is not None:
                        progress_value = min(100, int((1 - time_left / duration_seconds) * 100))
                        progress_ring.setValue(progress_value, specific_number)
                    else:
                        progress_ring.setValue(0, specific_number)
                    
                else:
                    progress_ring.setValue(0, "INACTIVE")

        except Exception as e:
            print("Error:", e)

        # Schedule the function to run again after a certain delay (in milliseconds)
        QTimer.singleShot(1000, self.update_numbers)

    def refresh_webpage(self):
        try:
            # Check if the refresh button has been clicked recently
            if not self.refresh_in_progress:
                # Set the flag to prevent multiple clicks
                self.refresh_in_progress = True

                # Execute a script to simulate a refresh
                self.driver.refresh()

                # Wait for a short time after the refresh
                time.sleep(3)

                # Reset the flag to allow the refresh button to be clicked again
                self.refresh_in_progress = False

        except Exception as e:
            print("Error during refresh:", e)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    @staticmethod
    def convert_time_to_seconds(time_str):
        # Convert time to seconds based on different formats
        components = [int(x) for x in time_str.split(':')]

        if len(components) == 1:  # SS format
            return components[0]
        elif len(components) == 2:  # MM:SS format
            return components[0] * 60 + components[1]
        elif len(components) == 3:  # HH:MM:SS format
            return components[0] * 3600 + components[1] * 60 + components[2]
        elif len(components) == 4:  # D:HH:MM:SS format
            return components[0] * 86400 + components[1] * 3600 + components[2] * 60 + components[3]

    @staticmethod
    def convert_duration_to_seconds(duration_str):
        try:
            # Convert rocket duration to seconds based on different formats
            if 'd' in duration_str:
                components = duration_str.split('d')
                days = int(components[0])
                time_components = components[1].split('h')
            else:
                days = 0
                time_components = duration_str.split('h')

            if len(time_components) == 2:
                hours = int(time_components[0])
                minutes = int(time_components[1].replace('m', ''))
            else:
                hours = int(time_components[0].replace('h', ''))
                minutes = 0

            return days * 86400 + hours * 3600 + minutes * 60
        except ValueError:
            print("Error converting duration to seconds:", duration_str)
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = DraggableWidget()
    widget.show()

    sys.exit(app.exec_())
