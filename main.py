import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class HelloWorldApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Hello World PyQt5")
        self.setGeometry(100, 100, 300, 200)

        # Création du layout principal
        layout = QVBoxLayout()

        # Ajout d'un label
        self.label = QLabel("Cliquez sur le bouton pour afficher Hello World", self)
        layout.addWidget(self.label)

        # Ajout d'un bouton
        button = QPushButton("Cliquez-moi", self)
        button.clicked.connect(self.show_message)
        layout.addWidget(button)

        # Ajout du layout au widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_message(self):
        self.label.setText("Hello World!")

# Point d'entrée principal
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Création de l'application Hello World
    window = HelloWorldApp()
    window.show()

    # Boucle principale de l'application
    sys.exit(app.exec_())
