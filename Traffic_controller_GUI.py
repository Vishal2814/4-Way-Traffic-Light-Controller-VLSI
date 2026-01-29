import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QHBoxLayout,
    QPushButton, QGridLayout
)
from PyQt5.QtCore import QTimer, Qt

CSV_FILE = r"D:/VLSI/Traffic light controller/sim_data.csv"


class TrafficGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4-Way Traffic Controller Simulation")
        self.resize(1000, 700)

        self.data = self.load_csv(CSV_FILE)
        self.index = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ================= Buttons =================
        self.control_layout = QHBoxLayout()

        self.start_btn = QPushButton("START")
        self.stop_btn = QPushButton("STOP")

        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4da6ff;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                min-width: 150px;
            }
        """)

        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6666;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                min-width: 150px;
            }
        """)

        self.control_layout.addStretch()
        self.control_layout.addWidget(self.start_btn)
        self.control_layout.addWidget(self.stop_btn)
        self.control_layout.addStretch()

        self.layout.addLayout(self.control_layout)

        self.start_btn.clicked.connect(self.start_simulation)
        self.stop_btn.clicked.connect(self.stop_simulation)

        # ================= Timer =================
        self.time_label = QLabel("TIMER: 0 s")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            margin: 10px;
        """)
        self.layout.addWidget(self.time_label)

        # ================= 4-Way Signals =================
        self.signals_layout = QGridLayout()
        self.signals_layout.setSpacing(20)

        self.north, self.n_red, self.n_yel, self.n_grn = self.create_signal("NORTH")
        self.south, self.s_red, self.s_yel, self.s_grn = self.create_signal("SOUTH")
        self.east,  self.e_red, self.e_yel, self.e_grn = self.create_signal("EAST")
        self.west,  self.w_red, self.w_yel, self.w_grn = self.create_signal("WEST")

        self.signals_layout.addWidget(self.north, 0, 1)
        self.signals_layout.addWidget(self.south, 0, 2)
        self.signals_layout.addWidget(self.west, 0, 4)
        self.signals_layout.addWidget(self.east, 0, 3)

        self.layout.addLayout(self.signals_layout)

        # ================= Table =================
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['TIME', 'STATE', 'TIMER', 'NS', 'EW'])
        self.table.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.table)
        self.populate_table()

        # ================= Simulation Timer =================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lights)

    # ====================================================
    def start_simulation(self):
        self.index = 0
        self.time_label.setText("TIMER: 0 s")
        self.timer.start(1000)   # 1 Hz (real-time simulation)

    def stop_simulation(self):
        self.timer.stop()

    def load_csv(self, filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def populate_table(self):
        self.table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, key in enumerate(['TIME', 'STATE', 'TIMER', 'NS', 'EW']):
                self.table.setItem(i, j, QTableWidgetItem(row[key]))

    # ================= Traffic Signals =================
    def create_signal(self, title):
        box = QVBoxLayout()

        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")

        red = QLabel("●")
        yellow = QLabel("●")
        green = QLabel("●")

        for l in (red, yellow, green):
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet("color: grey; font-size: 100px;")

        box.addWidget(label)
        box.addWidget(red)
        box.addWidget(yellow)
        box.addWidget(green)

        container = QWidget()
        container.setLayout(box)

        return container, red, yellow, green

    def set_color(self, r, y, g, val):
        r.setStyleSheet("color: red; font-size: 100px;" if val == "R" else "color: grey; font-size: 100px;")
        y.setStyleSheet("color: orange; font-size: 100px;" if val == "Y" else "color: grey; font-size: 100px;")
        g.setStyleSheet("color: green; font-size: 100px;" if val == "G" else "color: grey; font-size: 100px;")

    def update_lights(self):
        if self.index >= len(self.data):
            self.timer.stop()
            return

        row = self.data[self.index]

        ns = row['NS']
        ew = row['EW']
        timer_val = row['TIMER']

        self.time_label.setText(f"TIMER: {timer_val} s")

        self.set_color(self.n_red, self.n_yel, self.n_grn, ns)
        self.set_color(self.s_red, self.s_yel, self.s_grn, ns)

        self.set_color(self.e_red, self.e_yel, self.e_grn, ew)
        self.set_color(self.w_red, self.w_yel, self.w_grn, ew)

        self.table.selectRow(self.index)
        self.index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TrafficGUI()
    gui.show()
    sys.exit(app.exec_())
