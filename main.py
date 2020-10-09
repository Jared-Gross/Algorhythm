#!/usr/bin python3
# You should also check the file have the right to be execute. chmod +x main.py
# pip install pywin32-ctypes
import ctypes
import threading
import traceback
import atexit
import random
import time
import glob
import json
import os
import qdarkgraystyle
import qdarkstyle
from datetime import datetime
from string import ascii_lowercase, ascii_uppercase
from Themes.Breeze import breeze_resources
from PyQt5 import uic
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from functools import partial
from moviepy import editor
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub.playback import play
from pydub import AudioSegment
import sys
current_platform = 'Linux' if sys.platform == "linux" or sys.platform == "linux2" else 'Windows'

if current_platform == 'Windows':
    import win32com
# Audio Imports
# pip install pydub

# Video Imports
# Possible .exe build errors
# https://stackoverflow.com/questions/44615249/attributeerror-module-object-has-no-attribute-audio-fadein
# pip install moviepy
# from moviepy.video.VideoClip import resize
# from moviepy.video.VideoClip import VideoClip, ImageClip, ColorClip, TextClip
'''
NOTE make sure you have it installed properly
pip install Wand
sudo apt-get install python-wand
sudo apt-get install libmagickwand-dev
sudo apt-get install imagemagick
sudo apt-get update
sudo apt-get upgrade

if moveipy has wierd errors about not being found on LINUX machines, then is how you fix it:
go to: 
/etc/ImageMagick-6/policy.xml

and at the end usally some where there is this line:
<!-- <policy domain="path" rights="none" pattern="@*" /> -->
comment that out or delete it.

or go to this thread and you will find instructions to fix the error.
https://www.reddit.com/r/moviepy/comments/4nin6q/update_imagemagik_and_moviepy_has_broken/
'''

# GUI Imports
# pip install pyqt5

# Themes
'''
pip install qdarkgraystyle
https://github.com/ColinDuquesnoy/QDarkStyleSheet

pip install qdarkstyle
https://github.com/mstuttgart/qdarkgraystyle

Breeze
https://github.com/Alexhuszagh/BreezeStyleSheets
'''

# Other

if current_platform == 'Linux':
    import webbrowser as wb
    # Only works for linux
    # pip install notify2
    # pip install dbus-python
    import notify2 as notify
elif current_platform == 'Windows':
    import subprocess
    # only works for windows
    # pip install win10toast
    from win10toast import ToastNotifier as notify

'''
To generate a requirements.txt file you need to:
pip install pipreqs

Then run:
pipreqs /path/to/project/folder

To install requirements.txt run:
pip install -r requirements.txt
'''
#                     year, month, day, hour, minute, second
#                               y   m   d  h   m  s
latest_update_date = datetime(2020, 10, 5, 11, 1, 23)
latest_update_date_formated = latest_update_date.strftime(
    "%A %B %d %Y at %X%p")

company = 'TheCodingJs'
title = 'Algorhythm'
version = 'v0.1'


