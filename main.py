#!/bin/python3

import random
import socket
import sys
import os
import subprocess
import multiprocessing

from os import path
from NekoMimi import utils as nm
from PyQt6.QtGui import QAction, QFontDatabase, QIcon, QPixmap
from uiUtils import widgets
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QDialog, QHBoxLayout, QLineEdit, QMenu, QMenuBar, QPushButton, QScrollArea, QSplashScreen, QVBoxLayout, QWidget, QMainWindow, QTextEdit, QSystemTrayIcon, QStackedWidget

__version__= '1.0.0'
__debug_f__= True
DIRECTORY= f"{subprocess.getoutput('echo $HOME')}/.config/NekoConnect"

def create_conf(password: str):
    try:
        os.mkdir(DIRECTORY)
    except Exception:
        pass
    nm.write(f"password= {password}\nport= 10390", DIRECTORY+"/nc.conf")

def save_conf(attrs):
    try:
        os.mkdir(DIRECTORY)
    except Exception:
        pass
    nm.write(f"password= {attrs['pass']}\nport= {attrs['port']}", DIRECTORY+"/nc.conf")

def generate_sources():
    try:
        os.mkdir(f"{subprocess.getoutput('echo $HOME')}/.local/share/NekoConnect")
        os.mkdir(f"{subprocess.getoutput('echo $HOME')}/.local/share/NekoConnect/plugins")
    except Exception:
        pass
    nm.write("src nekomimi.tilde.team/API/v4 main", DIRECTORY+"/repo.list")

def load_conf():
    data= nm.read(DIRECTORY+"/nc.conf")
    lines= data.split("\n")
    attrs= {'pass' : '', 'port' : 0}
    for line in lines:
        if line.startswith("password= "):
            attrs["pass"]= line.split("password= ", 1)[1]

        if line.startswith("port= "):
            try:
                attrs["port"]= int(line.split("port= ", 1)[1])
            except Exception:
                print("port malformed, fix config")
                exit(1)

    if attrs["pass"] == '':
        print("no password in config, fix config")
        exit(1)

    if attrs["port"] == 0:
        print("no port in config, fix config")
        exit(1)

    return attrs

def randStr()-> str:
    base= "123456abcedfXYZQKS7890!#?&$"
    git= ""
    for i in range(6):
        if i == 3:
            git= git + base[random.randint(20, len(base)-1)]
        else:
            git= git + base[random.randint(0, len(base)-1)]

    return git

def crypt(inp: str, salt: str, passwd: str)-> str:
    wp= salt+passwd
    table_let= "abcdefghijklmnopqrstuvwxyz"
    table_num= "1234567890"
    table_upp= table_let.upper()
    table_sym= "~!@#$%^&*()_+-=[]{};':\",.<>/?\\|`"
    table= table_let+table_num+table_upp+table_sym
    objects= []
    onjects =[]
    i= 0

    for c in inp:
        j= 0
        if not c in table:
            onjects.append(127)
            continue

        for x in table:
            if x == c:
                onjects.append(j)

            j= j + 1


    for c in wp:
        j= 0
        if not c in table:
            objects.append(127)
            continue

        for x in table:
            if x == c:
                objects.append(j)

            j= j + 1

    for o in onjects:
        onjects[i]= o + objects[i]
        i= i + 1

    table= table + table_sym + table + table_upp + table_sym + table_upp + table + table + "uwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwu"
    string_of_doom= ""
    for w in onjects:
        string_of_doom= string_of_doom + table[w]

    return string_of_doom

class initUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NekoConnect")
        self.setFixedSize(280, 100)
        layout= QVBoxLayout()
        self.greeter= widgets.constr_label("First run, we are setting up NekoConnect")
        self.info= widgets.constr_label("Please create a password for NekoConnect:")
        self.input= QLineEdit()
        self.submit= QPushButton()
        self.submit.setText("Done")
        self.submit.clicked.connect(self.input_sub)
        self.inp_w= QWidget()
        self.sider= QHBoxLayout(self.inp_w)
        self.sider.addWidget(self.input)
        self.sider.addWidget(self.submit)
        layout.addWidget(self.greeter)
        layout.addWidget(self.info)
        layout.addWidget(self.inp_w)

        self.setLayout(layout)

    def input_sub(self):
        passwd= self.input.text()
        create_conf(passwd)
        self.destroy(True)
        self.accept()

