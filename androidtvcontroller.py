import sys
import os
import json
import subprocess
import win10toast
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QListWidget, QListWidgetItem, QStackedLayout, QGridLayout, QFrame, QComboBox)
from PyQt5.QtCore import (Qt, QTimer, QRectF)
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtGui import QIcon

KEYCODE_BACK = "KEYCODE_BACK"
KEYCODE_HOME = "KEYCODE_HOME"
KEYCODE_APP_SWITCH = "KEYCODE_APP_SWITCH"
KEYCODE_POWER = "KEYCODE_POWER"
KEYCODE_VOLUME_UP = "KEYCODE_VOLUME_UP"
KEYCODE_VOLUME_DOWN = "KEYCODE_VOLUME_DOWN"
KEYCODE_DPAD_LEFT = "KEYCODE_DPAD_LEFT"
KEYCODE_DPAD_RIGHT = "KEYCODE_DPAD_RIGHT"
KEYCODE_DPAD_UP = "KEYCODE_DPAD_UP"
KEYCODE_DPAD_DOWN = "KEYCODE_DPAD_DOWN"
KEYCODE_ENTER = "KEYCODE_ENTER"

class AndroidTVRemote(QWidget):
    def __init__(self):
        super().__init__()
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'icon', 'icon.ico')
        else:
            icon_path = os.path.join(os.path.dirname(__file__), 'icon', 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.toaster = win10toast.ToastNotifier()
        self.setWindowTitle("Android TV Remote")
        self.setFixedSize(300, 600)
        self.setStyleSheet("background-color: #111; color: #ccc;")
        self.current_device_ip = None
        
        self.ips_file = os.path.join(os.path.expanduser("~"), "Documents", "AndroidTVController", "ips.json")
        self.ips = self.load_ips()
        
        self.language_file = os.path.join(os.path.expanduser("~"), "Documents", "AndroidTVController", "language.json")
        self.language = self.load_language()

        self.translations_file = os.path.join(os.path.expanduser("~"), "Documents", "AndroidTVController", "translations.json")
        self.translations = self.load_translations()

        self.create_howto_file()

        self.init_ui()
        self.text_input.setFocus()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_connection_status)
        self.timer.start(3000)
        self.check_connection_status()

    def check_connection_status(self):
        output = self.run_adb(["get-state"])
        if "device" in output.lower():
            self.status.setText(f"{self.translate('status_connected')} {self.current_device_ip}")
            self.status.setStyleSheet("color: green; font-size: 16px;")
            self.show_notification(self.translate("status_connected"), f"{self.translate('status_connected')} {self.current_device_ip}")
        else:
            if self.current_device_ip:
                self.show_notification(self.translate("status_disconnected"), f"{self.translate('status_disconnected')} {self.current_device_ip}")
            self.status.setText(self.translate("status_disconnected"))
            self.status.setStyleSheet("color: gray; font-size: 16px;")

    def load_ips(self):
        if not os.path.exists(self.ips_file):
            default_ips = {"ip_addresses": []}
            self.save_ips(default_ips)
            return default_ips
        else:
            with open(self.ips_file, "r") as f:
                return json.load(f)

    def save_ips(self, ips):
        os.makedirs(os.path.dirname(self.ips_file), exist_ok=True)
        with open(self.ips_file, "w") as f:
            json.dump(ips, f, indent=4)

    def load_language(self):
        if not os.path.exists(self.language_file):
            default_language = {"language": "English"}
            self.save_language(default_language)
            return default_language
        else:
            with open(self.language_file, "r") as f:
                return json.load(f)

    def save_language(self, language):
        os.makedirs(os.path.dirname(self.language_file), exist_ok=True)
        with open(self.language_file, "w") as f:
            json.dump(language, f, indent=4)

    def load_translations(self):
        default_translations = {
            "Español": {
                "status_disconnected": "● Desconectado",
                "status_connected": "● Conectado",
                "text_input_placeholder": "Texto a enviar",
                "send": "Enviar",
                "connect_to_ip": "Conectar a IP",
                "connect": "Conectar",
                "disconnect_device": "Desconectar dispositivo",
                "previous_connections": "Conexiones previas:",
                "no_previous_connections": "Sin conexiones previas.",
                "language": "Idioma:",
                "close_settings": "Cerrar ajustes",
                "connection_success": "Conexión exitosa",
                "connection_error": "Error de conexión",
                "disconnected": "Desconectado"
            },
            "English": {
                "status_disconnected": "● Disconnected",
                "status_connected": "● Connected",
                "text_input_placeholder": "Text to send",
                "send": "Send",
                "connect_to_ip": "Connect to IP",
                "connect": "Connect",
                "disconnect_device": "Disconnect device",
                "previous_connections": "Previous connections:",
                "no_previous_connections": "No previous connections.",
                "language": "Language:",
                "close_settings": "Close settings",
                "connection_success": "Connection successful",
                "connection_error": "Connection error",
                "disconnected": "Disconnected"
            }
        }
        if not os.path.exists(self.translations_file):
            os.makedirs(os.path.dirname(self.translations_file), exist_ok=True)
            with open(self.translations_file, "w", encoding="utf-8") as f:
                json.dump(default_translations, f, indent=4, ensure_ascii=False)
        with open(self.translations_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def translate(self, key):
        lang = self.language["language"]
        return self.translations.get(lang, {}).get(key, key)
            
    def init_ui(self):
        self.status = QLabel("● Desconectado")
        self.status.setStyleSheet("color: gray; font-size: 16px;")

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setFixedSize(32, 32)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #222;
                font-size: 18px;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #333;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings_overlay)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText(self.translate("text_input_placeholder"))
        self.text_input.setStyleSheet("padding: 8px; font-size: 14px; background-color: #333; color: #ccc;")
        self.text_input.returnPressed.connect(self.send_text)

        self.send_btn = QPushButton(self.translate("send"))
        self.send_btn.setStyleSheet("background-color: #444; padding: 8px; font-size: 14px;")
        self.send_btn.clicked.connect(self.send_text)

        self.controls_layout = self.build_controls()

        main_layout = QVBoxLayout()
        top_row = QHBoxLayout()
        top_row.addWidget(self.status)
        top_row.addStretch()
        top_row.addWidget(self.settings_btn)

        main_layout.addLayout(top_row)
        main_layout.addLayout(self.controls_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.text_input)
        bottom_layout.addWidget(self.send_btn)

        main_layout.addLayout(bottom_layout)

        self.stack = QStackedLayout(self)
        base_widget = QWidget()
        base_widget.setLayout(main_layout)
        self.stack.addWidget(base_widget)

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.95);")
        self.overlay_layout = QVBoxLayout()
        self.overlay.setLayout(self.overlay_layout)

        self.setup_settings_overlay()

        self.stack.addWidget(self.overlay)
        self.stack.setCurrentIndex(0)
        self.setLayout(self.stack)

    def setup_settings_overlay(self):
        ip_input = QLineEdit()
        ip_input.setPlaceholderText(self.translate("connect_to_ip"))
        ip_input.setStyleSheet("padding: 8px; font-size: 14px; background-color: #222; color: #ccc;")
        ip_input.returnPressed.connect(lambda: self.connect_to_ip(ip_input.text()))

        connect_btn = QPushButton(self.translate("connect"))
        connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                padding: 8px;
                font-size: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        connect_btn.clicked.connect(lambda: self.connect_to_ip(ip_input.text()))

        disconnect_btn = QPushButton(self.translate("disconnect_device"))
        disconnect_btn.clicked.connect(self.disconnect_device)
        disconnect_btn.setStyleSheet("background-color: #444; padding: 8px; font-size: 14px;")

        history_label = QLabel(self.translate("previous_connections"))

        ip_addresses = self.ips.get("ip_addresses", [])
        if not ip_addresses:
            ip_addresses = [self.translate("no_previous_connections")]

        history_list = QListWidget()
        for ip in ip_addresses:
            item = QListWidgetItem(ip)
            if ip == self.translate("no_previous_connections"):
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
            history_list.addItem(item)

        history_list.itemDoubleClicked.connect(lambda item: self.reconnect(item.text()))

        close_btn = QPushButton(self.translate("close_settings"))
        close_btn.setStyleSheet("background-color: #333; padding: 8px; font-size: 14px;")
        close_btn.clicked.connect(self.close_settings_overlay)

        self.overlay_status = QLabel(self.translate("status_disconnected"))
        self.overlay_status.setStyleSheet("color: gray; font-size: 16px; margin-bottom: 8px;")
        self.overlay_layout.insertWidget(1, self.overlay_status)

        self.overlay_layout.addWidget(ip_input)
        self.overlay_layout.addWidget(connect_btn)
        self.overlay_layout.addWidget(disconnect_btn)
        self.overlay_layout.addWidget(history_label)
        self.overlay_layout.addWidget(history_list)

        language_label = QLabel(self.translate("language"))
        language_label.setStyleSheet("color: white; font-size: 14px;")

        language_select = QComboBox()
        language_select.clear()
        for lang_name, translations in self.translations.items():
            language_select.addItem(lang_name, lang_name)
        current_language = self.language["language"]
        if current_language in self.translations:
            language_select.setCurrentText(current_language)
        else:
            language_select.setCurrentIndex(0)
        language_select.setEditable(False)
        language_select.setStyleSheet("padding: 8px; font-size: 14px; background-color: #222; color: #ccc; border: none;")
        language_select.currentIndexChanged.connect(lambda: self.change_language(language_select.currentData()))
        language_select.currentIndexChanged.connect(self.update_ui_language)

        self.overlay_layout.addWidget(language_label)
        self.overlay_layout.addWidget(language_select)

        self.overlay_layout.addWidget(close_btn)

    def change_language(self, lang):
        self.language["language"] = lang
        self.save_language(self.language)

    def update_ui_language(self):
        self.status.setText(self.translate("status_disconnected"))
        self.text_input.setPlaceholderText(self.translate("text_input_placeholder"))
        self.send_btn.setText(self.translate("send"))
        self.overlay_status.setText(self.translate("status_disconnected"))
        self.overlay_layout.itemAt(1).widget().setPlaceholderText(self.translate("connect_to_ip"))
        self.overlay_layout.itemAt(2).widget().setText(self.translate("connect"))
        self.overlay_layout.itemAt(3).widget().setText(self.translate("disconnect_device"))
        self.overlay_layout.itemAt(4).widget().setText(self.translate("previous_connections"))
        self.overlay_layout.itemAt(8).widget().setText(self.translate("close_settings"))
        self.overlay_layout.itemAt(6).widget().setText(self.translate("language"))
        self.overlay_layout.itemAt(5).widget().clear()
        ip_addresses = self.ips.get("ip_addresses", [])
        if not ip_addresses:
            ip_addresses = [self.translate("no_previous_connections")]

        for ip in ip_addresses:
            item = QListWidgetItem(ip)
            if ip == self.translate("no_previous_connections"):
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
            self.overlay_layout.itemAt(5).widget().addItem(item)

    def connect_to_ip(self, ip):
        if ip:
            output = self.run_adb(["connect", ip])
            if "connected" in output.lower():
                self.add_connection(ip)
                self.current_device_ip = ip
                self.show_notification(self.translate("connection_success"), f"{self.translate('connection_success')} {ip}")
            else:
                self.show_notification(self.translate("connection_error"), f"{self.translate('connection_error')} {ip}")
            self.check_connection_status()

    def disconnect_device(self):
        if self.current_device_ip:
            self.run_adb(["disconnect", self.current_device_ip])
            self.show_notification(self.translate("disconnected"), f"{self.translate('disconnected')} {self.current_device_ip}")
            self.current_device_ip = None
            self.check_connection_status()

    def open_settings_overlay(self):
        self.stack.setCurrentIndex(1)

    def close_settings_overlay(self):
        self.stack.setCurrentIndex(0)

    class ShapeWidget(QFrame):
        def __init__(self, shape, radius=20, parent=None):
            super().__init__(parent)
            self.shape = shape
            self.radius = radius
            self.setStyleSheet("background-color: transparent;")

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(QColor(50, 50, 50), 2)
            painter.setPen(pen)
            rect = QRectF(0, 0, self.width(), self.height())
            path = QPainterPath()

            if self.shape == "circle":
                painter.drawEllipse(self.rect())
            elif self.shape == "rectangle":
                path.addRoundedRect(rect, self.radius, self.radius)
                painter.drawPath(path)

    def build_controls(self):
        layout = QVBoxLayout()

        power_btn = self.make_button("⏻")
        power_btn.clicked.connect(self.send_power_signal)

        up = self.make_button("↑")
        down = self.make_button("↓")
        left = self.make_button("←")
        right = self.make_button("→")
        ok = QPushButton("")
        ok.setFixedSize(80, 80)
        ok.setStyleSheet("""
            QPushButton {
                background-color: #000;
                border-radius: 40;
                font-size: 18px;
                color: white;
                border: 2px solid #333;
            }
            QPushButton:hover {
                background-color: #333;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        up.clicked.connect(self.send_up_key_signal)
        down.clicked.connect(self.send_down_key_signal)
        left.clicked.connect(self.send_left_key_signal)
        right.clicked.connect(self.send_right_key_signal)
        ok.clicked.connect(self.send_ok_key_signal)

        nav_circle = self.ShapeWidget("circle")
        nav_circle.setFixedSize(200, 200)

        nav_layout = QGridLayout(nav_circle)
        nav_layout.addWidget(up, 0, 1, alignment=Qt.AlignCenter)
        nav_layout.addWidget(left, 1, 0, alignment=Qt.AlignCenter)
        nav_layout.addWidget(ok, 1, 1, alignment=Qt.AlignCenter)
        nav_layout.addWidget(right, 1, 2, alignment=Qt.AlignCenter)
        nav_layout.addWidget(down, 2, 1, alignment=Qt.AlignCenter)

        apps_btn = self.make_button("⛶")
        back_btn = self.make_button("←")
        home_btn = self.make_button("○")
        apps_btn.clicked.connect(self.send_apps_signal)
        back_btn.clicked.connect(self.send_back_signal)
        home_btn.clicked.connect(self.send_home_signal)

        row1 = QHBoxLayout()
        row1.addWidget(apps_btn)
        row1.addWidget(back_btn)
        row1.addWidget(home_btn)
        row1.setAlignment(Qt.AlignCenter)

        vol_up = self.make_button("+")
        vol_down = self.make_button("-")
        vol_up.clicked.connect(self.send_volume_up_signal)
        vol_down.clicked.connect(self.send_volume_down_signal)

        vol_rect = self.ShapeWidget("rectangle")
        vol_rect.radius = 25
        vol_rect.setFixedSize(70, 120)
        vol_layout = QVBoxLayout(vol_rect)
        vol_layout.addWidget(vol_up, alignment=Qt.AlignCenter)
        vol_layout.addWidget(vol_down, alignment=Qt.AlignCenter)

        control_layout = QVBoxLayout()
        control_layout.addWidget(power_btn, alignment=Qt.AlignCenter)
        control_layout.addWidget(nav_circle, alignment=Qt.AlignCenter)
        control_layout.addLayout(row1)
        control_layout.addWidget(vol_rect, alignment=Qt.AlignCenter)

        layout.addLayout(control_layout)
        layout.setAlignment(Qt.AlignCenter)

        return layout

    def make_button(self, label, size=23):
        btn = QPushButton(label)
        btn.setFixedSize(size + 23, size + 23)
        
        btn.setStyleSheet("""
            QPushButton {
                background-color: #000;
                border-radius: 23;
                font-size: 16px;
                color: white;
                border-color: #333;
                border-width: 1px;
                border-style: solid;
            }
            QPushButton:hover {
                background-color: #333;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        return btn

    def run_adb(self, args):
        adb_path = os.path.join(os.path.dirname(__file__), "platform-tools", "adb.exe")
        try:
            result = subprocess.run([adb_path] + args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return result.stdout
        except Exception as e:
            return str(e)

    def send_text(self):
        text = self.text_input.text().strip()
        if text:
            self.run_adb(["shell", "input", "text", text.replace(" ", "%s")])
            self.text_input.clear()
        self.text_input.setFocus()

    def add_connection(self, ip):
        if ip and ip not in self.ips["ip_addresses"]:
            self.ips["ip_addresses"].append(ip)
            self.save_ips(self.ips)
        
    def send_back_signal(self):
        self.send_key_signal(KEYCODE_BACK)
        
    def send_home_signal(self):
        self.send_key_signal(KEYCODE_HOME)
    
    def send_apps_signal(self):
        self.send_key_signal(KEYCODE_APP_SWITCH)
    
    def send_power_signal(self):
        self.send_key_signal(KEYCODE_POWER)

    def send_volume_up_signal(self):
        self.send_key_signal(KEYCODE_VOLUME_UP)
    
    def send_volume_down_signal(self):
        self.send_key_signal(KEYCODE_VOLUME_DOWN)
        
    def send_left_key_signal(self):
        self.send_key_signal(KEYCODE_DPAD_LEFT)
        
    def send_right_key_signal(self):
        self.send_key_signal(KEYCODE_DPAD_RIGHT)
        
    def send_up_key_signal(self):
        self.send_key_signal(KEYCODE_DPAD_UP)
        
    def send_down_key_signal(self):
        self.send_key_signal(KEYCODE_DPAD_DOWN)
        
    def send_ok_key_signal(self):
        self.send_key_signal(KEYCODE_ENTER)

    def show_notification(self, title, message):
        self.toaster.show_toast(title, message, duration=5, threaded=True)

    def send_key_signal(self, keycode):
        self.run_adb(["shell", "input", "keyevent", keycode])

    def create_howto_file(self):
        howto_file = os.path.expanduser("~") + "/Documents/AndroidTVController/how_to_add_languages.txt"
        howto_content = "You can add your language in translations.json. Simply copy and paste the structure from the others."

        if not os.path.exists(howto_file):
            with open(howto_file, "w", encoding="utf-8") as f:
                f.write(howto_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AndroidTVRemote()
    window.show()
    sys.exit(app.exec_())