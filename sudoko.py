import PyQt5  # For PyQt5
import kivy  # For Kivy

from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import random


class SudokuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Game")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()

    def initUI(self):
        # Main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Sudoku grid
        grid_layout = QGridLayout()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                cell = QLineEdit()
                cell.setFont(QFont("Arial", 18))
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(50, 50)
                cell.setStyleSheet(
                    "border: 1px solid black;" 
                    "background-color: white;" 
                    "color: black;"
                )
                cell.setMaxLength(1)
                grid_layout.addWidget(cell, i, j)
                self.cells[i][j] = cell

        main_layout.addLayout(grid_layout)

        # Buttons
        button_layout = QVBoxLayout()
        start_button = QPushButton("New Game")
        start_button.clicked.connect(self.start_new_game)
        button_layout.addWidget(start_button)

        check_button = QPushButton("Check Solution")
        check_button.clicked.connect(self.check_solution)
        button_layout.addWidget(check_button)

        main_layout.addLayout(button_layout)

    def start_new_game(self):
        # Generate a new puzzle and fill the grid
        puzzle = self.generate_puzzle()
        for i in range(9):
            for j in range(9):
                self.cells[i][j].setText(str(puzzle[i][j]) if puzzle[i][j] != 0 else "")
                self.cells[i][j].setReadOnly(puzzle[i][j] != 0)

    def generate_puzzle(self):
        # Example: Simple static puzzle for now
        return [[random.randint(1, 9) if random.random() < 0.3 else 0 for _ in range(9)] for _ in range(9)]

    def check_solution(self):
        # Validate the Sudoku grid
        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].text()
                if not value.isdigit() or int(value) not in range(1, 10):
                    self.cells[i][j].setStyleSheet("background-color: red;")
                    return
        print("Solution is valid!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec_())
