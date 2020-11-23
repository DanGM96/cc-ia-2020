from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QLabel, \
    QPushButton, QSpinBox


def d_pouco(x):
    """ Calcula a curva de fuzzificação POUCO de Dinheiro """
    if x <= 30:
        return 1
    if 30 < x <= 50:
        return (50 - x) / 20
    if x > 50:
        return 0


def d_razoavel(x):
    """ Calcula a curva de fuzzificação RAZOAVEL de Dinheiro """
    if x < 30:
        return 0
    if 30 <= x < 50:
        return (x - 30) / 20
    if x == 50:
        return 1
    if 50 < x <= 70:
        return (70 - x) / 20
    if x > 70:
        return 0


def d_adequado(x):
    """ Calcula a curva de fuzzificação ADEQUADO de Dinheiro """
    if x < 50:
        return 0
    if 50 <= x < 70:
        return (x - 50) / 20
    if x >= 70:
        return 1


def p_insuficiente(x):
    """ Calcula a curva de fuzzificação INSUFICIENTE de Pessoal """
    if x <= 30:
        return 1
    if 30 < x <= 70:
        return (70 - x) / 40
    if x > 70:
        return 0


def p_satisfatorio(x):
    """ Calcula a curva de fuzzificação SATISFATORIO de Pessoal """
    if x < 30:
        return 0
    if 30 <= x < 70:
        return (x - 30) / 40
    if x >= 70:
        return 1


def r_baixo(x):
    """ Calcula a curva de fuzzificação BAIXO de Risco """
    if x <= 30:
        return 1
    if 30 < x <= 40:
        return (40 - x) / 10
    if x > 40:
        return 0


def r_medio(x):
    """ Calcula a curva de fuzzificação MEDIO de Risco """
    if x < 30:
        return 0
    if 30 <= x < 40:
        return (x - 30) / 10
    if 40 <= x <= 60:
        return 1
    if 60 < x <= 70:
        return (70 - x) / 10
    if x > 70:
        return 0


def r_alto(x):
    """ Calcula a curva de fuzzificação ALTO de Risco """
    if x < 60:
        return 0
    if 60 <= x < 70:
        return (x - 60) / 10
    if x >= 70:
        return 1


def center_of_gravity(ralto, rmedio, rbaixo):
    """ Calcula o centro de gravidade para determinarmos o risco """
    risk = list(range(5, 101, 5)) # Cria uma lista com as porcentagens de risco de 5 em 5
    cog = 0
    div = 0
    for _, r in enumerate(risk):
        alto = min(r_alto(r), ralto)
        medio = min(r_medio(r), rmedio)
        baixo = min(r_baixo(r), rbaixo)

        rmax = max(alto, medio, baixo)
        cog += r * rmax
        div += rmax

    return cog / div


def start_analysis():
    """ Função principal da Análise de Riscos """
    riskResult.setText("Analyising...")

    cost = costBox.value()
    personnel = personnelBox.value()

    dpouco = d_pouco(cost)
    drazoavel = d_razoavel(cost)
    dadequado = d_adequado(cost)
    pinsuficiente = p_insuficiente(personnel)
    psatisfatorio = p_satisfatorio(personnel)

    ralto1 = max(dpouco, pinsuficiente)
    ralto2 = min(dpouco, psatisfatorio)
    ralto = max(ralto1, ralto2)
    rmedio = min(drazoavel, psatisfatorio)
    rbaixo = min(dadequado, psatisfatorio)

    cog = center_of_gravity(ralto, rmedio, rbaixo)
    cogalto = r_alto(cog)
    cogmedio = r_medio(cog)
    cogbaixo = r_baixo(cog)
    cogmax = max(cogalto, cogmedio, cogbaixo)

    if cogmax == cogalto:
        risk = "High"
    elif cogmax == cogmedio:
        risk = "Medium"
    elif cogmax == cogbaixo:
        risk = "Low"

    riskResult.setText(f"Center of Gravity: {cog}\nThis project's risk is {risk}.")


def reset_analysis():
    """ Reinicia os padrões do programa """
    costBox.setValue(0)
    personnelBox.setValue(0)
    riskResult.setText("Press Analyse to determine a risk")


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])

    window = uic.loadUi(r"ia-cc-2020-2-jordan\2_logica_fuzzy\analise_de_risco.ui")

    # Entradas
    costBox = window.findChild(QSpinBox, "costSpinBox")
    personnelBox = window.findChild(QSpinBox, "personnelSpinBox")

    # Resultado
    riskResult = window.findChild(QLabel, "riskResultLabel")

    # Botoes
    analyseBtn = window.findChild(QPushButton, "analyseButton")
    analyseBtn.clicked.connect(start_analysis)

    resetBtn = window.findChild(QPushButton, "resetButton")
    resetBtn.clicked.connect(reset_analysis)

    window.show()
    app.exec_()
