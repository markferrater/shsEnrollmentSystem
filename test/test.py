import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QMessageBox
)
import pymysql


class SimpleBLOBUpload(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple BLOB Upload")
        self.setGeometry(100, 100, 400, 200)

        # Setup UI
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Instructions
        layout.addWidget(QLabel("Click button to upload a file directly to database:"))

        # Upload button
        self.btn = QPushButton("📤 Upload File to Database")
        self.btn.clicked.connect(self.upload_file)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.btn)

        # Status label
        self.status = QLabel("Ready")
        layout.addWidget(self.status)

    def upload_file(self):
        # Select file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Upload",
            "",
            "PDF Files (*.pdf);;Image Files (*.jpg *.jpeg *.png);;All Files (*)"
        )

        if not file_path:
            return

        try:
            # Read file as binary
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Connect to database
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='enrollment_database'
            )
            cursor = connection.cursor()

            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS simple_uploads (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    file_name VARCHAR(255),
                    file_data LONGBLOB,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Insert file
            sql = "INSERT INTO simple_uploads (file_name, file_data) VALUES (%s, %s)"
            cursor.execute(sql, (os.path.basename(file_path), file_data))
            connection.commit()
            connection.close()

            self.status.setText(f"✅ Uploaded: {os.path.basename(file_path)}")
            QMessageBox.information(self, "Success", "File uploaded to database!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Upload failed: {str(e)}")
            self.status.setText("❌ Upload failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleBLOBUpload()
    window.show()
    sys.exit(app.exec())