class UI(QMainWindow):
    def __init__(self)-> None:
        super().__init__()
        self.setWindowTitle("NekoConnect")
        self.setFixedSize(480, 380)
        self.TNF= QFontDatabase.addApplicationFont("./assets/TerminessNerdFontMono-Regular.ttf")
        self.HNF= QFontDatabase.addApplicationFont("./assets/HurmitNerdFontMono-Regular.otf")
        self.TFF= QFontDatabase.applicationFontFamilies(self.TNF)[0]
        self.HFF= QFontDatabase.applicationFontFamilies(self.HNF)[0]
        self.setStyleSheet(nm.read("./stylesheets/body.css")+f"font-family: {self.HFF};")
        self.console_line= 1
        self.warns= 0
        self.errors= 0
        self.stack= QStackedWidget()
        self.console_output = QTextEdit()
        self.warn_l= widgets.constr_label(f" {str(self.warns)}")
        self.err_l= widgets.constr_label(f" {str(self.errors)}")
        if not path.exists(DIRECTORY+"/nc.conf"):
            init_ui= initUI()
            init_ui.exec()

        self.attrs= load_conf()
        self.create_ui()

        self.server= Server(self.attrs["port"], self.attrs["pass"], self.log, self.warn, self.error, self.debug)
        self.server.init()

        self.globalMenu= self.menuBar()
        self.gm_constr()

        self.tray= QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("./assets/NekoConnR.png"))
        self.tray.setContextMenu(self.trayMenu())
        self.tray.setVisible(True)
        self.tray.activated.connect(self.trayToggle)

        self.setWindowIcon(QIcon("./assets/NekoConnect.png"))
        self.setWindowIconText("NekoConnect")
        self.setWindowFlags(
                Qt.WindowType.Window |
                Qt.WindowType.CustomizeWindowHint |
                Qt.WindowType.FramelessWindowHint
                )
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.initial_pos= None

        self.show()

    def mousePressEvent(self, event): #type: ignore
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event): #type: ignore
        if self.initial_pos is not None:
            if event.pos().y() < 50:
                delta = event.position().toPoint() - self.initial_pos
                self.window().move( #type: ignore
                    self.window().x() + delta.x(), #type: ignore
                    self.window().y() + delta.y(), #type: ignore
                )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event): #type: ignore
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def gm_constr(self):
        file= self.globalMenu.addMenu("File") #type: ignore

        exit_action= QAction("exit", self)
        exit_action.triggered.connect(self.quit)
        file.addAction(exit_action) #type: ignore

    def quit(self):
        if self.server.status():
            self.server.stop()
        self.tray.hide()
        sys.exit(0)

    def log_callout(self):
        self.debug("opening logs")
        self.stack.setCurrentIndex(0)

    def plug_callout(self):
        self.debug("opening plugins")
        self.stack.setCurrentIndex(1)

    def sett_callout(self):
        self.debug("opening settings")
        self.stack.setCurrentIndex(2)

    def nav_constr(self):
        nav= QWidget()
        wider= QHBoxLayout(nav)
        b_w= QWidget()
        i_w= QWidget()
        button_h= QHBoxLayout(b_w)
        info_h= QHBoxLayout(i_w)

        log_b= QPushButton()
        plug_b= QPushButton()
        settings_b= QPushButton()
        spacer= widgets.constr_label(" ")
        spacer.setFixedWidth(50)
        log_b.setText("")
        plug_b.setText("")
        settings_b.setText("󰢻")
        button_h.addWidget(log_b)
        button_h.addWidget(plug_b)
        button_h.addWidget(settings_b)
        button_h.addWidget(spacer)
        log_b.clicked.connect(self.log_callout)
        plug_b.clicked.connect(self.plug_callout)
        settings_b.clicked.connect(self.sett_callout)
        log_b.setStyleSheet(nm.read("./stylesheets/nav-button.css"))
        plug_b.setStyleSheet(nm.read("./stylesheets/nav-button.css"))
        settings_b.setStyleSheet(nm.read("./stylesheets/nav-button.css"))

        icon_w= widgets.constr_label("")
        icon_e= widgets.constr_label("")
        icon_w.setStyleSheet(nm.read("./stylesheets/icon.css"))
        icon_e.setStyleSheet(nm.read("./stylesheets/icon.css"))
        widget_w, hbox_w= widgets.constr_hbox()
        widget_e, hbox_e= widgets.constr_hbox()
        self.warn_l.setStyleSheet(nm.read("./stylesheets/counter.css"))
        self.err_l.setStyleSheet(nm.read("./stylesheets/counter.css"))
        hbox_w.addWidget(icon_w)
        hbox_w.addWidget(self.warn_l)
        hbox_e.addWidget(icon_e)
        hbox_e.addWidget(self.err_l)
        widget_w.setStyleSheet(nm.read("./stylesheets/warn.css"))
        widget_e.setStyleSheet(nm.read("./stylesheets/error.css"))
        info_spacer= widgets.constr_label(" ")
        info_spacer.setFixedWidth(100)
        info_h.addWidget(info_spacer)
        info_h.addWidget(widget_w)
        info_h.addWidget(widget_e)

        wider.addWidget(b_w)
        wider.addWidget(i_w)

        return nav

    def tray_green(self):
        self.tray.setIcon(QIcon("./assets/NekoConnO.png"))

    def tray_red(self):
        self.tray.setIcon(QIcon("./assets/NekoConnE.png"))

    def tray_yellow(self):
        self.tray.setIcon(QIcon("./assets/NekoConnW.png"))

    def start_srv(self):
        self.log("starting service...")
        if not self.server.status():
            try:
                self.server.run()
            except Exception as e:
                self.error(f"failed to start service, {str(e)}")
                self.tray_red()
                return
        if self.server.status():
            self.log("service is running.")
            self.tray_green()
            self.server_action.setText("Stop")
            self.server_action.setIcon(QIcon("./assets/NekoConnE.png"))
            self.server_action.triggered.disconnect()
            self.server_action.triggered.connect(self.stop_srv)
        else:
            self.error("failed to start service.")
            self.tray_red()

    def stop_srv(self):
        self.log("stopping service...")
        self.server.stop()
        self.log("service stopped.")
        self.tray_red()
        self.server_action.triggered.disconnect()
        self.server_action.triggered.connect(self.start_srv)
        self.server_action.setText("Start")
        self.server_action.setIcon(QIcon("./assets/NekoConnO.png"))

    def trayToggle(self):
        if self.isHidden() == False:
            self.hide()
        else:
            self.show()

    def trayMenu(self):
        tm= QMenu(self)
        tm.setToolTip("NekoConnect")
        tm.setTitle("NekoConnect")
        tm.setStatusTip("NekoConnect")
        self.server_action= QAction("Start", self)
        self.server_action.setIcon(QIcon("./assets/NekoConnO.png"))
        action= QAction("Exit", self)
        action.triggered.connect(self.quit)
        action.setIcon(QIcon("./assets/exit.png"))
        self.server_action.triggered.connect(self.start_srv)
        tm.addAction(self.server_action)
        tm.addAction(action)
        return tm

    def log(self, message):
        self.console_output.append(f"  {str(self.console_line)}| "+message)
        self.console_line= self.console_line + 1

    def warn(self, message):
        self.console_output.append(f" {str(self.console_line)}| "+message)
        self.console_line= self.console_line + 1
        self.warns= self.warns + 1
        self.warn_l.setText(f" {str(self.warns)}")
        self.err_l.setText(f" {str(self.errors)}")

    def error(self, message):
        self.console_output.append(f" {str(self.console_line)}| "+message)
        self.console_line= self.console_line + 1
        self.errors= self.errors + 1
        self.warn_l.setText(f" {str(self.warns)}")
        self.err_l.setText(f" {str(self.errors)}")

    def debug(self, message):
        if __debug_f__:
            self.console_output.append(f"󰨰 {str(self.console_line)}| "+message)
            self.console_line= self.console_line + 1

    def plugin_initialize(self):
        plugins= []
        if not path.exists(DIRECTORY+"/repo.list"):
            generate_sources()

        sources= nm.read(DIRECTORY+"/repo.list").split("\n")
        i= 0
        for source in sources:
            if source == "":
                sources.pop(i)
                continue
            if not len(source) > 8:
                sources.pop(i)
                continue
            if not source[:3] == "src":
                sources.pop(i)
                continue
            i= i+1

        providers= []
        for source in sources:
            providers.append(source.split(" ")[1])

        i= 0
        for provider in providers:
            if not provider.startswith("http://") or not provider.startswith("https://"):
                providers[i]= "http://"+provider
            i= i+1

        for provider in providers:
            if nm.isUp(provider) == 200:
                pass
            else:
                self.warn(f"provider [{provider}] is unreachable.")

        return plugins

    def plugin_constr(self):
        plugins= self.plugin_initialize()
        w= QWidget()
        w.setStyleSheet(nm.read("./stylesheets/plugins.css"))
        sa= QScrollArea(w)
        sa.setWidgetResizable(True)
        vw= QWidget()
        sa.setFixedWidth(480)
        sa.setFixedHeight(250)
        vb= QVBoxLayout(vw)
        sa.setWidget(vw)
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))
        vb.addWidget(widgets.constr_label("hello"))

        return w

    def settings_save(self):
        self.pass_w.setStyleSheet(nm.read("./stylesheets/setting-entry.css"))
        self.port_w.setStyleSheet(nm.read("./stylesheets/setting-entry.css"))
        if self.password_i.text() == '':
            self.pass_w.setStyleSheet(nm.read("./stylesheets/setting-entry-error.css"))
            self.error("password can not be empty.")
            return
        get_port= self.port_i.text()
        try:
            get_port= int(get_port)
        except Exception:
            self.port_w.setStyleSheet(nm.read("./stylesheets/setting-entry-error.css"))
            self.error("port must be a number.")
            return
        if get_port < 8080:
            self.port_w.setStyleSheet(nm.read("./stylesheets/setting-entry-error.css"))
            self.error("port must be greater than 8080")
            return
        self.attrs["pass"]= self.password_i.text()
        self.attrs["port"]= get_port
        save_conf(self.attrs)
        self.log("saved new config.")

    def settings_constr(self):
        w= QWidget()
        vb= QVBoxLayout(w)
        password_l= widgets.constr_label("Password ")
        self.password_i= QLineEdit()
        port_l= widgets.constr_label("Port ")
        self.port_i= QLineEdit()
        self.pass_w, pass_hb= widgets.constr_hbox()
        self.port_w, port_hb= widgets.constr_hbox()
        pass_hb.addWidget(password_l)
        pass_hb.addWidget(self.password_i)
        self.password_i.setText(self.attrs["pass"])
        self.port_i.setText(str(self.attrs["port"]))
        self.pass_w.setStyleSheet(nm.read("./stylesheets/setting-entry.css"))
        vb.addWidget(self.pass_w)
        port_hb.addWidget(port_l)
        port_hb.addWidget(self.port_i)
        self.port_w.setStyleSheet(nm.read("./stylesheets/setting-entry.css"))
        vb.addWidget(self.port_w)
        spacer= QWidget()
        spacer.setFixedHeight(80)
        vb.addWidget(spacer)
        sub_w, sub_hb= widgets.constr_hbox()
        sub_spacer= QWidget()
        sub_spacer.setFixedWidth(360)
        sub_b= QPushButton()
        sub_b.setText("Save")
        sub_b.clicked.connect(self.settings_save)
        sub_hb.addWidget(sub_spacer)
        sub_hb.addWidget(sub_b)
        sub_w.setStyleSheet(nm.read("./stylesheets/setting-save.css"))
        vb.addWidget(sub_w)

        return w

    def create_ui(self)-> None:
        main_widget= QWidget()
        self.setCentralWidget(main_widget)
        vertical_grid= QVBoxLayout(main_widget)
        vertical_grid.setContentsMargins(0, 0, 0, 0)
        vertical_grid.setSpacing(0)
        main_widget.setStyleSheet(nm.read("./stylesheets/nav.css"))
        self.stack.setFixedHeight(250)

        vertical_grid.addWidget(widgets.constr_label("NekoConnect", "font-size: 18px; font-weight: bold;"), 0, Qt.AlignmentFlag(8))

        self.console_output.setReadOnly(True)
        self.console_output.setFixedHeight(250)
        self.console_output.setStyleSheet(nm.read("./stylesheets/log.css")+"QTextEdit{font-family: "+self.TFF+";}")
        self.stack.addWidget(self.console_output)
        plugin_page= self.plugin_constr()
        sett_page= self.settings_constr()
        plugin_page.setFixedHeight(250)
        sett_page.setFixedHeight(250)
        self.stack.addWidget(plugin_page)
        self.stack.addWidget(sett_page)

        self.log(f"Starting NekoConnect v{__version__}")
        self.debug("debug build, flag set")
        
        vertical_grid.addWidget(self.stack)
        vertical_grid.addWidget(self.nav_constr())

        self.stack.setCurrentIndex(0)