class GenerateThread(QThread):
    generated = pyqtSignal(str, float, object, object,
                           object, object, object, object, str, object, list, list, list)

    def __init__(self, alphabetText, genres_file, seconds, note_types, keys_json, note_states, note_type_states, algorithmName, genreName, progressBar, buttonName, buttonPlay, buttonDelete, labelStatus, comboExport):
        QThread.__init__(self)
        self.genres_file = genres_file
        self.seconds = float(seconds)

        self.note_types = note_types
        self.keys_json = keys_json

        self.all_available_notes = []
        self.all_available_notes_index = []
        self.all_available_note_types = []

        self.note_states = note_states
        self.note_type_states = note_type_states
        self.algorithmName = algorithmName
        self.genreName = genreName

        self.progressBar = progressBar
        self.buttonName = buttonName
        self.buttonPlay = buttonPlay
        self.buttonDelete = buttonDelete
        self.labelStatus = labelStatus
        self.comboExport = comboExport

        self.alphabetText = alphabetText

        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        final_song = None
        self.all_available_notes = []
        self.all_available_note_types = []
        self.all_available_notes_index = []

        self.info_notes = []
        self.info_note_types = []
        self.info_duration_per_note = []

        num = 0
        sum_of_notes = 0
        sum_of_note_types = 0
        order_of_notes = 0
        order_of_note_types = 0
        final_name = ''
        alphabet_finished = False
        with open(self.genres_file) as file:
            genres_json = json.load(file)
            for i, noteState in enumerate(genres_json[0]['Notes'][0]):
                if self.note_states[i] == 'True':
                    self.all_available_notes.append(
                        self.keys_json[0]['keys'][i])
                    self.all_available_notes_index.append(i)
            for i, note in enumerate(genres_json[0]['Note Types'][0]):
                if self.note_type_states[i] == 'True':
                    self.all_available_note_types.append(self.note_types[note])
            while True:
                if self.algorithmName == 'Random':
                    randNote = random.randint(
                        0, len(self.all_available_notes) - 1)
                    randNoteType = random.randint(
                        0, len(self.all_available_note_types) - 1)  # min = 0, max = 5

                    selected_note_type = self.all_available_note_types[randNoteType]
                    num += 1
                    sum_of_notes += randNote
                    sum_of_note_types += selected_note_type
                    self.info_note_types.append(selected_note_type)
                    # min = 0, max = 60
                    note = AudioSegment.from_mp3(
                        f"{piano_samples}{self.all_available_notes[randNote]}.mp3")
                    note = note + 3  # increase audio
                    self.info_notes.append(self.all_available_notes[randNote])
                    note_length = note.duration_seconds * 1000  # milliseconds
                    note = note[:note_length / selected_note_type]
                    self.info_duration_per_note.append(note.duration_seconds)
                    final_song = note if not final_song else final_song + note
                elif 'Step' in self.algorithmName:
                    step_keys = []
                    step_note_keys = []
                    step_available_notes = []
                    step_available_notes_types = []
                    if not step_keys:
                        step_keys, step_note_keys = self.getStepNumberList()
                    if '(-)' in self.algorithmName:
                        step_keys.reverse()
                        step_note_keys.reverse()
                    elif 'Random' in self.algorithmName:
                        random.shuffle(step_keys)
                        random.shuffle(step_note_keys)
                    for index, j in enumerate(step_note_keys):
                        selected_note_type = step_note_keys[index]
                        self.info_note_types.append(selected_note_type)
                        # selected_note_type = step_available_notes_types[i]
                        note = AudioSegment.from_mp3(
                            f"{piano_samples}{step_keys[index]}.mp3")
                        note = note + 3  # increase audio

                        self.info_notes.append(step_keys[index])
                        note_length = note.duration_seconds * 1000  # milliseconds

                        num += 1
                        sum_of_notes += index
                        sum_of_note_types += selected_note_type

                        try:
                            note = note[:note_length / selected_note_type]
                        except ZeroDivisionError:
                            note = note[:note_length / selected_note_type + 1]

                        self.info_duration_per_note.append(
                            note.duration_seconds)
                        final_song = note if not final_song else final_song + note
                        if i == len(step_available_notes):
                            step_keys, step_note_keys = self.getStepNumberList()

                        self.generated.emit('Status: Generating...', (final_song.duration_seconds / self.seconds * 100),
                                            self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                elif self.algorithmName == 'Alphabet':
                    alpha_keys = []
                    alpha_note_keys = []
                    if not alpha_keys:
                        alpha_keys, alpha_note_keys = self.char_to_notes(
                            self.char_to_num(self.alphabetText.toPlainText(), False))
                    final_time = 0
                    for i, j in enumerate(alpha_keys):
                        for o, k in enumerate(j):
                            final_time += 1
                    # final_time = (len(alpha_keys) + 1 * len(alpha_note_keys) + 1)
                    current = 0
                    for i, j in enumerate(alpha_keys):
                        selected_note_type = alpha_note_keys[i]
                        for o, k in enumerate(j):
                            current += 1
                            self.info_notes.append(k)
                            note = AudioSegment.from_mp3(
                                f"{piano_samples}{k}.mp3")

                            num += 1
                            sum_of_notes += o
                            sum_of_note_types += selected_note_type

                            note = note + 3  # increase audio
                            note_length = note.duration_seconds * 1000  # milliseconds
                            note = note[:note_length / selected_note_type]
                            self.info_note_types.append(selected_note_type)
                            self.info_duration_per_note.append(
                                note.duration_seconds)
                            final_song = note if not final_song else final_song + note
                            self.generated.emit('Status: Generating...', ((current / final_time) * 100),
                                                self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                    alphabet_finished = True
                if alphabet_finished or final_song.duration_seconds >= self.seconds:
                    # final_name = (f'{str(first_note)}{str(num)}{str(order_of_notes)}{str(order_of_note_types)}{str(first_note_type)}
                    # self.generated.emit('Status: Saving...', (final_song.duration_seconds / self.seconds * 100),
                    # self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                    final_name = (
                        f'{str(self.algorithmName)} {str(num)}{str(sum_of_notes)}{str(sum_of_note_types)}{str(int(final_song.duration_seconds))}.mp3')
                    final_song.fade_in(6000).fade_out(6000)
                    self.generated.emit('Status: Finished!', (100), self.progressBar, self.buttonName,
                                        self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                    break
                # elif does_song_have_time_limit == False and alphabet_finished == True:
                #     self.generated.emit('Status: Saving...', (final_song.duration_seconds / self.seconds * 100), self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                #     final_name = (f'{str(self.algorithmName)} {str(self.genreName)} {str(final_song.duration_seconds)}{str()}.mp3')
                #     final_song.fade_in(6000).fade_out(6000)
                #     final_song.export(f"{compile_folder}{final_name}", format="mp3")
                #     self.generated.emit('Status: Finished!', (100), self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                #     break
                if not self.running:
                    self.generated.emit('Status: Canceled!', (final_song.duration_seconds / self.seconds * 100),
                                        self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)
                    break

                self.generated.emit('Status: Generating...', (final_song.duration_seconds / self.seconds * 100),
                                    self.progressBar, self.buttonName, self.buttonPlay, self.buttonDelete, self.labelStatus, self.comboExport, final_name, final_song, self.info_notes, self.info_note_types, self.info_duration_per_note)

    def getStepNumberList(self):
        amount_of_numbers = random.randint(4, 13)
        # NOTE TYPES
        note_types_number = []
        startNoteType = random.randint(0, 32)  # Min = 0, Max = 5
        endNoteType = random.randint(startNoteType, 32)
        try:
            stepNoteType = (endNoteType - startNoteType) / \
                (amount_of_numbers - 1)
        except ZeroDivisionError:
            stepNoteType = (endNoteType - startNoteType) / (amount_of_numbers)
        # NOTES
        numbers = []
        step_number_notes = []
        start = random.randint(0, 60)
        if start != 60:
            end = random.randint(start + 1, 60)
        else:
            end = random.randint(start, 60)
        try:
            step = (end - start) / (amount_of_numbers - 1)
        except ZeroDivisionError:
            step = (end - start) / (amount_of_numbers)
        for i in range(amount_of_numbers):
            # In this case we want to start at 1, to simplify things.
            i = i + 1
            if i == 1:
                numbers.append(int(start))  # first number
                note_types_number.append(int(startNoteType))
            if i == 2:
                numbers.append(int(start + step))  # second number
                note_types_number.append(int(startNoteType + stepNoteType))
            if i >= 3 and i < amount_of_numbers:
                # everything in bewtween
                numbers.append(int(start + (i - 1) * step))
                # everything in bewtween
                note_types_number.append(
                    int(startNoteType + (i - 1) * stepNoteType))
            if i == amount_of_numbers:
                numbers.append(
                    int(start + (amount_of_numbers - 1) * step))  # end
                note_types_number.append(
                    int(startNoteType + (amount_of_numbers - 1) * stepNoteType))  # end
        closest_numbers = []
        closest_numbers_note_types = []
        for i, j in enumerate(numbers):
            closest_numbers.append(self.closest(
                self.all_available_notes_index, j))
        for i, j in enumerate(note_types_number):
            closest_numbers_note_types.append(
                self.closest(self.all_available_note_types, j))
        for i, j in enumerate(closest_numbers):
            step_number_notes.append(keys_json[0]['keys'][j])
        return step_number_notes, closest_numbers_note_types

    def char_to_num(self, words, useLowerCase=False):
        # Toggle this to only use 1-26 numbers
        if useLowerCase:
            words = words.lower()
        output = []
        for s in words.split(' '):
            temp_list = []
            for i, j in enumerate(s):
                for o, k in enumerate(alphabetList):
                    if j == k:
                        temp_list.append(alphabetValList[o])
            output.append(temp_list)
        return output

    def char_to_notes(self, list_of_numbers):
        alphabet_note_types = []
        alphabet_notes_index = []
        alphabet_notes = []
        for i, j in enumerate(list_of_numbers):
            temp_list = []
            alphabet_note_types.append(self.closest(
                self.all_available_note_types, len(j)))
            for o, k in enumerate(j):
                temp_list.append(self.closest(
                    self.all_available_notes_index, k))
            alphabet_notes_index.append(temp_list)
        for i, j in enumerate(alphabet_notes_index):
            temp_list = []
            for o, k in enumerate(j):
                temp_list.append(keys_json[0]['keys'][k])
            alphabet_notes.append(temp_list)
        return alphabet_notes, alphabet_note_types

    def closest(self, lst, K):
        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


class mainwindowUI(QMainWindow):

    def __init__(self):
        super(mainwindowUI, self).__init__()
        uic.loadUi(UI_folder + 'mainwindow.ui', self)
        self.setWindowTitle(title + ' ' + version)
        self.setWindowIcon(QIcon(os.path.dirname(
            os.path.realpath(__file__)) + "/icon.png"))
        if current_platform == 'Windows':
            appid = u'{}.{}.{}'.format(company, title, version)
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                appid)
        self.show()
        self.center()
        self.load_theme()

        self.load_VAR()
        self.load_UI()
        self.UINotes()
        self.updateNotes()
        self.checkAlgorithm()
        self.setFixedSize(810, 590)

    def load_UI(self):
        self.miscLabels = []
        self.label_8 = self.findChild(QLabel, 'label_8')
        self.label_7 = self.findChild(QLabel, 'label_7')
        self.miscLabels.append(self.label_7)
        self.miscLabels.append(self.label_8)

        self.btnGenerate = self.findChild(QPushButton, 'btnGenerate_2')
        self.btnGenerate.clicked.connect(partial(self.btnGenerateClicked))
        self.btnGenerate.setToolTip('Start generating music.')

        self.generatedMusicLayout = self.findChild(
            QFrame, 'generatedMusicLayout_2')
        self.generatedMusicLayout.setHidden(True)

        self.btnDeleteAll = self.findChild(QPushButton, 'btnDeleteAll')
        self.btnDeleteAll.clicked.connect(
            partial(self.btnDeleteAllFiles, self.btnDeleteAllList))
        self.btnDeleteAll.setEnabled(False)
        self.btnDeleteAll.setToolTip(
            'Deletes all: \n(.mp3)\n(.mp4)\n\n that were recently saved.')

        self.alphabetText = self.findChild(QTextEdit, 'alphabetText')
        self.alphabetText.setHidden(True)
        self.alphabetText.setPlaceholderText("Enter some text here...")

        self.btnCancelThreads = self.findChild(QPushButton, 'btnCancelThreads')
        self.btnCancelThreads.clicked.connect(self.stop_generation_threads)
        self.btnCancelThreads.setEnabled(False)
        self.btnCancelThreads.setToolTip('Cancels all music generation.')

        self.btnClear = self.findChild(QPushButton, 'btnClear')
        self.btnClear.clicked.connect(self.btnClearGrid)
        self.btnClear.setEnabled(False)
        self.btnClear.setToolTip('Removes all generated music.')

        self.lblInputSongLength = self.findChild(QLabel, 'label_3')
        self.inputSongLength = self.findChild(
            QDoubleSpinBox, 'inputSongLength_4')

        self.genAlgorithms = self.findChild(QComboBox, 'genAlgorithms_4')
        self.genAlgorithms.setToolTip(
            'Diffrent algorithms of music generation.')
        for i, j in enumerate(self.algorithms):
            if i == 1 or i == 3:
                self.genAlgorithms.insertSeparator(i)
            self.genAlgorithms.addItem(j)
        self.genAlgorithms.currentIndexChanged.connect(self.checkAlgorithm)
        self.genAlgorithms.setToolTip('Music Generation Algorithms.')
        self.genAlgorithms.setCurrentIndex(lastSelectedAlgorithm[0])

        self.genresComboBox = self.findChild(QComboBox, 'genresComboBox')
        self.refreshNoteSettingComboBox()
        self.genresComboBox.currentIndexChanged.connect(self.updateNotes)
        self.genresComboBox.setCurrentIndex(lastSelectedGenre[0])

        self.comboMultiplier = self.findChild(QComboBox, 'comboMultiplier')
        self.comboMultiplier.addItems(self.mulitpliers)
        self.comboMultiplier.setToolTip(
            'Generate more music at a time with one click.')

        self.NoteGridLayout = self.findChild(QGridLayout, 'NoteGridLayout')
        self.NoteTypeGridLayout = self.findChild(
            QGridLayout, 'NoteTypeGridLayout')
        self.gridMusicProgressGridLayout = self.findChild(
            QGridLayout, 'gridMusicProgress')

        self.actionExport = self.findChild(QAction, 'actionExport')
        self.actionExport.setStatusTip('Export all saved genres to *.csv')

        self.actionPrefrences = self.findChild(QAction, 'actionTheme')
        self.actionPrefrences.setStatusTip('Change window settings.')
        self.actionPrefrences.triggered.connect(self.open_settings_window)

        self.actionAbout_Qt = self.findChild(QAction, 'actionAbout_Qt')
        self.actionAbout_Qt.triggered.connect(qApp.aboutQt)

        self.actionAbout = self.findChild(QAction, 'actionAbout')
        self.actionAbout.triggered.connect(self.open_about_window)

        self.actionLicense = self.findChild(QAction, 'actionLicense')
        self.actionLicense.triggered.connect(self.open_license_window)

        # Adding item on the menu bar
        # self.tray = QSystemTrayIcon()
        # self.tray.setIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + "/icon.png"))
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.dirname(
            os.path.realpath(__file__)) + "/icon.png"))

        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def load_VAR(self):
        self.algorithms = [
            'Random', 'Step (+)', 'Step (-)', 'Step Random', 'Alphabet']
        self.algorithms.sort()
        self.mulitpliers = ['1', '2', '5', '10']

        self.threads = []
        self.btnDeleteAllList = []
        self.delete_how_many_files = 0
        self.genres_folder = genres_folder
        self.all_genre_files = all_genre_files
        self.genre_names = genre_names

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def load_theme(self):
        QApplication.setPalette(QApplication.palette())
        global originalPalette
        if originalPalette == None:
            originalPalette = QApplication.palette()
        if CSSOn[0] == 'True':
            self.setStyleSheet(open(themes_folder + "style.qss", "r").read())
        else:
            self.setStyleSheet('')
        if DefaultMode[0] == 'True':
            if current_platform == 'Windows':
                app.setStyle('Windowsvista')
            elif current_platform == 'Linux':
                app.setStyle('Fusion')
            QApplication.setPalette(originalPalette)
            app.setStyleSheet('')
        if LightMode[0] == 'True':
            if lastSelectedTheme[0] == 'Fusion' or lastSelectedTheme[0] == 'windowsvista':
                app.setPalette(QApplication.style().standardPalette())
                palette = QPalette()
                gradient = QLinearGradient(0, 0, 0, 400)
                gradient.setColorAt(0.0, QColor(240, 240, 240))
                gradient.setColorAt(1.0, QColor(215, 215, 215))
                palette.setColor(QPalette.ButtonText, Qt.black)
                palette.setBrush(QPalette.Window, QBrush(gradient))
                app.setPalette(palette)
                app.setStyle(lastSelectedTheme[0])
                app.setStyleSheet('')
            elif lastSelectedTheme[0] == 'Breeze':
                file = QFile(themes_folder + 'Breeze/light.qss')
                file.open(QFile.ReadOnly | QFile.Text)
                stream = QTextStream(file)
                app.setStyleSheet(stream.readAll())
        if DarkMode[0] == 'True':
            if lastSelectedTheme[0] == 'Fusion' or lastSelectedTheme[0] == 'windowsvista':
                palette = QPalette()
                gradient = QLinearGradient(0, 0, 0, 400)
                gradient.setColorAt(0.0, QColor(40, 40, 40))
                gradient.setColorAt(1.0, QColor(30, 30, 30))
                palette.setBrush(QPalette.Window, QBrush(gradient))
                palette.setColor(QPalette.WindowText, Qt.white)
                palette.setColor(QPalette.Base, QColor(25, 25, 25))
                palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
                palette.setColor(QPalette.ToolTipBase, Qt.black)
                palette.setColor(QPalette.ToolTipText, Qt.white)
                palette.setColor(QPalette.Text, Qt.white)
                palette.setColor(QPalette.Button, QColor(30, 30, 30))
                palette.setColor(QPalette.ButtonText, Qt.white)
                palette.setColor(QPalette.BrightText, Qt.red)
                palette.setColor(QPalette.Link, QColor(42, 130, 218))
                palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
                palette.setColor(QPalette.HighlightedText, Qt.black)
                app.setPalette(palette)
                app.setStyle(lastSelectedTheme[0])
                app.setStyleSheet('')
            elif lastSelectedTheme[0] == 'Breeze':
                file = QFile(themes_folder + 'Breeze/dark.qss')
                file.open(QFile.ReadOnly | QFile.Text)
                stream = QTextStream(file)
                app.setStyleSheet(stream.readAll())
            elif lastSelectedTheme[0] == 'qdarkstyle':
                QApplication.setPalette(originalPalette)
                app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            elif lastSelectedTheme[0] == 'qdarkgraystyle':
                QApplication.setPalette(originalPalette)
                app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    def UINotes(self):
        try:
            colSize = 12
            for i, j in enumerate(keys_json[0]['keys']):
                self.btnNote = QPushButton(j)
                self.btnNote.setCheckable(True)
                self.btnNote.setChecked(
                    True if note_states[i] == 'True' else False)
                self.btnNote.clicked.connect(
                    partial(self.btnNoteClick, j, i, self.btnNote, True))
                if '#' in j or 'b' in j:
                    self.btnNote.setToolTip(
                        f'{j[0]} Sharp {j[2]}' if '#' in j else f'{j[0]} Flat {j[2]}')
                    self.btnNote.setObjectName(
                        'blackOn' if note_states[i] == 'True' else 'blackOff')
                    self.btnNote.setFixedSize(34, 64)
                else:
                    self.btnNote.setToolTip(f'{j}')
                    self.btnNote.setObjectName(
                        'whiteOn' if note_states[i] == 'True' else 'whiteOff')
                    self.btnNote.setFixedSize(42, 64)
                self.NoteGridLayout.addWidget(
                    self.btnNote, i / colSize, i % colSize)
            for i, j in enumerate(note_types):
                self.btnNoteType = QPushButton()
                self.btnNoteType.setFixedSize(72, 72)
                self.btnNoteType.setToolTip(j)
                self.btnNoteType.setCheckable(True)
                self.btnNoteType.setChecked(
                    True if note_type_states[i] == 'True' else False)
                self.btnNoteType.setIcon(QIcon(f'{image_folder}{j}.png'))
                self.btnNoteType.setIconSize(QSize(42, 42))
                self.btnNoteType.setObjectName(
                    "whiteOn" if note_type_states[i] == 'True' else "whiteOff")

                self.btnNoteType.clicked.connect(
                    partial(self.btnNoteClick, j, i, self.btnNoteType, False))
                self.NoteTypeGridLayout.setColumnStretch(0, 3)
                self.NoteTypeGridLayout.addWidget(
                    self.btnNoteType, i / 2, i % 2)
        except:
            print('no generes')

    def btnNoteClick(self, name, index, state, play):
        global genres_json, note_states, note_type_states
        temp_note_type_list_states = note_type_states
        temp_note_list_states = note_states
        for i, j in enumerate(note_types):
            if j == name:
                temp_note_type_list_states[i] = 'False' if temp_note_type_list_states[i] == 'True' else 'True'
        for i, j in enumerate(keys_json[0]['keys']):
            if j == name:
                temp_note_list_states[i] = 'False' if temp_note_list_states[i] == 'True' else 'True'
        genres_json.pop(0)
        genres_json.append(
            {"Name": [str(self.genresComboBox.currentText())], "Notes": [{"C1": [str(temp_note_list_states[0])], "C#1": [str(temp_note_list_states[1])], "D1": [str(temp_note_list_states[2])], "Eb1": [str(temp_note_list_states[3])], "E1": [str(temp_note_list_states[4])], "F1": [str(temp_note_list_states[5])], "F#1": [str(temp_note_list_states[6])], "G1": [str(temp_note_list_states[7])], "Ab1": [str(temp_note_list_states[8])], "A1": [str(temp_note_list_states[9])], "Bb1": [str(temp_note_list_states[10])], "B1": [str(temp_note_list_states[11])], "C2": [str(temp_note_list_states[12])], "C#2": [str(temp_note_list_states[13])], "D2": [str(temp_note_list_states[14])], "Eb2": [str(temp_note_list_states[15])], "E2": [str(temp_note_list_states[16])], "F2": [str(temp_note_list_states[17])], "F#2": [str(temp_note_list_states[18])], "G2": [str(temp_note_list_states[19])], "Ab2": [str(temp_note_list_states[20])], "A2": [str(temp_note_list_states[21])], "Bb2": [str(temp_note_list_states[22])], "B2": [str(temp_note_list_states[23])], "C3": [str(temp_note_list_states[24])], "C#3": [str(temp_note_list_states[25])], "D3": [str(temp_note_list_states[26])], "Eb3": [str(temp_note_list_states[27])], "E3": [str(temp_note_list_states[28])], "F3": [str(temp_note_list_states[29])], "F#3": [str(temp_note_list_states[30])], "G3": [str(temp_note_list_states[31])], "Ab3": [str(temp_note_list_states[32])], "A3": [str(temp_note_list_states[33])], "Bb3": [str(temp_note_list_states[34])], "B3": [str(temp_note_list_states[35])], "C4": [str(temp_note_list_states[36])], "C#4": [str(temp_note_list_states[37])], "D4": [str(temp_note_list_states[38])], "Eb4": [str(temp_note_list_states[39])], "E4": [str(temp_note_list_states[40])], "F4": [str(temp_note_list_states[41])], "F#4": [str(temp_note_list_states[42])], "G4": [str(temp_note_list_states[43])], "Ab4": [str(temp_note_list_states[44])], "A4": [str(temp_note_list_states[45])], "Bb4": [str(temp_note_list_states[46])], "B4": [str(temp_note_list_states[47])], "C5": [str(temp_note_list_states[48])], "C#5": [str(temp_note_list_states[49])], "D5": [str(temp_note_list_states[50])], "Eb5": [str(temp_note_list_states[51])], "E5": [str(temp_note_list_states[52])], "F5": [str(temp_note_list_states[53])], "F#5": [str(temp_note_list_states[54])], "G5": [str(temp_note_list_states[55])], "Ab5": [str(temp_note_list_states[56])], "A5": [str(temp_note_list_states[57])], "Bb5": [str(temp_note_list_states[58])], "B5": [str(temp_note_list_states[59])], "C6": [str(temp_note_list_states[60])]}], "Note Types": [{"Semibreve": [str(temp_note_type_list_states[0])], "Minim": [str(temp_note_type_list_states[1])], "Crochet": [str(temp_note_type_list_states[2])], "Quaver": [str(temp_note_type_list_states[3])], "Semiquaver": [str(temp_note_type_list_states[4])], "Demisemiquaver": [str(temp_note_type_list_states[5])]}]})
        with open(genres_file, mode='w+', encoding='utf-8') as file:
            json.dump(genres_json, file, ensure_ascii=True, indent=4)
        note_states.clear()
        note_type_states.clear()
        with open(genres_file) as file:
            genres_json = json.load(file)
            for i, noteState in enumerate(genres_json[0]['Notes']):
                for j, k in enumerate(keys_json[0]['keys']):
                    note_states.append(noteState[str(k)][0])
            for i, noteState in enumerate(genres_json[0]['Note Types']):
                for j, k in enumerate(note_types):
                    note_type_states.append(noteState[str(k)][0])
        self.clearLayout(self.NoteGridLayout)
        self.clearLayout(self.NoteTypeGridLayout)
        self.UINotes()
        if play:
            threading.Thread(target=self.playNote, args=(index,)).start()

        # if play: self.playNote(index)

    def btnPlayMediaClick(self, audio_file, file_name):
        threading.Thread(target=self.threadPlayMedia,
                         args=(audio_file, file_name,)).start()

    def threadPlayMedia(self, audio_file, file_name):
        try:
            file_name = file_name.replace('.mp3', ' A.mp3')
            audio_file.export(f"{compile_folder}{file_name}", format="mp3")
            audio = AudioSegment.from_mp3(f'{compile_folder}{file_name}')
            play(audio)
            os.remove(f'{compile_folder}{file_name}')
        except PermissionError as e:
            self.OpenErrorDialog('Permission Denied', e)
            return
        except FileNotFoundError as e:
            self.OpenErrorDialog('File Not Found', e)
            return

    def playNote(self, i):
        try:
            note = AudioSegment.from_mp3(
                f"{piano_samples}{keys_json[0]['keys'][i]}.mp3")
            play(note)
        except PermissionError as e:
            self.OpenErrorDialog('Permission Denied', e)
            return
        except FileNotFoundError as e:
            self.OpenErrorDialog('File Not Found', e)
            return

    @pyqtSlot(str)
    def OpenErrorDialog(self, title, text):
        QMessageBox.critical(
            self, f'{title}', f"{text}", QMessageBox.Ok, QMessageBox.Ok)

    def btnGenerateClicked(self):
        all_available_notes = []
        all_available_note_types = []

        try:
            with open(genres_file) as file:
                genres_json = json.load(file)
                for i, noteState in enumerate(genres_json[0]['Notes'][0]):
                    if note_states[i] == 'True':
                        all_available_notes.append(keys_json[0]['keys'][i])
                for i, note in enumerate(genres_json[0]['Note Types'][0]):
                    if note_type_states[i] == 'True':
                        all_available_note_types.append(note_types[note])
        except:
            ret = QMessageBox.warning(self, 'No genre files', "Must create a genere file to generate music.\n\nWould you like to create a genre?",
                                      QMessageBox.Yes |
                                      QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                self.createGenere()
            return
        if self.genAlgorithms.currentText() == 'Alphabet' and self.alphabetText.toPlainText() == '' or self.alphabetText.toPlainText() == ' ':
            self.OpenErrorDialog(
                'No text', 'No text to generate music, must have atleast one charecter')
            return
        if len(all_available_notes) == 0:
            self.OpenErrorDialog(
                'No notes', 'No notes to select, must have atleast one.')
            return
        if len(all_available_note_types) == 0:
            self.OpenErrorDialog(
                'No note types', 'No note types to select, must have atleast one.')
            return
        if len(all_available_note_types) > 0 and len(all_available_notes) > 0:
            self.btnDeleteAll.setEnabled(False)
            self.btnClear.setEnabled(False)
            for i, j in enumerate(range(int(self.comboMultiplier.currentText()))):
                global total
                total += 1
                self.progressBar = QProgressBar()
                self.btnDelete = QPushButton()
                self.btnDelete.setIcon(self.style().standardIcon(
                    getattr(QStyle, 'SP_DialogDiscardButton')))
                self.btnDelete.setEnabled(False)

                self.lblStatus = QLabel('Status: Generating...')

                self.btnName = QPushButton(str(total) + '. ')
                self.btnName.setFlat(True)
                self.btnName.clicked.connect(
                    partial(self.btnOpenPath, compile_folder))
                self.btnName.setIcon(self.style().standardIcon(
                    getattr(QStyle, 'SP_DirOpenIcon')))

                self.btnPlay = QPushButton()
                self.btnPlay.setEnabled(False)
                self.btnPlay.setIcon(self.style().standardIcon(
                    getattr(QStyle, 'SP_MediaPlay')))

                self.comboExport = QComboBox()
                self.comboExport.setEnabled(False)
                self.comboExport.addItem('Save As...')
                self.comboExport.addItem('Audio')
                if current_platform == 'Linux':
                    self.comboExport.addItem('Video')
                # self.comboExport.addItem('')

                self.gridMusicProgressGridLayout.addWidget(
                    self.btnName, total, 0)
                self.gridMusicProgressGridLayout.addWidget(
                    self.progressBar, total, 1)
                self.gridMusicProgressGridLayout.addWidget(
                    self.lblStatus, total, 2)
                self.gridMusicProgressGridLayout.addWidget(
                    self.btnPlay, total, 3)
                self.gridMusicProgressGridLayout.addWidget(
                    self.btnDelete, total, 4)
                self.gridMusicProgressGridLayout.addWidget(
                    self.comboExport, total, 5)

                threading.Thread(target=self.generate_song, args=(self.genAlgorithms.currentText(
                ), self.progressBar, self.btnName, self.btnPlay, self.btnDelete, self.lblStatus, self.comboExport,)).start()

                loop = QEventLoop()
                QTimer.singleShot(10, loop.quit)
                loop.exec_()

    def btnOpenPath(self, path):
        if current_platform == 'Linux':
            wb.open(path)
        elif current_platform == 'Windows':
            FILEBROWSER_PATH = os.path.join(
                os.getenv('WINDIR'), 'explorer.exe')
            path = os.path.normpath(path)
            if os.path.isdir(path):
                subprocess.run([FILEBROWSER_PATH, path])
            elif os.path.isfile(path):
                subprocess.run(
                    [FILEBROWSER_PATH, '/select,', os.path.normpath(path)])

    def btnDeleteAllFiles(self, filesToDelete):
        self.delete_how_many_files = 0
        for i, j in enumerate(filesToDelete):
            threading.Thread(target=self.btnDeleteFile, args=(
                j[0], True, False)).start()
        else:
            threading.Thread(target=self.btnDeleteFile, args=(
                j[0], True, True)).start()

    def btnDeleteFile(self, path, deleteAllFiles=False, final=False):
        try:
            if not deleteAllFiles:
                self.delete_how_many_files = 0
            for i in range(2):
                if os.path.isfile(path) or os.path.islink(path):
                    os.remove(path)  # remove the file
                    self.delete_how_many_files += 1
                path = path.replace('.mp3', '.mp4')
            if not self.delete_how_many_files == 0 and final:
                grammerFix = 'file' if self.delete_how_many_files == 1 else 'files'
                self.send_notification(
                    'Deleted', f'Successfully deleted {self.delete_how_many_files} {grammerFix}.')
        except Exception as e:
            print(e)

    def send_notification(self, header, message):
        # path to notification window icon
        ICON_PATH = os.path.realpath(__file__) + '/icon.png'
        duration_sec = 3
        if current_platform == 'Linux':
            # initialise the d-bus connection
            notify.init(title)
            # create Notification object
            n = notify.Notification(None, icon=ICON_PATH)
            # set urgency level
            n.set_urgency(notify.URGENCY_NORMAL)
            # set timeout for a notification
            n.set_timeout(duration_sec * 1000)  # milliseconds
            # update notification data for Notification object
            n.update(header, message)
            # show notification on screen
            n.show()
        elif current_platform == 'Windows':
            # One-time initialization
            n = notify()
            # Show notification whenever needed
            n.show_toast(header, message, threaded=True,
                         icon_path=ICON_PATH, duration=duration_sec)  # 3 seconds

    def createGenere(self):
        text, okPressed = QInputDialog.getText(
            self, "Name", "Enter Genre name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            if not text.endswith('.json'):
                file_name = self.genres_folder + text + '.json'
            with open(file_name, 'w+') as f:
                textToWrite = '[{"Name":["' + text + '"],"Notes":[{"C1":["True"],"C#1":["True"],"D1":["True"],"Eb1":["True"],"E1":["True"],"F1":["True"],"F#1":["True"],"G1":["True"],"Ab1":["True"],"A1":["True"],"Bb1":["True"],"B1":["True"],"C2":["True"],"C#2":["True"],"D2":["True"],"Eb2":["True"],"E2":["True"],"F2":["True"],"F#2":["True"],"G2":["True"],"Ab2":["True"],"A2":["True"],"Bb2":["True"],"B2":["True"],"C3":["True"],"C#3":["True"],"D3":["True"],"Eb3":["True"],"E3":["True"],"F3":["True"],"F#3":["True"],"G3":["True"],"Ab3":["True"],"A3":["True"],"Bb3":["True"],"B3":["True"],"C4":["True"],"C#4":["True"],"D4":["True"],"Eb4":["True"],"E4":["True"],"F4":["True"],"F#4":["True"],"G4":["True"],"Ab4":["True"],"A4":["True"],"Bb4":["True"],"B4":["True"],"C5":["True"],"C#5":["True"],"D5":["True"],"Eb5":["True"],"E5":["True"],"F5":["True"],"F#5":["True"],"G5":["True"],"Ab5":["True"],"A5":["True"],"Bb5":["True"],"B5":["True"],"C6":["True"]}],"Note Types":[{"Semibreve":["True"],"Minim":["True"],"Crochet":["True"],"Quaver":["True"],"Semiquaver":["True"],"Demisemiquaver":["True"]}]}]'
                f.write(textToWrite)
        self.genresComboBox.setCurrentIndex(0)
        self.refreshNoteSettingComboBox()
        self.updateNotes()

    def deleteGenere(self):
        text, okPressed = QInputDialog().getItem(self, "Select one to delete.",
                                                 "Generes:", genre_names, 0, False)
        if okPressed:
            for i in self.all_genre_files:
                i = i.replace(self.genres_folder, '')
                i = i.replace('.json', '')
                if text == i:
                    if not text.endswith('.json'):
                        os.remove(self.genres_folder + text + '.json')
                    else:
                        os.remove(self.genres_folder + text)
        self.refreshNoteSettingComboBox()
        self.updateNotes()
        if not len(genre_names) == 1:
            self.genresComboBox.setCurrentIndex(0)

    def refreshNoteSettingComboBox(self):
        index = 0
        try:
            global genres_json, note_states, note_type_states, genres_file
            self.genresComboBox.clear()
            self.genre_names.clear()
            self.all_genre_files = [f for f in glob.glob(
                self.genres_folder + "**/*.json", recursive=True)]
            genres_file = self.all_genre_files[0]
            for i in self.all_genre_files:
                i = i.replace(self.genres_folder, '')
                i = i.replace('.json', '')
                self.genre_names.append(i)
                index += 1
            self.genresComboBox.addItems(self.genre_names)
        except IndexError:
            self.genresComboBox.addItem('')
            self.genresComboBox.addItem('Create')
            self.genresComboBox.setItemIcon(
                index + 1, QIcon(image_folder + 'Create.png'))
            return
        self.genresComboBox.insertSeparator(index + 1)
        self.genresComboBox.addItem('Create')
        self.genresComboBox.setItemIcon(
            index + 1, QIcon(image_folder + 'Create.png'))
        self.genresComboBox.addItem('Delete')
        self.genresComboBox.setItemIcon(
            index + 2, QIcon(image_folder + 'Delete.png'))
        self.genresComboBox.setIconSize(QSize(20, 20))
        # self.UINotes()

    def updateNotes(self):
        global genres_json, note_states, note_type_states, genres_file
        if self.genresComboBox.currentText() == 'Create':
            self.UINotes()
            self.createGenere()
            return
        if self.genresComboBox.currentText() == 'Delete':
            self.UINotes()
            self.deleteGenere()
            return
        note_states.clear()
        note_type_states.clear()
        try:
            config_json.pop(0)
            config_json.append(
                {
                    "Default": [str(DefaultMode[0])],
                    "Dark": [str(DarkMode[0])],
                    "Light": [str(LightMode[0])],
                    "CSS": [str(CSSOn[0])],
                    "Last Genre": [int(self.genresComboBox.currentIndex())],
                    "Last Theme": [str(lastSelectedTheme[0])],
                    "Last Algorithm": [int(lastSelectedAlgorithm[0])]
                })
            with open(config_file, mode='w+', encoding='utf-8') as file:
                json.dump(config_json, file, ensure_ascii=True)
            self.reload_config_file()
            genres_file = self.all_genre_files[self.genresComboBox.currentIndex(
            )]
            with open(genres_file) as file:
                genres_json = json.load(file)
                for i, noteState in enumerate(genres_json[0]['Notes']):
                    for j, k in enumerate(keys_json[0]['keys']):
                        note_states.append(noteState[str(k)][0])
                for i, noteState in enumerate(genres_json[0]['Note Types']):
                    for j, k in enumerate(note_types):
                        note_type_states.append(noteState[str(k)][0])
        except FileNotFoundError:
            pass
        except IndexError:
            pass
        self.clearLayout(self.NoteGridLayout)
        self.clearLayout(self.NoteTypeGridLayout)
        self.UINotes()

    def checkAlgorithm(self):
        if self.genAlgorithms.currentText() == 'Alphabet':
            self.alphabetText.setHidden(False)
            [img.setHidden(True) for img in self.miscLabels]
            self.inputSongLength.setHidden(True)
            self.lblInputSongLength.setHidden(True)
        else:
            self.alphabetText.setHidden(True)
            [img.setHidden(False) for img in self.miscLabels]
            self.inputSongLength.setHidden(False)
            self.lblInputSongLength.setHidden(True)

        config_json.pop(0)
        config_json.append(
            {
                "Default": [str(DefaultMode[0])],
                "Dark": [str(DarkMode[0])],
                "Light": [str(LightMode[0])],
                "CSS": [str(CSSOn[0])],
                "Last Genre": [int(lastSelectedGenre[0])],
                "Last Theme": [str(lastSelectedTheme[0])],
                "Last Algorithm": [int(self.genAlgorithms.currentIndex())]
            })
        with open(config_file, mode='w+', encoding='utf-8') as file:
            json.dump(config_json, file, ensure_ascii=True)
        self.reload_config_file()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
        self.btnDeleteAllList.clear()
        self.generatedMusicLayout.setHidden(True)
        self.btnDeleteAll.setEnabled(False)
        self.btnClear.setEnabled(False)

    def stop_generation_threads(self):
        for generator in self.threads:
            # generator.terminate()
            generator.stop()
            generator.wait()
        self.threads.clear()
        self.unsetCursor()
        self.btnDeleteAll.setEnabled(False)
        self.btnClear.setEnabled(True)

    def start_generation(self, progressBar, buttonName, buttonPlay, buttonDelete, labelStatus, comboExport):
        self.generatedMusicLayout.setHidden(False)
        # self.thread.clear()
        generator = GenerateThread(self.alphabetText, genres_file, self.inputSongLength.text(), note_types, keys_json, note_states, note_type_states,
                                   self.genAlgorithms.currentText(), self.genresComboBox.currentText(), progressBar, buttonName, buttonPlay, buttonDelete, labelStatus, comboExport)
        generator.generated.connect(self.on_data_ready)
        self.threads.append(generator)
        generator.start()

    def on_data_ready(self, lblStatus, progress, progressBar, buttonName, buttonPlay, buttonDelete, labelStatus, comboExport, final_name, audio_file, info_notes, info_note_types, info_duration_per_note):
        try:
            if progress == 100 and lblStatus == 'Status: Finished!':
                temp_list = []
                temp_list.append(compile_folder + final_name)
                self.btnDeleteAllList.append(temp_list)
                self.unsetCursor()
                name = final_name.replace('.mp3', '')
                buttonName.setText(buttonName.text() + name)
                buttonPlay.setEnabled(True)
                buttonPlay.setToolTip(f'Plays {final_name}')
                buttonDelete.setEnabled(True)
                buttonDelete.setToolTip(
                    f'Deletes both:\n{name}.mp3\n{name}.mp4\n\nif they are saved')
                comboExport.setEnabled(True)
                comboExport.currentIndexChanged.connect(partial(
                    self.exportFiles, comboExport, labelStatus, buttonName, final_name, audio_file, info_notes, info_note_types, info_duration_per_note))
                self.btnDeleteAll.setEnabled(True)
                self.btnClear.setEnabled(True)
                self.btnCancelThreads.setEnabled(False)
                buttonDelete.clicked.connect(partial(
                    self.btnDeleteFile, compile_folder + final_name, False, True))
                buttonPlay.clicked.connect(
                    partial(self.btnPlayMediaClick, audio_file, final_name))
            elif lblStatus == 'Status: Canceled!':
                self.btnClear.setEnabled(True)
                self.btnCancelThreads.setEnabled(False)
            else:
                comboExport.setEnabled(False)
                buttonPlay.setEnabled(False)
                buttonDelete.setEnabled(False)
                self.btnDeleteAll.setEnabled(False)
                self.btnClear.setEnabled(False)
                self.btnCancelThreads.setEnabled(True)
            labelStatus.setText(lblStatus)
            progressBar.setValue(progress)
        except Exception as e:
            print(e)

    def exportFiles(self, comboExport, labelStatus, buttonName, file_name, audio_file, info_notes, info_note_types, info_duration_per_note):
        fileName = file_name.replace('.mp3', '')
        default_filename = compile_folder + fileName
        directoryAndFile = ''
        extension = ''

        if comboExport.currentText() == 'Audio':
            directoryAndFile, extension = QFileDialog.getSaveFileName(
                self, "Save audio file", default_filename, f"mp3 (*.mp3)")
            if not directoryAndFile or not extension:
                comboExport.setCurrentIndex(0)
                return
        elif comboExport.currentText() == 'Video':
            directoryAndFile, extension = QFileDialog.getSaveFileName(
                self, "Save video file", default_filename, f"mp4 (*.mp4);;.webm (*.webm)")
            if not directoryAndFile or not extension:
                comboExport.setCurrentIndex(0)
                return
        file_extension = extension.split('*')[-1].replace(')', '')
        self.setCursor(Qt.BusyCursor)
        threading.Thread(target=self.exportFilesThread, args=(comboExport, labelStatus, buttonName,
                                                              directoryAndFile, file_extension, audio_file,
                                                              info_notes, info_note_types, info_duration_per_note,)).start()

    def exportFilesThread(self, comboExport, labelStatus, buttonName, file_name, file_extension, audio_file, info_notes, info_note_types, info_duration_per_note):
        width = 640
        height = 360
        if comboExport.currentText() == 'Audio':
            comboExport.setCurrentIndex(0)
            labelStatus.setText('Status: Saving!')
            audio_file.export(f"{file_name}", format="mp3")
            labelStatus.setText('Status: Finished!')
        elif comboExport.currentText() == 'Video':
            comboExport.setCurrentIndex(0)
            text_list_clips = []
            image_list_clip = []
            labelStatus.setText('Status: Saving!')
            file_name = file_name.replace('.webm', '')
            file_name = file_name.replace('.mp4', '')
            file_name += ' V.mp3'
            audio_file.export(f"{file_name}", format="mp3")
            labelStatus.setText('Status: Generating...')
            music = AudioFileClip(f'{file_name}')
            for i in range(len(info_notes)):
                # https://www.reddit.com/r/moviepy/comments/4nin6q/update_imagemagik_and_moviepy_has_broken/
                txt_clip = editor.TextClip(
                    f"{info_notes[i]}", fontsize=100, color='black')
                txt_clip = txt_clip.on_color(size=(width, height), color=(0, 0, 0), pos=(
                    250, 200), col_opacity=0).set_duration(info_duration_per_note[i]).crossfadeout(info_duration_per_note[i])
                text_list_clips.append(txt_clip)

                img_clip = editor.ImageClip(
                    f'{image_folder}{self.get_key(info_note_types[i])}.png')
                img_clip = img_clip.resize(width=128, height=128).on_color(size=(width, height), color=(0, 0, 0), pos=(
                    310, 50), col_opacity=0).set_duration(info_duration_per_note[i]).crossfadeout(info_duration_per_note[i])
                image_list_clip.append(img_clip)
            background_clip = editor.ColorClip(
                size=(width, height), color=[255, 255, 255])
            background_clip = background_clip.set_duration(
                sum(info_duration_per_note))
            watermark_clip = txt_clip = editor.TextClip(f"thecodingjsoftware.weebly.com", fontsize=20, color='black').on_color(size=(
                width, height), color=(0, 0, 0), pos=(width - 350, height - 20), col_opacity=0).set_duration(sum(info_duration_per_note))
            result_text = editor.concatenate_videoclips(
                [text for text in text_list_clips])
            result_image = editor.concatenate_videoclips(
                [img for img in image_list_clip])
            result = editor.CompositeVideoClip(
                [background_clip, watermark_clip, result_text, result_image, ])
            result = result.set_audio(music)
            file_name = file_name.replace(' V.mp3', '')
            labelStatus.setText('Status: Rendering...')
            # result.iterframe_callback = self.testCall(result.iframe, result.frame, result.number_of_frames)  # some_function(iframe, frame, number_of_frames)
            result.write_videofile(f"{file_name}{file_extension}", fps=30)
            os.remove(f"{file_name} V.mp3")
            labelStatus.setText('Status: Finished!')
        self.unsetCursor()

    def testCall(self, iframe, frame, number_of_frames):
        print(number_of_frames)

    def get_key(self, val):
        for key, value in note_types.items():
            if val == value:
                return key

    def generate_song(self, algorithmName, progressBar, buttonName, buttonPlay, buttonDelete, labelStatus, comboExport):
        self.setCursor(Qt.BusyCursor)
        self.start_generation(progressBar, buttonName,
                              buttonPlay, buttonDelete, labelStatus, comboExport)
        self.btnCancelThreads.setEnabled(True)

    def btnClearGrid(self):
        global total
        total = 0
        self.clearLayout(self.gridMusicProgress)
        self.reload_config_file()

    def open_settings_window(self):
        self.settingsUI = settingsUI(self)
        self.settingsUI.show()

    def open_about_window(self):
        time_now = datetime.now()
        diffrence = (time_now - latest_update_date).days
        QMessageBox.information(
            self, f'{title}', f"Version: {version}\nLast Update: {diffrence} days ago on {latest_update_date_formated}.\nDeveloped by: TheCodingJ's", QMessageBox.Ok, QMessageBox.Ok)

    def open_license_window(self):
        self.licenseUI = licensewindowUI()
        self.licenseUI.show()

    def reload_config_file(self):
        load_config_file(DefaultMode, DarkMode, LightMode, CSSOn,
                         lastSelectedGenre, lastSelectedAlgorithm, lastSelectedTheme)


class licensewindowUI(QDialog):

    def __init__(self):
        super(licensewindowUI, self).__init__()
        uic.loadUi(UI_folder + 'license.ui', self)
        self.setWindowTitle("License")
        self.setWindowIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_FileDialogInfoView')))
        self.icon = self.findChild(QLabel, 'lblIcon')
        self.icon.setFixedSize(128, 128)
        pixmap = QPixmap('icon.png')
        myScaledPixmap = pixmap.scaled(self.icon.size(), Qt.KeepAspectRatio)
        self.icon.setPixmap(myScaledPixmap)
        self.lisenceText = self.findChild(QLabel, 'label_2')
        with open('LICENSE', 'r') as f:
            self.lisenceText.setText(f.read())
        self.btnClose = self.findChild(QPushButton, 'btnClose')
        if current_platform == 'Linux':
            self.btnClose.setIcon(self.style().standardIcon(
                getattr(QStyle, 'SP_DialogOkButton')))
        self.btnClose.clicked.connect(self.close)
        self.setFixedSize(780, 470)


class settingsUI(QWidget):

    def __init__(self, mainwindow):
        super(settingsUI, self).__init__()
        uic.loadUi(UI_folder + 'settings.ui', self)
        self.mainwindow = mainwindow
        self.center()
        self.setFixedSize(270, 340)
        self.setWindowIcon(QIcon("icon.png"))
        self.Default = self.findChild(QRadioButton, 'radDefault')
        self.Default.toggled.connect(self.RadClicked)
        self.Dark = self.findChild(QRadioButton, 'radDark')
        self.Dark.toggled.connect(self.RadClicked)
        self.Light = self.findChild(QRadioButton, 'radLight')
        self.Light.toggled.connect(self.RadClicked)
        self.CSS = self.findChild(QCheckBox, 'customeCSS')
        self.CSS.setChecked(True if CSSOn[0] == 'True' else False)
        self.CSS.toggled.connect(self.RadClicked)

        self.styles = ['Breeze', 'Fusion', 'qdarkgraystyle', 'qdarkstyle']
        self.comboBoxStyles = self.findChild(QComboBox, 'comboBoxStyles')
        self.comboBoxStyles.addItems(self.styles)
        self.Default.setChecked(True if DefaultMode[0] == 'True' else False)
        self.Dark.setChecked(True if DarkMode[0] == 'True' else False)
        self.Light.setChecked(True if LightMode[0] == 'True' else False)
        self.comboBoxStyles.currentIndexChanged.connect(self.ComboClicked)
        for index, style in enumerate(self.styles):
            if lastSelectedTheme[0] == style:
                self.comboBoxStyles.setCurrentIndex(index)

        self.btnApply = self.findChild(QPushButton, 'btnApply')
        self.btnApply.clicked.connect(self.close)

    def RadClicked(self):
        config_json.pop(0)
        config_json.append(
            {
                "Default": [str(self.Default.isChecked())],
                "Dark": [str(self.Dark.isChecked())],
                "Light": [str(self.Light.isChecked())],
                "CSS": [str(self.CSS.isChecked())],
                "Last Genre": [int(lastSelectedGenre[0])],
                "Last Theme": [str(lastSelectedTheme[0])],
                "Last Algorithm": [int(lastSelectedAlgorithm[0])]
            })
        with open(config_file, mode='w+', encoding='utf-8') as file:
            json.dump(config_json, file, ensure_ascii=True)
        load_config_file(DefaultMode, DarkMode, LightMode, CSSOn,
                         lastSelectedGenre, lastSelectedAlgorithm, lastSelectedTheme)
        self.load_theme()

    def ComboClicked(self):
        if self.comboBoxStyles.currentText() == 'qdarkgraystyle' or self.comboBoxStyles.currentText() == 'qdarkstyle':
            if not self.Default.isChecked():
                self.Dark.setChecked(True)
            self.Light.setEnabled(False)
        else:
            self.Light.setEnabled(True)
        config_json.pop(0)
        config_json.append(
            {
                "Default": [str(DefaultMode[0])],
                "Dark": [str(DarkMode[0])],
                "Light": [str(LightMode[0])],
                "CSS": [str(CSSOn[0])],
                "Last Genre": [int(lastSelectedGenre[0])],
                "Last Theme": [str(self.comboBoxStyles.currentText())],
                "Last Algorithm": [int(lastSelectedAlgorithm[0])]
            })
        with open(config_file, mode='w+', encoding='utf-8') as file:
            json.dump(config_json, file, ensure_ascii=True)
        load_config_file(DefaultMode, DarkMode, LightMode, CSSOn,
                         lastSelectedGenre, lastSelectedAlgorithm, lastSelectedTheme)
        self.load_theme()

    def load_theme(self):
        QApplication.setPalette(QApplication.palette())
        if CSSOn[0] == 'True':
            self.mainwindow.setStyleSheet(
                open(themes_folder + "style.qss", "r").read())
        else:
            self.mainwindow.setStyleSheet('')
        if DefaultMode[0] == 'True':
            if current_platform == 'Windows':
                app.setStyle('Windowsvista')
            elif current_platform == 'Linux':
                app.setStyle('Fusion')
            QApplication.setPalette(originalPalette)
            app.setStyleSheet('')
        if LightMode[0] == 'True':
            if lastSelectedTheme[0] == 'Fusion' or lastSelectedTheme[0] == 'windowsvista':
                app.setPalette(QApplication.style().standardPalette())
                palette = QPalette()
                gradient = QLinearGradient(0, 0, 0, 400)
                gradient.setColorAt(0.0, QColor(240, 240, 240))
                gradient.setColorAt(1.0, QColor(215, 215, 215))
                palette.setColor(QPalette.ButtonText, Qt.black)
                palette.setBrush(QPalette.Window, QBrush(gradient))
                app.setPalette(palette)
                app.setStyle(lastSelectedTheme[0])
                app.setStyleSheet('')
            elif lastSelectedTheme[0] == 'Breeze':
                file = QFile(themes_folder + 'Breeze/light.qss')
                file.open(QFile.ReadOnly | QFile.Text)
                stream = QTextStream(file)
                app.setStyleSheet(stream.readAll())
        if DarkMode[0] == 'True':
            if lastSelectedTheme[0] == 'Fusion' or lastSelectedTheme[0] == 'windowsvista':
                palette = QPalette()
                gradient = QLinearGradient(0, 0, 0, 400)
                gradient.setColorAt(0.0, QColor(40, 40, 40))
                gradient.setColorAt(1.0, QColor(30, 30, 30))
                palette.setBrush(QPalette.Window, QBrush(gradient))
                palette.setColor(QPalette.WindowText, Qt.white)
                palette.setColor(QPalette.Base, QColor(25, 25, 25))
                palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
                palette.setColor(QPalette.ToolTipBase, Qt.black)
                palette.setColor(QPalette.ToolTipText, Qt.white)
                palette.setColor(QPalette.Text, Qt.white)
                palette.setColor(QPalette.Button, QColor(30, 30, 30))
                palette.setColor(QPalette.ButtonText, Qt.white)
                palette.setColor(QPalette.BrightText, Qt.red)
                palette.setColor(QPalette.Link, QColor(42, 130, 218))
                palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
                palette.setColor(QPalette.HighlightedText, Qt.black)
                app.setPalette(palette)
                app.setStyle(lastSelectedTheme[0])
                app.setStyleSheet('')
            elif lastSelectedTheme[0] == 'Breeze':
                file = QFile(themes_folder + 'Breeze/dark.qss')
                file.open(QFile.ReadOnly | QFile.Text)
                stream = QTextStream(file)
                app.setStyleSheet(stream.readAll())
            elif lastSelectedTheme[0] == 'qdarkstyle':
                QApplication.setPalette(originalPalette)
                app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            elif lastSelectedTheme[0] == 'qdarkgraystyle':
                QApplication.setPalette(originalPalette)
                app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def closeEvent(self, event):
        self.close()


alphabetList = list(ascii_lowercase) + list(ascii_uppercase)
alphabetValList = list(i + 1 for i in range(len(alphabetList)))

piano_samples = os.path.dirname(os.path.realpath(__file__)) + '/Piano Samples/'
image_folder = os.path.dirname(os.path.realpath(__file__)) + '/Images/'
compile_folder = os.path.dirname(os.path.realpath(__file__)) + '/Music/'
themes_folder = os.path.dirname(os.path.realpath(__file__)) + '/Themes/'
genres_folder = os.path.dirname(os.path.realpath(__file__)) + '/Genres/'
UI_folder = os.path.dirname(os.path.realpath(__file__)) + '/GUI/'

if current_platform == 'Windows':
    UI_folder = UI_folder.replace('/', '\\')
    piano_samples = piano_samples.replace('/', '\\')
    image_folder = image_folder.replace('/', '\\')
    compile_folder = compile_folder.replace('/', '\\')
    genres_folder = genres_folder.replace('/', '\\')
    themes_folder = themes_folder.replace('/', '\\')

if not os.path.exists(compile_folder):
    os.mkdir(compile_folder)
if not os.path.exists(genres_folder):
    os.mkdir(genres_folder)
all_genre_files = [f for f in glob.glob(
    genres_folder + "**/*.json", recursive=True)]
try:
    genres_file = all_genre_files[0]
except IndexError:
    genres_file = []
keys_file = os.path.dirname(os.path.realpath(__file__)) + '/keys.json'
config_file = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
if not os.path.exists(config_file):
    with open(config_file, 'w+') as f:
        f.write(
            '[{"Default": ["True"],"Dark": ["False"],"Light": ["False"],"CSS": ["True"], "Last Genre": [0], "Last Algorithm": [0], "Last Theme": ["Fusion"]}]')
note_types = {
    'Semibreve': 1,  # semibreve
    'Minim': 2,  # minim
    'Crochet': 4,  # crochet
    'Quaver': 8,  # quaver
    'Semiquaver': 16,  # semiquaver
    'Demisemiquaver': 32  # demisemiquaver
}

# NOTE JSON
note_states = []
genre_names = []
note_type_states = []
total = 0
for i in all_genre_files:
    i = i.replace(genres_folder, '')
    i = i.replace('.json', '')
    genre_names.append(i)
with open(keys_file) as file:
    keys_json = json.load(file)
try:
    with open(genres_file) as file:
        genres_json = json.load(file)
        for i, noteState in enumerate(genres_json[0]['Notes']):
            for j, k in enumerate(keys_json[0]['keys']):
                note_states.append(noteState[str(k)][0])
        for i, noteState in enumerate(genres_json[0]['Note Types']):
            for j, k in enumerate(note_types):
                note_type_states.append(noteState[str(k)][0])
except:
    pass

# CONFIG JSON
DefaultMode = []
DarkMode = []
LightMode = []
CSSOn = []
lastSelectedGenre = []
lastSelectedTheme = []
lastSelectedAlgorithm = []

originalPalette = None
config_json = []


def load_config_file(*args):
    global config_json
    for i, j in enumerate(args):
        j.clear()
        with open(config_file) as file:
            config_json = json.load(file)
            for d in config_json[0]['Default']:
                args[0].append(d)
            for da in config_json[0]['Dark']:
                args[1].append(da)
            for l in config_json[0]['Light']:
                args[2].append(l)
            for c in config_json[0]['CSS']:
                args[3].append(c)
            for g in config_json[0]['Last Genre']:
                args[4].append(g)
            for al in config_json[0]['Last Algorithm']:
                args[5].append(al)
            for th in config_json[0]['Last Theme']:
                args[6].append(th)


def exit_handler(): sys.exit()


if __name__ == '__main__':
    load_config_file(DefaultMode, DarkMode, LightMode, CSSOn,
                     lastSelectedGenre, lastSelectedAlgorithm, lastSelectedTheme)
    atexit.register(exit_handler)
    app = QApplication(sys.argv)
    window = mainwindowUI()
    app.exec_()
