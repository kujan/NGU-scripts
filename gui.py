import sys
from PySide2.QtCore import QThread, QMutex, Qt, QPropertyAnimation, QSettings, QTimer, Signal
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QButtonGroup, QComboBox, QLineEdit, QCheckBox, QRadioButton, QPushButton
from PySide2.QtGui import QImage, QPixmap, QIcon
from classes.stats import Stats, Tracker
from design.design import Ui_MainWindow
from design.options import Ui_OptionsWindow
from design.inventory import Ui_InventorySelecter
from classes.inputs import Inputs
from classes.helper import Helper
from classes.window import Window
from distutils.util import strtobool
from typing import ClassVar
from PIL import Image
import io
import json
import itopod
import questing
import inspect
import math
import time
import re
import coordinates as coords
import pytesseract
import win32gui


class NguScriptApp(QMainWindow, Ui_MainWindow):
    """Main window."""

    mutex: ClassVar[QMutex] = None

    def __init__(self, parent=None):
        """Generate UI."""
        super(NguScriptApp, self).__init__(parent)
        self.setupUi(self)  # generate the UI
        self.mutex = QMutex()  # lock for script thread to enable pausing
        self.setup()

    def setup(self):
        """Add logic to UI elements."""
        self.rebirth_progress.setAlignment(Qt.AlignCenter)
        self.task_progress.setAlignment(Qt.AlignCenter)
        self.get_ngu_window()
        self.test_tesseract()
        self.load_stats()
        self.task_progress.setValue(0)
        self.rebirth_progress.setValue(0)
        self.task_progress_animation = QPropertyAnimation(self.task_progress, b"value")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.action_stop)
        self.run_button.clicked.connect(self.action_run)
        self.run_options.clicked.connect(self.action_options)
        self.run_thread = None
        self.options = None
        # self.tabWidget.setFixedSize(self.sizeHint())  # shrink window

    def load_stats(self):
        self.settings = QSettings("Kujan", "NGU-Scripts")
        self.total_itopod_kills = int(self.settings.value("total_itopod_kills", "0"))
        self.total_minor_quests = int(self.settings.value("total_minor_quests", "0"))
        self.total_major_quests = int(self.settings.value("total_major_quests", "0"))
        self.lifetime_itopod_kills_data.setText(str(self.total_itopod_kills))
        self.label_total_major_quests.setText(str(self.total_major_quests))
        self.label_total_minor_quests.setText(str(self.total_minor_quests))
        n = self.total_itopod_kills * 0.8
        days = math.floor(n // (24 * 3600))
        n = n % (24 * 3600)
        hours = math.floor(n // 3600)
        n %= 3600
        minutes = math.floor(n // 60)
        n %= 60
        seconds = math.floor(n)

        self.lifetime_itopod_time_saved_data.setText(f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

    def closeEvent(self, event):
        """Event fired when exiting the application. This will save the current stats to file."""
        quit_msg = "Are you sure you want to exit?"
        reply = QMessageBox.question(self, 'Message',
                                               quit_msg, QMessageBox.Yes,
                                               QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.options is not None:
                if self.options.inventory_selecter is not None:
                    self.options.inventory_selecter.close()
                self.options.close()
            event.accept()
        else:
            event.ignore()

    def window_enumeration_handler(self, hwnd, top_windows):
        """Add window title and ID to array."""
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    def get_ngu_window(self):
        """Get window ID for NGU IDLE."""
        Helper.init()
        if Window.id:
            self.window_retry.setText("Show Window")
            self.window_retry.clicked.connect(self.action_show_window)
            self.window_info_text.setText("Window detected!")
            if Window.x and Window.y:
                self.window_info_text.setStyleSheet("color: green")
                self.window_info_text.setText(f"Game detected at: {Window.x}, {Window.y}")
                self.run_button.setEnabled(True)
                self.run_options.setEnabled(True)
        else:
            self.window_retry.clicked.connect(self.get_ngu_window)
            self.run_button.setEnabled(False)
            self.run_options.setEnabled(False)

    def test_tesseract(self):
        """Check if tesseract is installed."""
        try:
            pytesseract.image_to_string(Image.open("images/consumable.png"))
            self.get_ngu_window()
        except pytesseract.pytesseract.TesseractNotFoundError:
            self.window_info_text.setStyleSheet("color: red")
            self.window_info_text.setText("Tesseract not found")
            self.window_retry.setText("Try again")
            self.window_retry.clicked.connect(self.test_tesseract)
            self.run_button.setEnabled(False)

    def action_show_window(self):
        """Activate game window."""
        win32gui.ShowWindow(Window.id, 5)
        win32gui.SetForegroundWindow(Window.id)

    def action_stop(self, thread):
        """Stop script thread."""
        if self.mutex.tryLock(1000):  # only way to check if we have the lock without crashing?
            self.run_thread.terminate()
            self.run_button.setText("Run")
            self.run_button.clicked.connect(self.action_run)
            self.stop_button.setEnabled(False)
            self.settings.setValue("total_itopod_kills", self.total_itopod_kills)
            self.settings.setValue("total_major_quests", self.total_major_quests)
            self.settings.setValue("total_minor_quests", self.total_minor_quests)
            self.mutex.unlock()
        else:
            QMessageBox.information(self, "Error", "Couldn't acquire lock of script thread.")

    def action_pause(self, thread):
        """Attempt to block script thread by acquiring lock."""
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(False)  # stopping while paused causes a deadlock
        self.run_options.setEnabled(False)  # trying to open inventory viewer causes deadlock
        self.run_button.setText("Pausing...")
        self.mutex.lock()
        self.run_button.clicked.connect(self.action_resume)
        self.run_button.setText("Resume")
        self.run_button.setEnabled(True)

    def action_resume(self, thread):
        """Attempt to release lock to un-block script thread."""
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.run_button.setText("Pause")
        self.mutex.unlock()
        self.run_button.setEnabled(True)
        self.run_button.clicked.connect(self.action_pause)

    def action_options(self):
        """Display option window."""
        index = self.combo_run.currentIndex()
        self.options = OptionsWindow(index, self.run_thread, self)
        self.options.show()

    def human_format(self, num):
        """Convert large integer to readable format."""
        num = float('{:.3g}'.format(num))
        if num > 1e14:
            return
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def timestamp(self):
        """Update timestamp for elapsed time."""
        n = time.time() - self.start_time
        days = math.floor(n // (24 * 3600))
        n = n % (24 * 3600)

        if days > 0:
            result = f"{days} days, {time.strftime('%H:%M:%S', time.gmtime(n))}"
        else:
            result = f"{time.strftime('%H:%M:%S', time.gmtime(n))}"
        self.elapsed_data.setText(result)

    def update(self, result):
        """Update data in UI upon event."""
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
            elif k == "task_progress":
                self.task_progress_animation.setDuration(200)
                self.task_progress_animation.setStartValue(self.task_progress.value())
                self.task_progress_animation.setEndValue(v)
                self.task_progress_animation.start()
                # self.task_progress.setValue(math.ceil(v))
            elif k == "itopod_kill":
                self.total_itopod_kills += 1
                self.lifetime_itopod_kills_data.setText(str(self.human_format(self.total_itopod_kills)))
                n = self.total_itopod_kills * 0.8
                days = math.floor(n // (24 * 3600))
                n = n % (24 * 3600)
                hours = math.floor(n // 3600)
                n %= 3600
                minutes = math.floor(n // 60)
                n %= 60
                seconds = math.floor(n)

                self.lifetime_itopod_time_saved_data.setText(f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

            elif k == "task":
                self.current_task_text.setText(v)
            elif k == "quest_complete":
                if v == "minor":
                    self.total_minor_quests += 1
                    self.label_total_minor_quests.setText(str(self.human_format(self.total_minor_quests)))
                else:
                    self.total_major_quests += 1
                    self.label_total_major_quests.setText(str(self.human_format(self.total_major_quests)))

    def action_run(self):
        """Start the selected script."""
        run = self.combo_run.currentIndex()
        self.start_time = time.time()
        self.timer = QTimer()
        self.timer.setInterval(1010)
        self.timer.timeout.connect(self.timestamp)
        self.timer.start()
        if run == 0:
            self.run_thread = ScriptThread(0)
            self.run_thread.signal.connect(self.update)
            self.run_button.setText("Pause")
            self.run_button.clicked.connect(self.action_pause)
            self.w_exp.show()
            self.w_pp.hide()
            self.w_pph.hide()
            self.w_exph.show()
            self.w_qp.show()
            self.w_qph.show()
            self.current_rb_text.hide()
            self.rebirth_progress.hide()
            self.setFixedSize(300, 320)
            self.current_task_text.show()
            self.task_progress.show()
            self.task_progress.setValue(0)
            self.stop_button.setEnabled(True)
            self.run_thread.start()

        elif run == 1:
            self.run_thread = ScriptThread(1)
            self.run_thread.signal.connect(self.update)
            self.run_button.setText("Pause")
            self.run_button.clicked.connect(self.action_pause)
            self.w_exp.show()
            self.w_pp.show()
            self.w_pph.show()
            self.w_exph.show()
            self.w_qp.hide()
            self.w_qph.hide()
            self.current_rb_text.hide()
            self.rebirth_progress.hide()
            self.setFixedSize(300, 320)
            self.current_task_text.show()
            self.task_progress.show()
            self.task_progress.setValue(0)
            self.stop_button.setEnabled(True)
            self.run_thread.start()

        elif run == 2:
            self.run_thread = ScriptThread(2, self.w, self.mutex)
            self.run_thread.signal.connect(self.update)
            self.run_button.setText("Pause")
            self.run_button.clicked.connect(self.action_pause)
            self.w_exp.show()
            self.w_pp.show()
            self.w_pph.show()
            self.w_exph.show()
            self.w_qp.show()
            self.w_qph.show()
            self.current_rb_text.hide()
            self.rebirth_progress.hide()
            self.setFixedSize(300, 320)
            self.current_task_text.show()
            self.task_progress.show()
            self.task_progress.setValue(0)
            self.stop_button.setEnabled(True)
            self.run_thread.start()

class OptionsWindow(QMainWindow, Ui_OptionsWindow):
    """Option window."""

    def __init__(self, index, thread, parent=None):
        """Setup UI."""
        super(OptionsWindow, self).__init__(parent)
        self.setupUi(self)
        self.index = index
        self.settings = QSettings("Kujan", "NGU-Scripts")
        self.button_ok.clicked.connect(self.action_ok)
        self.radio_group_gear = QButtonGroup(self)
        self.radio_group_gear.addButton(self.radio_equipment)
        self.radio_group_gear.addButton(self.radio_cube)
        self.check_gear.stateChanged.connect(self.state_changed_gear)
        self.check_force.stateChanged.connect(self.state_changed_force_zone)
        self.check_boost_inventory.stateChanged.connect(self.state_changed_boost_inventory)
        self.check_merge_inventory.stateChanged.connect(self.state_changed_merge_inventory)
        self.check_subcontract.stateChanged.connect(self.state_changed_subcontract)
        self.button_boost_inventory.clicked.connect(self.action_boost_inventory)
        self.button_merge_inventory.clicked.connect(self.action_merge_inventory)
        self.inventory_selecter = None
        self.script_thread = thread
        self.gui_load()

    def state_changed_gear(self, int):
        """Update UI."""
        if self.check_gear.isChecked():
            self.radio_equipment.setEnabled(True)
            self.radio_cube.setEnabled(True)
        else:
            self.radio_equipment.setEnabled(False)
            self.radio_equipment.setChecked(False)
            self.radio_cube.setEnabled(False)
            self.radio_cube.setChecked(False)

    def state_changed_boost_inventory(self, int):
        """Update UI."""
        if self.script_thread is not None:
            if self.script_thread.isRunning():
                self.button_boost_inventory.setText("Stop current script")
                return
        self.button_boost_inventory.setText("Setup")
        if self.check_boost_inventory.isChecked():
            self.button_boost_inventory.setEnabled(True)
        else:
            self.button_boost_inventory.setEnabled(False)

    def state_changed_merge_inventory(self, int):
        """Update UI."""
        if self.script_thread is not None:
            if self.script_thread.isRunning():
                self.button_boost_inventory.setText("Stop current script")
                return
        if self.check_merge_inventory.isChecked():
            self.button_merge_inventory.setEnabled(True)
        else:
            self.button_merge_inventory.setEnabled(False)

    def action_boost_inventory(self, int):
        """Update UI."""
        if self.check_boost_inventory.isChecked():
            self.inventory_selecter = InventorySelecter("arr_boost_inventory", self)
            self.inventory_selecter.show()

    def action_merge_inventory(self, int):
        """Update UI."""
        if self.check_merge_inventory.isChecked():
            self.inventory_selecter = InventorySelecter("arr_merge_inventory", self)
            self.inventory_selecter.show()

    def state_changed_force_zone(self, int):
        """Update UI."""
        if self.check_force.isChecked():
            self.combo_force.setEnabled(True)
        else:
            self.combo_force.setEnabled(False)

    def state_changed_subcontract(self, int):
        """Show warning."""
        if self.check_subcontract.isChecked():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Are you sure you wish to subcontract your quests?")
            msg.setWindowTitle("Subcontract warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def gui_load(self):
        """Load settings from registry."""
        if self.index == 0:
            self.check_force.show()
            self.check_major.show()
            self.check_subcontract.show()
            self.combo_force.show()
            self.setFixedSize(315, 250)

        elif self.index == 1:
            self.check_force.hide()
            self.check_major.hide()
            self.check_subcontract.hide()
            self.combo_force.hide()
            self.setFixedSize(300, 200)
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()
                text = obj.itemText(index)
                name = obj.objectName()
                value = (self.settings.value(name))

                if value == "":
                    continue

                index = obj.findText(value)

                if index == -1:
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)

            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = (self.settings.value(name))
                obj.setText(value)

            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                value = self.settings.value(name)
                if value is not None:
                    obj.setChecked(strtobool(value))
            if isinstance(obj, QRadioButton):
                name = obj.objectName()
                value = self.settings.value(name)
                if value is not None:
                    obj.setChecked(strtobool(value))

    def action_ok(self):
        """Save settings and close window."""
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QComboBox):
                name = obj.objectName()
                index = obj.currentIndex()
                text = obj.itemText(index)
                self.settings.setValue(name, text)
                self.settings.setValue(name + "_index", index)

            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = obj.text()
                self.settings.setValue(name, value)

            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                state = obj.isChecked()
                self.settings.setValue(name, state)

            if isinstance(obj, QRadioButton):
                name = obj.objectName()
                value = obj.isChecked()
                self.settings.setValue(name, value)
        self.close()


class InventorySelecter(QMainWindow, Ui_InventorySelecter):
    """Option window."""

    def __init__(self, mode, parent=None):
        """Setup UI."""
        super(InventorySelecter, self).__init__(parent)
        self.setupUi(self)
        self.mode = mode
        self.settings = QSettings("Kujan", "NGU-Scripts")
        self.slots = []
        self.button_ok.clicked.connect(self.action_ok)
        self.generate_inventory()
        self.setFixedSize(761, 350)

    def action_ok(self):
        """Save settings and close window."""
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QPushButton):
                if obj.toggled:
                    name = obj.objectName()
                    if name == "button_ok":
                        continue
                    print(name)
                    self.slots.append(re.sub(r"[^0-9]", "", name))
        print(self.slots)
        self.settings.setValue(self.mode, self.slots)
        self.close()

    def pil2pixmap(self, im):
        """Convert PIL Image object to QPixmap"""
        with io.BytesIO() as output:
            im.save(output, format="png")
            output.seek(0)
            data = output.read()
            qim = QImage.fromData(data)
            pixmap = QPixmap.fromImage(qim)
        return pixmap

    def action_button_clicked(self):
        button = getattr(self, self.sender().objectName())

        if not button.toggled:
            button.toggled = True
            button.setStyleSheet("border:3px solid rgb(0, 0, 0)")
        else:
            button.toggled = False
            button.setStyleSheet("")

    def generate_inventory(self, depth=0):
        """Get image from inventory and create clickable grid."""
        if depth > 4:  # infinite recursion guard
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Couldn't find inventory, is the game running?")
            msg.setWindowTitle("Inventory error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return

        self.i.click(*coords.MENU_ITEMS["inventory"])
        if self.i.check_pixel_color(*coords.INVENTORY_SANITY):
            print("in inventory")
        else:
            self.generate_inventory(depth=depth + 1)
        self.i.click(*coords.INVENTORY_PAGE_1)
        bmp = self.i.get_bitmap()
        bmp = bmp.crop((self.i.window.x + 8, self.i.window.y + 8, self.i.window.x + 968, self.i.window.y + 608))
        bmp = bmp.crop((coords.INVENTORY_AREA.x1, coords.INVENTORY_AREA.y1, coords.INVENTORY_AREA.x2, coords.INVENTORY_AREA.y2))
        button_count = 1
        for y in range(5):
            for x in range(12):
                x1 = x * coords.INVENTORY_SLOT_WIDTH
                y1 = y * coords.INVENTORY_SLOT_HEIGHT
                x2 = x1 + coords.INVENTORY_SLOT_WIDTH
                y2 = y1 + coords.INVENTORY_SLOT_WIDTH
                slot = bmp.crop((x1, y1, x2, y2))
                button = getattr(self, f"pushButton_{button_count}")
                pixmap = self.pil2pixmap(slot)
                icon = QIcon(pixmap)
                button.setIcon(icon)
                button.setIconSize(pixmap.rect().size())
                button.toggled = False
                button.clicked.connect(self.action_button_clicked)
                button_count += 1

        toggles = self.settings.value(self.mode)
        if toggles is not None:
            for toggle in toggles:
                button = getattr(self, "pushButton_" + toggle)
                button.toggled = True
                button.setStyleSheet("border:3px solid rgb(0, 0, 0)")


class ScriptThread(QThread):
    """Thread class for script."""

    signal = Signal(object)
    settings = QSettings("Kujan", "NGU-Scripts")
    mutex = NguScriptApp.mutex
    selected_script = 1
    duration = 0
    tracker = None
    start_exp = 0
    start_pp = 0
    start_qp = 0
    iteration = 0

    def __init__(self, script):
        """Init thread variables."""
        QThread.__init__(self)
        selected_script = script
        ScriptThread.__setup()

    @staticmethod
    def __setup():
        ScriptThread.duration = int(ScriptThread.settings.value("line_adv_duration", "2"))
        ScriptThread.tracker = Tracker(ScriptThread.duration)
        ScriptThread.start_exp = Stats.xp
        ScriptThread.start_pp = Stats.pp
        ScriptThread.start_qp = Stats.qp
        ScriptThread.iteration = 1

    def run(self):
        """Check which script to run."""
        print("pepega")
        while True:
            print(ScriptThread.tracker.get_rates())
            self.signal.emit(ScriptThread.tracker.get_rates())
            self.signal.emit({"exp": Stats.xp - ScriptThread.start_exp, "pp": Stats.pp - ScriptThread.start_pp, "qp": Stats.qp - ScriptThread.start_qp})
            if ScriptThread.selected_script == 0:
                Stats.track_pp = False
                questing.run()
            if ScriptThread.selected_script == 1:
                Stats.track_qp = False
                itopod.run()
            if ScriptThread.selected_script == 2:
                Stats.track_qp = False
            self.signal.emit({"iteration": ScriptThread.iteration})
            ScriptThread.iteration += 1
            ScriptThread.tracker.progress()


def run():
    """Start GUI thread."""
    app = QApplication(sys.argv)
    GUI = NguScriptApp()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

"""
Ideas
Tools for annoying actions while playing manually (cap all diggers)

TODO:
pass feature object to scripts instead of creating new ones each run and losing members
make equipment merge use the same system as the new inventory merge
"""
