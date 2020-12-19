import random
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QComboBox, \
    QPushButton, QLineEdit, QLabel, QSpinBox

#"""
UI_FILE = r"ia-cc-2020-2-jordan\7_crossover_operation\crossover_operation.ui"
"""
UI_FILE = "crossover_operation.ui"
#"""

global SIZE
SIZE = 10 # Padrão do tamanho dos genes

def create_random_bin():
    """ Cria um novo gene binario de forma aleatória """
    # Random de 2^SIZE começando em 0
    maxint = (2 ** SIZE) - 1
    rand_int = random.randint(0, maxint)
    rand_bin = bin(rand_int)
    # [2:] remove "0b" da string
    # zfill(SIZE) completa o lado esquerdo com zeros
    treated_rand_bin = str(rand_bin)[2:].zfill(SIZE)
    return treated_rand_bin

def on_random_pushbutton_clicked():
    """  """
    father_line_edit.setText(create_random_bin())
    mother_line_edit.setText(create_random_bin())

def on_cross_pushbutton_clicked():
    """  """
    father = father_line_edit.text()
    mother = mother_line_edit.text()
    if method_combo_box.currentText() == "Corte Simples":
        offsprings = simple_cut_crossover(father, mother)
    else:
        offsprings = pmx_crossover()

    son1_label_1.setText(offsprings[0])
    son1_label_2.setText(offsprings[1])
    son1_label_3.setText(offsprings[2])
    son2_label_1.setText(offsprings[3])
    son2_label_2.setText(offsprings[4])
    son2_label_3.setText(offsprings[5])

def on_method_combobox_current_text_changed():
    """  """
    print('combo box changed')

def update_line_edit():
    """  """
    line_edit = [father_line_edit, mother_line_edit]
    for i in range(len(line_edit)):
        line_edit[i].setMaxLength(SIZE)
        line_edit[i].setInputMask("B" * SIZE)
        current_text = line_edit[i].text()
        line_edit[i].setText(current_text.zfill(SIZE))

def on_genes_spin_box_value_changed():
    """  """
    global SIZE
    SIZE = genes_spin_box.value()
    update_line_edit()

def pmx_crossover():
    """  """
    # Esta função está retornando 6 valores.
    # Ao criar o corpo da função você deve ordená-los de acordo com
    # as linhas 17 a 22 deste arquivo.
    return '','','','','',''

def simple_cut_crossover(father, mother):
    """  """
    cut = random.randint(0, SIZE - 1)
    child1 = father[:cut] + mother[cut:]
    child2 = mother[:cut] + father[cut:]

    small = SIZE // 3
    big = SIZE - small
    _p1 = slice(0, small)
    _p2 = slice(small, big)
    _p3 = slice(big, SIZE)

    return  child1[_p1], child1[_p2], child1[_p3], \
            child2[_p1], child2[_p2], child2[_p3]

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])

    # Loading widgets elements from ui file
    window = uic.loadUi(UI_FILE)
    window.show()

    # Getting widgets elements
    father_line_edit = window.findChild(QLineEdit, 'fatherLineEdit')
    mother_line_edit = window.findChild(QLineEdit, 'motherLineEdit')
    son1_label_1 = window.findChild(QLabel, 'son1Label1')
    son1_label_2 = window.findChild(QLabel, 'son1Label2')
    son1_label_3 = window.findChild(QLabel, 'son1Label3')
    son2_label_1 = window.findChild(QLabel, 'son2Label1')
    son2_label_2 = window.findChild(QLabel, 'son2Label2')
    son2_label_3 = window.findChild(QLabel, 'son2Label3')
    method_combo_box = window.findChild(QComboBox, 'methodComboBox')
    cross_push_button = window.findChild(QPushButton, 'crossPushButton')
    random_push_button = window.findChild(QPushButton, 'randomPushButton')
    genes_spin_box = window.findChild(QSpinBox, 'genesSpinBox')

    on_genes_spin_box_value_changed()

    # Connecting
    random_push_button.clicked.connect(on_random_pushbutton_clicked)
    cross_push_button.clicked.connect(on_cross_pushbutton_clicked)
    method_combo_box.currentTextChanged.connect(on_method_combobox_current_text_changed)
    genes_spin_box.valueChanged.connect(on_genes_spin_box_value_changed)

    app.exec_()
