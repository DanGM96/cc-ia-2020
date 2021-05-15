from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QLabel, \
    QPushButton, QSpinBox, QComboBox

from hebb_rule import hebb_rule
from perceptron import perceptron

BIAS = 1 # Bias padrão utilizado nos algoritmos

def get_choice():
    """ Muda o nome da janela dinâmicamente """
    window.setWindowTitle("GUI - " + choice.currentText())

def get_sb(_object):
    """ Retorna os objetos QSpinBox """
    return window.findChild(QSpinBox, _object)

def get_lbl(_object):
    """ Retorna os objetos QLabel """
    return window.findChild(QLabel, _object)

def get_train_data():
    """ Organiza as entradas do usuário """
    train = []
    # Set 1
    train.append(get_sb("spinBox_in_1a").value()) # in a
    train.append(get_sb("spinBox_in_1b").value()) # in b
    train.append(get_sb("spinBox_out_1").value()) # out
    # Set 2
    train.append(get_sb("spinBox_in_2a").value()) # in a
    train.append(get_sb("spinBox_in_2b").value()) # in b
    train.append(get_sb("spinBox_out_2").value()) # out
    # Set 3
    train.append(get_sb("spinBox_in_3a").value()) # in a
    train.append(get_sb("spinBox_in_3b").value()) # in b
    train.append(get_sb("spinBox_out_3").value()) # out
    # Set 4
    train.append(get_sb("spinBox_in_4a").value()) # in a
    train.append(get_sb("spinBox_in_4b").value()) # in b
    train.append(get_sb("spinBox_out_4").value()) # out

    # Retorna um vetor de ([entradas], saida)
    return [([train[i], train[i + 1], BIAS], train[i + 2]) for i in range(0, len(train), 3)]

def sub(_string):
    """ Transforma string para substring utilizando html (aceito pelo Qt) """
    return f"<span style=' vertical-align:sub;'>{_string}</span>"

def start_trainning():
    """ Faz o treinamento de acordo com os inputs e outputs e mostra os pesos """
    data = get_train_data()
    chosen = choice.currentText()

    if chosen == "Hebb":
        weight = hebb_rule(data)
    elif chosen == "Perceptron":
        weight = perceptron(data)
    else:
        weight = "err"

    get_lbl("weightLabel_1").setText(f"W{sub('1')}: {weight[0]}")
    get_lbl("weightLabel_2").setText(f"W{sub('2')}: {weight[1]}")
    get_lbl("weightLabel_B").setText(f"W{sub('B')}: {weight[2]}")
    store(weight)

def process_weights(_input, _weight):
    """ Processa os pesos de acordo com o neurônio e seu modelo matemático """
    net = _weight[2] # Adiciona o bias primeiro
    for i in range(len(_input)):
        net += _input[i] * _weight[i] # Soma a multiplicação das entradas com os pesos

    # Função de transferência - Degrau Unitário
    if net <= 0:
        return -1
    return 1

def store(*values):
    """ Guarda valores de forma gambiarrística """
    store.values = values or store.values
    return store.values[0]

def start_running():
    """ Faz o teste de acordo com os inputs e mostra o resultado """
    # Input
    run_in = []
    run_in.append(get_sb("spinBox_run_a").value())
    run_in.append(get_sb("spinBox_run_b").value())

    weight = store()
    result = process_weights(run_in, weight)
    # Output
    get_lbl("outputLabel").setText(f"Output: {result}")

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    window = uic.loadUi(r"cc-ia-2020\5_gui_hebb_perceptron\hebb_perceptron.ui")
    store([0, 0, 0])

    # Escolha do algoritmo
    choice = window.findChild(QComboBox, "choiceComboBox")
    choice.activated.connect(get_choice)

    # Botão do trainning
    trainBtn = window.findChild(QPushButton, "trainButton")
    trained = trainBtn.clicked.connect(start_trainning)

    # Botão do running
    runBtn = window.findChild(QPushButton, "runButton")
    runBtn.clicked.connect(start_running)

    window.show()
    app.exec_()
