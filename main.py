import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QScrollArea, QGridLayout, QFrame)
from PyQt5.QtCore import Qt
import numpy as np
from metadata_reader import ExifReader
import os


class FileMetadataWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Metadata Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Set dark theme for the main window
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QScrollArea {
                border: none;
            }
            QFrame {
                background-color: #363636;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # Create main widget with horizontal layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Create drop area
        self.create_drop_area()
        
        # Create metadata display area
        self.create_metadata_area()
        
        # Enable drop events
        self.setAcceptDrops(True)

    def create_drop_area(self):
        self.drop_label = QLabel("Drop files here\n(Supported image files)")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #666666;
                border-radius: 8px;
                padding: 30px;
                background-color: #363636;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                min-height: 100px;
            }
            QLabel:hover {
                background-color: #404040;
                border-color: #888888;
            }
        """)
        self.layout.addWidget(self.drop_label)

    def create_metadata_area(self):
        # Create scroll area for metadata
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #2b2b2b;")
        
        # Create widget to hold metadata
        self.metadata_widget = QWidget()
        self.metadata_layout = QVBoxLayout(self.metadata_widget)
        self.metadata_layout.setSpacing(15)
        
        self.scroll.setWidget(self.metadata_widget)
        self.layout.addWidget(self.scroll)

    def create_metadata_section(self, title, data, parent_layout):
        # Create frame for section
        section_frame = QFrame()
        section_frame.setStyleSheet("""
            QFrame {
                background-color: #363636;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # Create layout for section
        section_layout = QVBoxLayout(section_frame)
        
        # Add title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 5px;
            }
        """)
        section_layout.addWidget(title_label)
        
        # Create grid for metadata
        grid = QGridLayout()
        grid.setSpacing(10)
        row = 0
        
        # Add metadata items
        for key, value in data.items():
            print(key,value) #DEGBUGGING
            key_label = QLabel(f"{key}:")
            key_label.setStyleSheet("color: #bbbbbb; font-weight: bold;")
            value_label = QLabel(str(value))
            value_label.setWordWrap(True)
            value_label.setStyleSheet("color: #ffffff;")
            
            grid.addWidget(key_label, row, 0)
            grid.addWidget(value_label, row, 1)
            row += 1
        
        section_layout.addLayout(grid)
        parent_layout.addWidget(section_frame)

    def process_file(self, file_path):
        """
        Process the file and display its metadata
        """
        try:
            # Clear previous metadata
            for i in reversed(range(self.metadata_layout.count())): 
                self.metadata_layout.itemAt(i).widget().setParent(None)
            
            # Create ExifReader instance and get metadata
            reader = ExifReader(file_path)
            reader.load_image()
            
            # Display file info
            file_info = {
                "File Name": os.path.basename(file_path),
                "File Size": f"{os.path.getsize(file_path) / 1024:.2f} KB",
                "File Type": os.path.splitext(file_path)[1].upper()
            }
            self.create_metadata_section("File Information", file_info, self.metadata_layout)
            
            # Display GPS data if available
            if hasattr(reader, 'gps_data') and reader.gps_data:
                self.create_metadata_section("GPS Data", reader.gps_data, self.metadata_layout)
            else:
                print("ERROR: Reader didnt have gps_data")
            
            # Display EXIF data if available
            if hasattr(reader, 'exif_data') and reader.exif_data:
                self.create_metadata_section("EXIF Data", reader.exif_data, self.metadata_layout)
            else:
                print("ERROR: Reader didnt have exif_data")
                
            # Update drop label to show success
            self.drop_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #4CAF50;
                    border-radius: 8px;
                    padding: 30px;
                    background-color: #363636;
                    color: #4CAF50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 14px;
                }
            """)
            self.drop_label.setText("File processed successfully!\nDrop another file to view its metadata")
            
        except Exception as e:
            self.show_error(f"Error processing file: {str(e)}")

    def show_error(self, message):
        print(f"Error: {message}")
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ff5252;
                border-radius: 8px;
                padding: 30px;
                background-color: #363636;
                color: #ff5252;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        self.drop_label.setText(f"Error: {message}\nTry again with a different file")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.drop_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #888888;
                    border-radius: 8px;
                    padding: 30px;
                    background-color: #404040;
                    color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 14px;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #666666;
                border-radius: 8px;
                padding: 30px;
                background-color: #363636;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        self.drop_label.setText("Drop files here\n(Supported image files)")

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.process_file(files[0])

def main():
    # Enable High DPI display
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = FileMetadataWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()