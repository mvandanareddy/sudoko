from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt
import sys
import random


class SudokuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Game")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()
        self.difficulty = "Easy"  # Default difficulty
        self.mistakes = 0  # Track mistakes
        self.max_mistakes = 5
        self.fixed_cells = set()  # Track fixed cells for highlighting
        self.start_new_game()

    def initUI(self):
        # Main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Sudoku grid
        grid_layout = QGridLayout()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        validator = QIntValidator(1, 9)  # Allow only numbers 1 to 9
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
                cell.setValidator(validator)
                cell.textChanged.connect(lambda text, x=i, y=j: self.on_cell_change(text, x, y))
                grid_layout.addWidget(cell, i, j)
                self.cells[i][j] = cell

        main_layout.addLayout(grid_layout)

        # Buttons for difficulty levels
        difficulty_layout = QHBoxLayout()
        easy_button = QPushButton("Easy")
        easy_button.clicked.connect(lambda: self.set_difficulty("Easy"))
        difficulty_layout.addWidget(easy_button)

        medium_button = QPushButton("Medium")
        medium_button.clicked.connect(lambda: self.set_difficulty("Medium"))
        difficulty_layout.addWidget(medium_button)

        hard_button = QPushButton("Hard")
        hard_button.clicked.connect(lambda: self.set_difficulty("Hard"))
        difficulty_layout.addWidget(hard_button)

        main_layout.addLayout(difficulty_layout)

        # Action button for new game
        start_button = QPushButton("New Game")
        start_button.clicked.connect(self.start_new_game)
        main_layout.addWidget(start_button)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.start_new_game()

    def start_new_game(self):
        self.mistakes = 0
        self.fixed_cells.clear()
        puzzle = self.generate_puzzle()
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if puzzle[i][j] != 0:
                    cell.setText(str(puzzle[i][j]))
                    cell.setReadOnly(True)
                    cell.setStyleSheet(
                        "border: 1px solid black;"
                        "background-color: lightgray;"
                        "color: black;"
                    )
                    self.fixed_cells.add((i, j))
                else:
                    cell.setText("")
                    cell.setReadOnly(False)
                    cell.setStyleSheet(
                        "border: 1px solid black;"
                        "background-color: white;"
                        "color: black;"
                    )

    def generate_puzzle(self):
        # Generate a complete, valid Sudoku board
        board = self.generate_complete_board()

        # Remove numbers based on difficulty
        difficulty_map = {"Easy": 40, "Medium": 30, "Hard": 20}
        cells_to_keep = difficulty_map[self.difficulty]

        # Randomly remove cells
        filled_positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(filled_positions)

        for i, j in filled_positions[cells_to_keep:]:
            board[i][j] = 0

        return board

    def generate_complete_board(self):
        def is_valid(board, row, col, num):
            for x in range(9):
                if board[row][x] == num or board[x][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if board[i][j] == num:
                        return False
            return True

        def solve(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        board = [[0] * 9 for _ in range(9)]
        solve(board)
        return board

    def on_cell_change(self, text, row, col):
        if text.isdigit() and int(text) in range(1, 10):
            self.cells[row][col].setStyleSheet(
                "border: 1px solid black;"
                "background-color: white;"
                "color: black;"
            )
            self.check_completion()
        elif text == "":
            return
        else:
            self.cells[row][col].setText("")  # Revert invalid input

    def check_completion(self):
        board = [[int(self.cells[i][j].text()) if self.cells[i][j].text().isdigit() else 0 for j in range(9)] for i in range(9)]

        if all(all(cell != 0 for cell in row) for row in board):
            if self.is_valid_solution(board):
                QMessageBox.information(self, "Congratulations!", "You solved the Sudoku! Well done!")
                self.start_new_game()
            else:
                QMessageBox.critical(self, "Game Over", "You made mistakes! Game Over.")
                self.start_new_game()

    def is_valid_solution(self, board):
        def is_unique(lst):
            nums = [x for x in lst if x != 0]
            return len(nums) == len(set(nums))

        for i in range(9):
            if not is_unique(board[i]) or not is_unique([board[j][i] for j in range(9)]):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [board[i][j] for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3)]
                if not is_unique(box):
                    return False

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec_())
