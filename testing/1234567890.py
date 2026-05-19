import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class StudentPieChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Result Pie Chart")
        self.resize(500, 500)

        main_layout = QVBoxLayout()

        # ----- Input Fields -----
        input_layout = QHBoxLayout()

        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Total Students")

        self.passed_input = QLineEdit()
        self.passed_input.setPlaceholderText("Passed")

        self.failed_input = QLineEdit()
        self.failed_input.setPlaceholderText("Failed")

        input_layout.addWidget(self.total_input)
        input_layout.addWidget(self.passed_input)
        input_layout.addWidget(self.failed_input)

        # ----- Button -----
        self.update_btn = QPushButton("Update Pie Chart")
        self.update_btn.clicked.connect(self.update_chart)

        # ----- Matplotlib Figure -----
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Add widgets to main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.update_btn)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def update_chart(self):
        try:
            total = int(self.total_input.text())
            passed = int(self.passed_input.text())
            failed = int(self.failed_input.text())

            if passed + failed != total:
                QMessageBox.warning(
                    self,
                    "Input Error",
                    "Passed + Failed must equal Total Students"
                )
                return

            self.ax.clear()

            labels = ['Passed', 'Failed']
            sizes = [passed, failed]

            self.ax.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                startangle=90
            )
            self.ax.set_title("Student Results")

            self.canvas.draw()

        except ValueError:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid numbers"
            )


app = QApplication(sys.argv)
window = StudentPieChart()
window.show()
sys.exit(app.exec())
