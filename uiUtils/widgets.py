from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

def constr_label(text, css= ""):
    label= QLabel(text)
    label.setStyleSheet(css)
    return label

def constr_hbox():
    w= QWidget()
    hb= QHBoxLayout(w)
    return w, hb
