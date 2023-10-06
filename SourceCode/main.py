import ctypes
import os
import random
import sys
import time

from global_hotkeys import *
from pynput.keyboard import Controller, Key
from pynput.mouse import Listener
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import (QAbstractEventDispatcher, QAbstractNativeEventFilter,
                          QEventLoop, QSettings, QSize, QTimer)
from PyQt5.QtGui import QIcon, QKeyEvent, QKeySequence, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QKeySequenceEdit,
                             QLineEdit, QMainWindow, QMessageBox, QRadioButton,
                             QShortcut, QWidget)
from PyQt5.uic import loadUi

from ui_PatternRandomizer import Ui_PatternRandomizer

# for taskbar icon
myappid = u'PatternRandomizer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# i dont understand it


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_PatternRandomizer()
        self.ui.setupUi(self)
        self.initUI()

    # add self.ui to fix
    def initUI(self):  # initialize
        # for WindowIcon
        self.setWindowIcon(QIcon(u":/image/die_icon31024.png"))
        self.numbers = []  # the list of numbers to chose from
        # to give people the chioce to go faster at thier oun risk
        self.ui.TimeSpinBox.setValue(100)
        self.ui.StartBtn.clicked.connect(self.StartBtnFun)
        self.ui.StopBtn.clicked.connect(self.StopBtnFun)
        self.ui.HotkeyBtn.clicked.connect(self.HotkeyBtnFun)
        self.ui.Btn1.clicked.connect(self.Btn1fun)
        self.ui.Btn2.clicked.connect(self.Btn2fun)
        self.ui.Btn3.clicked.connect(self.Btn3fun)
        self.ui.Btn4.clicked.connect(self.Btn4fun)
        self.ui.Btn5.clicked.connect(self.Btn5fun)
        self.ui.Btn6.clicked.connect(self.Btn6fun)
        self.ui.Btn7.clicked.connect(self.Btn7fun)
        self.ui.Btn8.clicked.connect(self.Btn8fun)
        self.ui.Btn9.clicked.connect(self.Btn9fun)
        self.ui.SelectAllBtn.clicked.connect(self.SelectAllfun)
        self.ui.DeselectAllBtn.clicked.connect(self.DeselectAllfun)
        self.MouseListener = None  # for mouse listener
        self.RepeatCounter = 0  # Repat counter
        # to make settings file
        self.Settings = QSettings("PatternRandomizer", "PatternRandomizer")
        self.SettingsConfig()  # to apply settings

    def StartBtnFun(self):  # start the app
        if not self.numbers:  # if list is empty
            pass  # QMessageBox gives an error QObject::setParent: Cannot set parent, new parent is in a different thread
        else:  # if list is not empty
            self.ui.StopBtn.setEnabled(True)  # enable stop button
            self.ui.StartBtn.setEnabled(False)  # disable start button
            self.mainfun()  # run the main function

    def StopBtnFun(self):  # stop the app
        self.ui.StopBtn.setEnabled(False)  # disable stop button
        self.ui.StartBtn.setEnabled(True)  # enable start button
        self.OnClickRadioButtonfun(False)  # stop mouse listener
        self.RepeatCounter = 0  # reset Repat counter

    # Add the number to list and disable it

    def Btn1fun(self):
        self.numbers.append(1)
        self.ui.Btn1.setEnabled(False)

    def Btn2fun(self):
        self.numbers.append(2)
        self.ui.Btn2.setEnabled(False)

    def Btn3fun(self):
        self.numbers.append(3)
        self.ui.Btn3.setEnabled(False)

    def Btn4fun(self):
        self.numbers.append(4)
        self.ui.Btn4.setEnabled(False)

    def Btn5fun(self):
        self.numbers.append(5)
        self.ui.Btn5.setEnabled(False)

    def Btn6fun(self):
        self.numbers.append(6)
        self.ui.Btn6.setEnabled(False)

    def Btn7fun(self):
        self.numbers.append(7)
        self.ui.Btn7.setEnabled(False)

    def Btn8fun(self):
        self.numbers.append(8)
        self.ui.Btn8.setEnabled(False)

    def Btn9fun(self):
        self.numbers.append(9)
        self.ui.Btn9.setEnabled(False)

    def SelectAllfun(self):  # select All
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # fill the list
        buttons = [self.ui.Btn1, self.ui.Btn2, self.ui.Btn3, self.ui.Btn4, self.ui.Btn5, self.ui.Btn6,
                   self.ui.Btn7, self.ui.Btn8, self.ui.Btn9]  # loop and disable all buttons
        for button in buttons:
            button.setEnabled(False)

    def DeselectAllfun(self):  # deselect all
        self.numbers = []  # empty the list
        buttons = [self.ui.Btn1, self.ui.Btn2, self.ui.Btn3, self.ui.Btn4, self.ui.Btn5,
                   self.ui.Btn6, self.ui.Btn7, self.ui.Btn8, self.ui.Btn9]  # loop and enable all buttons
        for button in buttons:
            button.setEnabled(True)

    def mainfun(self):  # main function
        if self.ui.OnClickRadioButton.isChecked():  # to check if checked no need to initialize
            self.OnClickRadioButtonCheckedfun()  # OnClick Radio Button Checked function
        elif self.ui.TimeRadioButton.isChecked():  # to check if checked no need to initialize
            try:  # for globla hotkey
                self.hotkeyFun()  # this fix the disabling of the hotkey
            except Exception:
                pass
            while self.ui.StopBtn.isEnabled():  # while app works
                self.TimeRadioButtonCheckedfun()  # Time Radio Button Checked function
            # bug: prints one more after stopping with hotkey

    def TimeRadioButtonCheckedfun(self):  # Time Radio Button Checked function
        keyboard = Controller()  # for key press
        RandomNumber = str(random.choice(self.numbers))  # the random number
        loop = QEventLoop()  # sleep
        QTimer.singleShot(self.ui.TimeSpinBox.value(), loop.quit)  # sleep
        loop.exec_()  # sleep
        keyboard.press(RandomNumber)  # press random from list
        keyboard.release(RandomNumber)  # release random from list
        if self.ui.RepeatRadioButton.isChecked():  # to check if checked no need to initialize
            self.RepeatCounterFun()  # for RepeatCounter

    # mouse detection code
    def OnClickRadioButtonCheckedfun(self):  # start mouse listener
        self.OnClickRadioButtonfun(True)  # start mouse listener

    def OnClickRadioButtonfun(self, checked):  # for mouse click detection
        if checked:
            # Start the mouse listener
            # link mouse click to OnMouseClick function
            self.MouseListener = Listener(on_click=self.OnMouseClick)
            self.MouseListener.start()
        else:
            # Stop the mouse listener
            if self.MouseListener:
                self.MouseListener.stop()
                self.MouseListener = None

    # what happend after detection
    def OnMouseClick(self, x, y, button, pressed):
        keyboard = Controller()  # for key press
        RandomNumber = str(random.choice(self.numbers))  # the random number
        if pressed:  # solves the double click problem
            keyboard.press(RandomNumber)  # press random from list
            keyboard.release(RandomNumber)  # release random from list
            if self.ui.RepeatRadioButton.isChecked():  # to check if checked no need to initialize
                self.RepeatCounterFun()  # for RepeatCounter

    # hotkey detection code
    # change the text for the buttons and sends the hotkey value to listener
    def HotkeyBtnFun(self):
        if self.ui.shortcut_edit.keySequence().isEmpty():  # if keySequenceEdit is empty
            QMessageBox.warning(
                self, "Invalid Shortcut", "Please enter a valid shortcut.")  # error message
        else:  # if keySequenceEdit is not empty
            try:  # try expect for hotkey length and special characters
                self.HotkeySequence = self.ui.shortcut_edit.keySequence().toString().lower()
                self.hotkeyFun()  # call the hotkey function to assign
                # change button text to add the hotkey
                self.ui.StartBtn.setText(
                    "Start  ({})".format(self.HotkeySequence.upper()))
                # change button text to add the hotkey
                self.ui.StopBtn.setText(
                    "Stop  ({})".format(self.HotkeySequence.upper()))

            # self.shortcut_edit.setEnabled(False)#diable the keySequenceEdit #no need
            except Exception:
                QMessageBox.warning(
                    self, "Invalid Shortcut", "Please enter a valid shortcut.")  # error message

    # for globla hotkey

    def hotkeyFun(self):  # assign the globla hotkey and start listening
        clear_hotkeys()  # clear all hotkeys
        # get hotkey from HotkeySequence
        self.bindings = [[self.HotkeySequence,
                          self.OnHotkeyClick, None, False]]
        register_hotkeys(self.bindings)  # register hotkeys
        start_checking_hotkeys()  # start listening

    # for globla hotkey
    def OnHotkeyClick(self):  # what the hotkey dose when pressed
        if self.ui.StartBtn.isEnabled():  # if app not running
            self.StartBtnFun()  # start app
        elif self.ui.StopBtn.isEnabled():  # if app running
            self.StopBtnFun()  # stop app

    def RepeatCounterFun(self):  # Repeat Radio Button Checked function
        self.RepeatCounter += 1  # for each repeat
        if self.RepeatCounter == self.ui.RepeatSpinBox.value():  # To stop
            self.StopBtnFun()  # To stop

    def SettingsConfig(self):  # applies settings at startup
        # move the window position at startup
        try:  # for first start error
            self.move(self.Settings.value("WindowPosition"))
            # set TimeSpinBox value at startup
            self.ui.TimeSpinBox.setValue(self.Settings.value("TimeSpinBox"))
            # set RepeatSpinBox value at startup
            self.ui.RepeatSpinBox.setValue(
                self.Settings.value("RepeatSpinBox"))
            self.HotkeySequence = (self.Settings.value(
                "HotkeySequence"))  # get the hotkey sequence
            self.ui.shortcut_edit.setKeySequence(
                self.HotkeySequence)  # set Hotkey value at startup
            self.HotkeyBtnFun()  # press save button
        except Exception:
            pass

    # override the closeEvent

    def closeEvent(self, event):  # what happend when closing the app
        # save the position of the window
        self.Settings.setValue("WindowPosition", self.pos())
        # save TimeSpinBox value
        self.Settings.setValue("TimeSpinBox", self.ui.TimeSpinBox.value())
        # save RepeatSpinBox value
        self.Settings.setValue("RepeatSpinBox", self.ui.RepeatSpinBox.value())
        try:
            # save HotkeySequence value
            self.Settings.setValue("HotkeySequence", self.HotkeySequence)
        except Exception:
            pass
        self.StopBtnFun()  # stops running in the background
        stop_checking_hotkeys()  # Stops the hotkey listening
        event.accept()  # IDK
        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
