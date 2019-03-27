import sys
from PyQt5 import QtCore, QtWidgets
from design.design import Ui_MainWindow
from design.options import Ui_OptionsWindow
from classes.inputs import Inputs
from classes.window import Window
import json
import itopod
import math
import coordinates as coords
import win32gui

class NguScriptApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(NguScriptApp, self).__init__(parent)
        self.setupUi(self)  # generate the UI
        self.mutex = QtCore.QMutex()  # lock for script thread to enable pausing
        self.w = Window()
        self.i = Inputs(self.w, self.mutex)

        self.setup()

    def setup(self):
        """Add logic to UI elements."""
        self.rebirth_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.task_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.get_ngu_window()
        self.w_elapsed.hide()
        self.w_exp.hide()
        self.w_pp.hide()
        self.w_qp.hide()
        self.w_exph.hide()
        self.w_pph.hide()
        self.w_qph.hide()
        self.current_task_text.hide()
        self.task_progress.hide()
        self.current_rb_text.hide()
        self.rebirth_progress.hide()
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.action_stop)
        self.run_button.clicked.connect(self.action_run)
        self.run_options.clicked.connect(self.action_options)

        try:
            with open("stats.txt", "r") as f:
                data = json.loads(f.read())
                self.lifetime_itopod_kills = int(data["itopod_snipes"])
                self.lifetime_itopod_kills_data.setText(str(self.human_format(self.lifetime_itopod_kills)))
                self.lifetime_itopod_time_saved_data.setText(data["itopod_time_saved"])
        except FileNotFoundError:
            self.lifetime_itopod_kills_data.setText("0")
            self.lifetime_itopod_time_saved_data.setText("0")
            self.lifetime_itopod_kills = 0
        #self.tabWidget.setFixedSize(self.sizeHint())  # shrink window
    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               quit_msg, QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            with open("stats.txt", "w") as f:
                data = {"itopod_snipes": self.lifetime_itopod_kills,
                        "itopod_time_saved": self.lifetime_itopod_time_saved_data.text()}
                f.write(json.dumps(data))
            event.accept()
        else:
            event.ignore()
    def window_enumeration_handler(self, hwnd, top_windows):
        """Add window title and ID to array."""
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    def get_ngu_window(self):
        """Get window ID for NGU IDLE."""
        window_name = "debugg"
        top_windows = []
        win32gui.EnumWindows(self.window_enumeration_handler, top_windows)
        for i in top_windows:
            if window_name in i[1].lower():
                self.w.id = i[0]

        if self.w.id:
            self.window_retry.setText("Show Window")
            self.window_retry.clicked.connect(self.action_show_window)
            self.window_info_text.setText("Window detected!")
            self.get_top_left()
            if Window.x and Window.y:
                self.window_info_text.setStyleSheet("color: green")
                self.window_info_text.setText(f"Window detected! Game detected at: {Window.x}, {Window.y}")
        else:
            self.window_retry.clicked.connect(self.get_ngu_window)

    def get_top_left(self):
        """Get coordinates for top left of game."""
        try:
            Window.x, Window.y = self.i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
        except TypeError:
            self.window_info_text.setText(f"Window detected, but game not found!")
            self.window_info_text.setStyleSheet("color: red")
            self.window_retry.setText("Retry")
            self.window_retry.disconnect()
            self.window_retry.clicked.connect(self.get_ngu_window)
        print(Window.x, Window.y)
    def action_show_window(self):
        """Activate game window."""
        win32gui.ShowWindow(self.w.id, 5)
        win32gui.SetForegroundWindow(self.w.id)

    def action_stop(self, thread):
        """Stop script thread."""
        if self.mutex.tryLock(1000):
            self.run_thread.terminate()
            self.run_button.setText("Run")
            self.run_button.disconnect()
            self.run_button.clicked.connect(self.action_run)
            self.stop_button.setEnabled(False)
            self.mutex.unlock()
        else:
            QtWidgets.QMessageBox.information(self, "Error", "Couldn't acquire lock of script thread.")

    def action_pause(self, thread):
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.run_button.setText("Pausing...")
        self.mutex.lock()
        self.run_button.disconnect()
        self.run_button.clicked.connect(self.action_resume)
        self.run_button.setText("Resume")
        self.run_button.setEnabled(True)

    def action_resume(self, thread):
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.run_button.setText("Pause")
        self.run_button.disconnect()
        self.mutex.unlock()
        self.run_button.setEnabled(True)
        self.run_button.clicked.connect(self.action_pause)

    def action_options(self):
        self.options = OptionsWindow()
        self.options.setFixedSize(self.sizeHint())
        self.options.show()


    def human_format(self, num):
        num = float('{:.3g}'.format(num))
        if num > 1e14:
            return
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def update(self, result):
        for k, v in result.items():
            if k == "exp":
                self.exp_data.setText(self.human_format(v))
            elif k == "pp":
                self.pp_data.setText(self.human_format(v))
            elif k == "qp":
                self.qp_data.setText(self.human_format(v))
            elif k == "xph":
                self.exph_data.setText(self.human_format(v))
            elif k == "pph":
                self.pph_data.setText(self.human_format(v))
            elif k == "qph":
                self.qph_data.setText(self.human_format(v))
            elif k == "timer":
                prog = (1 + ((result["current"] - result["end"]) / result["duration"])) * 100
                self.task_progress.setValue(math.ceil(prog))
            elif k == "itopod_snipes":
                self.lifetime_itopod_kills += 1
                self.lifetime_itopod_kills_data.setText(str(self.human_format(self.lifetime_itopod_kills)))

                n = self.lifetime_itopod_kills * 0.8
                days = math.floor(n // (24 * 3600))
                n = n % (24 * 3600)
                hours = math.floor(n // 3600)
                n %= 3600
                minutes = math.floor(n // 60)
                n %= 60
                seconds = math.floor(n)

                self.lifetime_itopod_time_saved_data.setText(f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

    def action_run(self):
        runs = ["Static Questing",
                "Static ITOPOD"]
        text = str(self.combo_run.currentText())
        run = runs.index(text)
        print(run)
        if run == 1:
            self.run_thread = ScriptThread(1, self.w, self.mutex)
            self.run_thread.signal.connect(self.update)
            self.run_button.setText("Pause")
            self.run_button.disconnect()
            self.run_button.clicked.connect(self.action_pause)
            self.w_exp.show()
            self.w_pp.show()
            self.w_pph.show()
            self.w_exph.show()
            self.current_task_text.setText("Sniping I.T.O.P.O.D")
            self.current_task_text.show()
            self.task_progress.show()
            self.task_progress.setValue(0)
            self.stop_button.setEnabled(True)
            self.run_thread.start()

class OptionsWindow(QtWidgets.QMainWindow, Ui_OptionsWindow):
    def __init__(self, parent=None):
        super(OptionsWindow, self).__init__(parent)
        self.setupUi(self)

class ScriptThread(QtCore.QThread):
    """Thread class for script."""
    signal = QtCore.pyqtSignal("PyQt_PyObject")

    def __init__(self, run, w, mutex):
        QtCore.QThread.__init__(self)
        self.run = run
        self.w = w
        self.mutex = mutex

    def run(self):
        if self.run == 1:
            itopod.run(self.w, self.mutex, self.signal, 60)
            print("value")


def run():
    """Start GUI thread."""
    app = QtWidgets.QApplication(sys.argv)
    GUI = NguScriptApp()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

"""
Ideas

Progressbars tracking current long running task (sniping, questing)
Progressbar tracking run progression (if applicable)
Tools for annoying actions while playing manually (cap all diggers)
Quickstart for infinite questing/itopod sniping
Track minor/major quests done
"""