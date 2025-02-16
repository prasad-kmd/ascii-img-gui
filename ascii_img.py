import sys
import os
import subprocess
import webbrowser
import shutil
import tempfile
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QCheckBox, QGridLayout
)

APP_ICON = os.path.abspath("app_icon.ico")  # Get full path
EXE_NAME = "ascii-image-converter.exe"

class AsciiImageConverterGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ASCII Image Converter - GUI by PrasadM (c)2025")
        self.setGeometry(100, 100, 400, 350)
        self.setFixedSize(400, 350)
        self.setWindowIcon(QIcon(APP_ICON))

        layout = QVBoxLayout()

        self.label = QLabel("Select an image (JPEG JPG PNG BMP WEBP):")
        layout.addWidget(self.label)

        self.button_select = QPushButton("Browse")
        self.button_select.clicked.connect(self.select_image)
        layout.addWidget(self.button_select)

        self.selected_file_label = QLabel("No file selected")
        layout.addWidget(self.selected_file_label)

        self.options = {
            "--color": QCheckBox("Color"),
            "--grayscale": QCheckBox("Grayscale"),
            "--complex": QCheckBox("Complex characters"),
            "--full": QCheckBox("Full size"),
            "--negative": QCheckBox("Negative"),
            "--flipX": QCheckBox("Flip X"),
            "--flipY": QCheckBox("Flip Y")
        }

        grid_layout = QGridLayout()
        row, col = 0, 0
        for key, checkbox in self.options.items():
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        layout.addLayout(grid_layout)

        self.button_process = QPushButton("Process")
        self.button_process.clicked.connect(self.process_image)
        layout.addWidget(self.button_process)

        self.button_about = QPushButton("About")
        self.button_about.clicked.connect(self.show_about)
        layout.addWidget(self.button_about)

        self.setLayout(layout)
        self.image_path = ""
        self.extract_ascii_converter()

    def extract_ascii_converter(self):
        """Extracts ascii-image-converter.exe from the bundled PyInstaller EXE"""
        temp_dir = tempfile.gettempdir()
        self.exe_path = os.path.join(temp_dir, EXE_NAME)

        if not os.path.exists(self.exe_path):  # Extract only if not already extracted
            try:
                exe_source_path = os.path.join(sys._MEIPASS, EXE_NAME) if getattr(sys, 'frozen', False) else EXE_NAME
                shutil.copy(exe_source_path, self.exe_path)
                os.chmod(self.exe_path, 0o755)  # Make executable
            except Exception as e:
                print(f"Error extracting {EXE_NAME}: {e}")
                self.exe_path = None

    def select_image(self):
        file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an image", "", file_filter)
        if file_path:
            self.image_path = file_path
            self.selected_file_label.setText(f"Image Selected: {os.path.basename(file_path)}")

    def process_image(self):
        if not self.image_path:
            self.selected_file_label.setText("Image Error: No image selected!")
            return
        if not self.exe_path:
            self.selected_file_label.setText("EXE Error: ascii-image-converter.exe not found!")
            return

        output_dir = os.path.dirname(self.image_path)
        image_path_quoted = f'"{self.image_path}"'
        output_dir_quoted = f'"{output_dir}"'

        command = [self.exe_path, image_path_quoted]
        for flag, checkbox in self.options.items():
            if checkbox.isChecked():
                command.append(flag)

        command.extend(["--save-img", output_dir_quoted])

        try:
            subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.selected_file_label.setText(f"Output Image saved in: {output_dir}")
        except Exception as e:
            self.selected_file_label.setText(f"Error: {e}")

    def show_about(self):
        self.about_window = AboutUsWindow()
        self.about_window.show()

class AboutUsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About this GUI")
        self.setGeometry(200, 200, 300, 250)
        self.setFixedSize(400, 250)
        self.setWindowIcon(QIcon(APP_ICON))

        layout = QVBoxLayout()

        about_label = QLabel(
            "ASCII Image Converter - GUI by PrasadM\n"
            "Version: 1.0\n\n"
            "This is a GUI based on ascii-image-converter.exe.\n"
            "Thanks to TheZoraiz / ascii-image-converter on Github\n"
            "Built by Prasad Madhuranga @ 2025.02.07 \n"
            "Built using Python and PyQt6."
        )
        layout.addWidget(about_label)

        self.button_contribute = QPushButton("Contribute on GitHub")
        self.button_contribute.clicked.connect(lambda: self.open_link("https://github.com/prasad-kmd/ascii-img-gui"))
        layout.addWidget(self.button_contribute)

        self.button_docs = QPushButton("Website")
        self.button_docs.clicked.connect(lambda: self.open_link("https://prasad-kmd.blogspot.com/"))
        layout.addWidget(self.button_docs)

        self.button_website = QPushButton("Based Project : TheZoraiz/ascii-image-converter")
        self.button_website.clicked.connect(lambda: self.open_link("https://github.com/TheZoraiz/ascii-image-converter"))
        layout.addWidget(self.button_website)

        self.button_linkedin = QPushButton("LinkedIn")
        self.button_linkedin.clicked.connect(lambda: self.open_link("https://www.linkedin.com/in/prasad-madhuranga"))
        layout.addWidget(self.button_linkedin)

        self.setLayout(layout)

    def open_link(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(APP_ICON))
    window = AsciiImageConverterGUI()
    window.show()
    sys.exit(app.exec())