class Client:
    def __init__(self, port, auth)-> None:
        self.host= '0.0.0.0'
        self.port= port
        self.auth= auth
        self.connection: socket.socket

    def connect(self)-> int:
        self.connection= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))

        greet= randStr()
        self.connection.send(len(greet).to_bytes(4))
        g_l= self.connection.recv(len(greet))
        if not int().from_bytes(g_l) == len(greet):
            self.connection.close()
            return 504
        self.connection.send(greet.encode())
        read_rand= self.connection.recv(4)
        self.connection.send(read_rand)
        ranmom= self.connection.recv(int().from_bytes(read_rand))
        encshion= crypt(ranmom.decode(), greet, self.auth)
        self.connection.send(len(encshion).to_bytes(4))
        enc_l= self.connection.recv(4)
        if not int().from_bytes(enc_l) == len(encshion):
            self.connection.close()
            return 504
        self.connection.send(encshion.encode())
        resp= self.connection.recv(4)

        return int().from_bytes(resp)

    def disconnect(self)-> None:
        self.connection.close()

class Server:
    def __init__(self, port, auth, logger, warn, error, dbg)-> None:
        self.host= '0.0.0.0'
        self.port= port
        self.auth= auth
        self.server: socket.socket
        self.logger= logger
        self.warn= warn
        self.error= error
        self.dbg= dbg

    def spawn(self):
        self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

    def handler(self):
        self.logger("handler alive.")
        while True:
            conn, addr= self.server.accept()
            self.logger(f"Client {addr[0]}:{addr[1]} connected.")

            greet_l= conn.recv(4)
            conn.send(greet_l)
            greet= conn.recv(int().from_bytes(greet_l))
            rand_resp= randStr().encode()
            conn.send(len(rand_resp).to_bytes(4))
            check= conn.recv(4)
            if not int().from_bytes(check) == len(rand_resp):
                conn.close()
            conn.send(rand_resp)
            enc_len= conn.recv(4)
            conn.send(enc_len)
            enc_raw= conn.recv(int().from_bytes(enc_len)).decode()
            calc= crypt(rand_resp.decode(), greet.decode(), self.auth)
            if calc == enc_raw:
                conn.send(int(200).to_bytes(4))
            else:
                conn.send(int(400).to_bytes(4))

            conn.close()

    def init(self):
        self.thread= multiprocessing.Process(target=self.handler)

    def run(self):
        self.spawn()
        self.dbg("server starting thread.")
        self.thread.start()

    def stop(self):
        self.thread.kill()
        self.server.close()

    def status(self):
        return self.thread.is_alive()

if __name__ == '__main__':
    app= QApplication(sys.argv)
    if not "--nosplash" in sys.argv and not "--no-spash" in sys.argv:
        splash= QSplashScreen(QPixmap("./assets/NekoConnectBanner.png"))
        splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        splash.show()
        QTimer.singleShot(2000, splash.close)
        while splash.isVisible():
            app.processEvents()
    runner= UI()
    app.exec()
