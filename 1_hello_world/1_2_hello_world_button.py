# realizando as importações necessárias
from PyQt5.QtWidgets import QApplication, QPushButton


def say_hello():
    print("Botão clicado: Hello World!")


if __name__ == "__main__":
    # Criando a janela da aplicação
    app = QApplication([])

    # Criando o botão
    button = QPushButton("Click me")
    button.clicked.connect(say_hello)
    button.show()

    # Executando a janela
    app.exec_()
