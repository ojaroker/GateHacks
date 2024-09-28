from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QInputDialog

class UserInterface(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Resource Allocation Game")
        layout = QVBoxLayout()

        self.status_label = QLabel("Welcome to the Resource Allocation Game!")
        layout.addWidget(self.status_label)

        self.play_button = QPushButton("Play Round")
        self.play_button.clicked.connect(self.play_round)
        layout.addWidget(self.play_button)

        self.setLayout(layout)

    def play_round(self):
        """
        Play a round of the game and update the UI.
        """
        self.play_button.setEnabled(False)  # Disable button during processing

        # Get human allocations through a dialog
        human_allocations = self.get_human_allocations()
        if human_allocations:
            self.game.play_round(human_allocations)
        
        # Update UI based on the game's status
        self.update_ui()

        self.play_button.setEnabled(True)  # Re-enable button after processing

    def get_human_allocations(self):
        """
        Prompt the user for their allocations using a dialog.
        """
        allocations = []
        for j in range(len(self.game.success_probabilities)):
            allocation, ok = QInputDialog.getInt(self, f"Allocate Tokens", 
                                                  f"Allocate tokens to Project {j + 1} (1 token minimum):", 
                                                  value=1, min=1)
            if ok:
                allocations.append(allocation)
            else:
                return None  # User canceled the dialog

        return allocations

    def update_ui(self):
        if self.game.current_round >= 5 or self.game.check_single_player_left():
            self.show_final_scores()
            return

        self.status_label.setText(f"Round {self.game.current_round + 1} played.")

    def show_final_scores(self):
        scores = "\n".join(f"Player {i + 1}: {score} points" for i, score in enumerate(self.game.player_scores))
        QMessageBox.information(self, "Game Over", f"Final Scores:\n{scores}")
        self.close()  # Close the application after showing final scores
