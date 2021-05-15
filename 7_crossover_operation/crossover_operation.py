import random, string
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QComboBox, \
    QPushButton, QLineEdit, QLabel, QSpinBox

#"""
UI_FILE = r"cc-ia-2020\7_crossover_operation\crossover_operation.ui"
"""
UI_FILE = "crossover_operation.ui"
#"""

global SIZE, IS_SIMPLE_CUT
SIZE = 10 # Padrão do tamanho dos genes
IS_SIMPLE_CUT = True # Padrão da seleção de crossover


def update_line_edit(mask, father_fill, mother_fill):
    """ Atualiza a mascara e a string dos pais de acordo com o tamanho """
    meta = ""
    if not IS_SIMPLE_CUT:
        meta = ">"

    father_line_edit.setMaxLength(SIZE)
    father_line_edit.setInputMask(meta + mask * SIZE)
    current_text = father_line_edit.text()
    father_line_edit.setText(current_text.ljust(SIZE, father_fill))

    mother_line_edit.setMaxLength(SIZE)
    mother_line_edit.setInputMask(meta + mask * SIZE)
    current_text = mother_line_edit.text()
    mother_line_edit.setText(current_text.ljust(SIZE, mother_fill))


def create_random_letters():
    """ Cria uma string aleatória de letras maiúsculas sem repetição """
    char_set = string.ascii_uppercase[:SIZE]
    return "".join(random.sample(char_set, SIZE))


def create_random_bin():
    """ Cria uma string aleatória de número binário """
    # Random de 2^SIZE começando em 0
    maxint = (2 ** SIZE) - 1
    rand_int = random.randint(0, maxint)
    rand_bin = bin(rand_int)
    # [2:] remove "0b" da string
    # zfill(SIZE) completa o lado esquerdo com zeros
    treated_rand_bin = str(rand_bin)[2:].zfill(SIZE)

    return treated_rand_bin


def fill_labels(offsprings):
    """ Coloca texto nas labels do Qt """
    son1_label_1.setText(offsprings[0])
    son1_label_2.setText(offsprings[1])
    son1_label_3.setText(offsprings[2])
    son2_label_1.setText(offsprings[3])
    son2_label_2.setText(offsprings[4])
    son2_label_3.setText(offsprings[5])


def on_random_pushbutton_clicked():
    """ Atualiza as strings de entrada dos pais ao clique do botão 'Aleatório' """
    if IS_SIMPLE_CUT:
        father_line_edit.setText(create_random_bin())
        mother_line_edit.setText(create_random_bin())
    else:
        father_line_edit.setText(create_random_letters())
        mother_line_edit.setText(create_random_letters())


def on_genes_spin_box_value_changed():
    """ Muda o tamanho exato dos genes e atualiza as strings de entrada """
    global SIZE
    SIZE = genes_spin_box.value()
    if IS_SIMPLE_CUT:
        update_line_edit("B", "0", "1")
    else:
        update_line_edit("A", "A", "B")


def on_cross_pushbutton_clicked():
    """ Inicia os processos de cruzamento """
    father = father_line_edit.text()
    mother = mother_line_edit.text()
    if IS_SIMPLE_CUT:
        offsprings = simple_cut_crossover(father, mother)
    else:
        offsprings = pmx_crossover(father, mother)

    fill_labels(offsprings)


def on_method_combobox_current_text_changed():
    """ Atualiza as informações na tela do Qt de acordo com o método de crossover """
    global IS_SIMPLE_CUT
    if method_combo_box.currentText() == "Corte Simples":
        IS_SIMPLE_CUT = True
    else:
        IS_SIMPLE_CUT = False
    empty_str = '', '', '', '', '', ''
    fill_labels(empty_str)
    on_genes_spin_box_value_changed()


def triple_split_string(child1, child2):
    """ Divide uma string em 3 partes iguais (ou quase) """
    small = SIZE // 3
    big = SIZE - small
    _p1 = slice(0, small)
    _p2 = slice(small, big)
    _p3 = slice(big, SIZE)

    return  child1[_p1], child1[_p2], child1[_p3], \
            child2[_p1], child2[_p2], child2[_p3]


def replace_repeated(child, aux, cut, subsize):
    """ Substitui os caracteres repetidos pelo corte pmx """
    child = list(child)
    for i in range(SIZE):
        if i >= cut and i < cut + subsize:
            continue
        count = 0
        char = child[i]
        for j in range(SIZE):
            if child[j] == char:
                count += 1
        if count > 1:
            new_char = "\0"
            find = False
            for j in range(subsize):
                new_char = aux[j]
                find = False
                for k in range(SIZE):
                    if child[k] == new_char:
                        find = True
                        break
                if not find:
                    break
            child[i] = new_char

    return "".join(child)


def pmx_crossover(father, mother):
    """ Faz o corte pmx de forma aleatória em subconjuntos """
    subsize = 3 # subconjunto do gene, padrão é 3
    cut = random.randint(0, SIZE - 1 * subsize)
    aux1 = father[cut : cut + subsize]
    aux2 = mother[cut : cut + subsize]
    child1 = mother.replace(aux2, aux1)
    child2 = father.replace(aux1, aux2)
    child1 = replace_repeated(child1, aux2, cut, subsize)
    child2 = replace_repeated(child2, aux1, cut, subsize)

    return triple_split_string(child1, child2)


def simple_cut_crossover(father, mother):
    """ Faz o corte simples de forma aleatória """
    cut = random.randint(0, SIZE - 1)
    child1 = father[:cut] + mother[cut:]
    child2 = mother[:cut] + father[cut:]
    return triple_split_string(child1, child2)


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
