from pydub import AudioSegment
from pydub.playback import play
import os, json, sys, random, threading, glob, datetime, atexit, subprocess
import webbrowser as wb
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import (QAbstractVideoBuffer, QMediaContent,
        QMediaMetaData, QMediaPlayer, QMediaPlaylist, QVideoFrame, QVideoProbe)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5 import QtWidgets, uic
from functools import partial

if sys.platform == "linux" or sys.platform == "linux2": current_platform = 'Linux'
elif sys.platform == "darwin": current_platform = 'Mac'
elif sys.platform == "win32": current_platform = 'Windows'

if current_platform == 'Linux':
    piano_samples = 'Piano Samples/'
    image_folder = 'Images/'
    compile_folder = 'Compile/'
    genres_folder = 'Genres/'
elif current_platform == 'Windows':
    piano_samples = 'Piano Samples\\'
    image_folder = 'Images\\'
    compile_folder = 'Compile\\'
    genres_folder = 'Genres\\'


if not os.path.exists(compile_folder): os.mkdir(compile_folder)
all_genre_files = [f for f in glob.glob(genres_folder + "**/*.json", recursive=True)]
genres_file = all_genre_files[0]

keys_file = os.path.dirname(os.path.realpath(__file__)) + '/keys.json'
config_file = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

note_types = {
    'Semibreve': 1,    #semibreve
    'Minim': 2,    #minim
    'Crochet': 4,    #crochet
    'Quaver': 8,    #quaver
    'Semiquaver': 16,    #semiquaver
    'Demisemiquaver': 32    #demisemiquaver
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
with open(keys_file) as file: keys_json = json.load(file)
with open(genres_file) as file:
    genres_json = json.load(file)
    for i, noteState in enumerate(genres_json[0]['Notes']):
        for j, k in enumerate(keys_json[0]['keys']): note_states.append(noteState[str(k)][0])
    for i, noteState in enumerate(genres_json[0]['Note Types']):
        for j, k in enumerate(note_types): note_type_states.append(noteState[str(k)][0])

# CONFIG JSON
theme = []
name = []
config_json = {}
class mainwindowUI(QMainWindow):
    def __init__(self, parent = None):
        super(mainwindowUI, self).__init__(parent)
        uic.loadUi('Music_Generator/mainwindow.ui', self)
        self.setStyleSheet(open("style.qss", "r").read())
        self.btnGenerate = self.findChild(QPushButton, 'btnGenerate_2')
        self.btnGenerate.clicked.connect(partial(self.btnGenerateClicked))

        self.btnClear = self.findChild(QPushButton, 'btnClear')
        self.btnClear.clicked.connect(self.btnClearGrid)

        self.inputSongLength = self.findChild(QDoubleSpinBox,'inputSongLength_4')

        self.genAlgorithms = self.findChild(QComboBox, 'genAlgorithms_4')
        self.genAlgorithms.setToolTip('Diffrent algorithms of music generation.')
        self.genAlgorithms.addItem('Random')
        self.genAlgorithms.addItem('Step')

        self.genresComboBox = self.findChild(QComboBox, 'genresComboBox')
        self.genresComboBox.addItems(genre_names)
        self.genresComboBox.currentIndexChanged.connect(self.updateNotes)

        self.NoteGridLayout = self.findChild(QGridLayout,'NoteGridLayout')
        self.NoteTypeGridLayout = self.findChild(QGridLayout,'NoteTypeGridLayout')
        self.gridMusicProgressGridLayout = self.findChild(QGridLayout,'gridMusicProgress')

        self.actionExport = self.findChild(QAction, 'actionExport')
        self.actionExport.setStatusTip('Export all saved genres to *.csv')

        self.actionPrefrences = self.findChild(QAction, 'actionPrefrences')
        self.actionPrefrences.setStatusTip('Change window settings.')
        self.actionPrefrences.triggered.connect(self.open_settings_window)

        self.actionOpenMusicPlayer = self.findChild(QAction, 'actionOpen_Music_Player')
        self.actionOpenMusicPlayer.setStatusTip('Open Media Player.')
        self.actionOpenMusicPlayer.triggered.connect(partial(self.open_mediaplayer_window, ''))

        self.UINotes()
        self.resize(700,600)
        self.show()
    def UINotes(self):
        colSize = 12
        for i, j in enumerate(keys_json[0]['keys']):
            self.btnNote = QPushButton(j)
            self.btnNote.setCheckable(True)
            self.btnNote.setChecked(True if note_states[i] == 'True' else False)
            self.btnNote.clicked.connect(partial(self.btnNoteClick, j, i, self.btnNote, True))
            if '#' in j or 'b' in j:
                self.btnNote.setToolTip(f'{j[0]} Sharp {j[2]}' if '#' in j else f'{j[0]} Flat {j[2]}')
                if note_states[i] == 'True': self.btnNote.setObjectName('blackOn') # self.btnNote.setStyleSheet("background-color: #4DFF33; color: black; border-radius: 3px; border: 1px solid black;")
                else: self.btnNote.setObjectName('blackOff') #self.btnNote.setStyleSheet("background-color: #FF3335; color: black; border-radius: 3px; border: 1px solid black;")
                self.btnNote.setFixedSize(28,64)
            else:
                self.btnNote.setToolTip(f'{j}')
                if note_states[i] == 'True': self.btnNote.setObjectName('whiteOn') #self.btnNote.setStyleSheet("background-color: #7FFF8E; color: black; border-radius: 3px; border: 1px solid black;")
                else: self.btnNote.setObjectName('whiteOff') #self.btnNote.setStyleSheet("background-color: #FF7F7F; color: black; border-radius: 3px; border: 1px solid black;")
                self.btnNote.setFixedSize(36,64)
            self.NoteGridLayout.addWidget(self.btnNote, i / colSize, i % colSize)
        for i, j in enumerate(note_types):
            self.btnNoteType = QPushButton()
            self.btnNoteType.setFixedSize(64,64)
            self.btnNoteType.setToolTip(j)
            self.btnNoteType.setCheckable(True)
            self.btnNoteType.setChecked(True if note_type_states[i] == 'True' else False)
            self.btnNoteType.setIcon(QtGui.QIcon(f'{image_folder}{j}.png'))
            self.btnNoteType.setIconSize(QtCore.QSize(32,32))
            self.btnNoteType.setObjectName("whiteOn" if note_type_states[i] == 'True' else "whiteOff")

            self.btnNoteType.clicked.connect(partial(self.btnNoteClick, j, i, self.btnNoteType, False))
            self.NoteTypeGridLayout.setColumnStretch(0,3)
            self.NoteTypeGridLayout.addWidget(self.btnNoteType, i / 2, i % 2)
    def btnNoteClick(self, name, index, state, play):
        global genres_json, genre_names, note_states, note_type_states
        temp_note_type_list_states = note_type_states
        temp_note_list_states = note_states
        for i, j in enumerate(note_types):
            if j == name:
                if temp_note_type_list_states[i] == 'True': temp_note_type_list_states[i] = 'False'
                else: temp_note_type_list_states[i] = 'True'
        for i, j in enumerate(keys_json[0]['keys']):
            if j == name:
                if temp_note_list_states[i] == 'True': temp_note_list_states[i] = 'False'
                else: temp_note_list_states[i] = 'True'

        genres_json.pop(0)
        genres_json.append(
            {
                "Name":[
                    str(self.genresComboBox.currentText())
                ],
                "Notes":[
                    {
                        "C1": [
                            str(temp_note_list_states[0])
                        ],
                        "C#1": [
                            str(temp_note_list_states[1])
                        ],
                        "D1": [
                            str(temp_note_list_states[2])
                        ],
                        "Eb1": [
                            str(temp_note_list_states[3])
                        ],
                        "E1": [
                            str(temp_note_list_states[4])
                        ],
                        "F1": [
                            str(temp_note_list_states[5])
                        ],
                        "F#1": [
                            str(temp_note_list_states[6])
                        ],
                        "G1": [
                            str(temp_note_list_states[7])
                        ],
                        "Ab1": [
                            str(temp_note_list_states[8])
                        ],
                        "A1": [
                            str(temp_note_list_states[9])
                        ],
                        "Bb1": [
                            str(temp_note_list_states[10])
                        ],
                        "B1": [
                            str(temp_note_list_states[11])
                        ],
                        "C2": [
                            str(temp_note_list_states[12])
                        ],
                        "C#2": [
                            str(temp_note_list_states[13])
                        ],
                        "D2": [
                            str(temp_note_list_states[14])
                        ],
                        "Eb2": [
                            str(temp_note_list_states[15])
                        ],
                        "E2": [
                            str(temp_note_list_states[16])
                        ],
                        "F2": [
                            str(temp_note_list_states[17])
                        ],
                        "F#2": [
                            str(temp_note_list_states[18])
                        ],
                        "G2": [
                            str(temp_note_list_states[19])
                        ],
                        "Ab2": [
                            str(temp_note_list_states[20])
                        ],
                        "A2": [
                            str(temp_note_list_states[21])
                        ],
                        "Bb2": [
                            str(temp_note_list_states[22])
                        ],
                        "B2": [
                            str(temp_note_list_states[23])
                        ],
                        "C3": [
                            str(temp_note_list_states[24])
                        ],
                        "C#3": [
                            str(temp_note_list_states[25])
                        ],
                        "D3": [
                            str(temp_note_list_states[26])
                        ],
                        "Eb3": [
                            str(temp_note_list_states[27])
                        ],
                        "E3": [
                            str(temp_note_list_states[28])
                        ],
                        "F3": [
                            str(temp_note_list_states[29])
                        ],
                        "F#3": [
                            str(temp_note_list_states[30])
                        ],
                        "G3": [
                            str(temp_note_list_states[31])
                        ],
                        "Ab3": [
                            str(temp_note_list_states[32])
                        ],
                        "A3": [
                            str(temp_note_list_states[33])
                        ],
                        "Bb3": [
                            str(temp_note_list_states[34])
                        ],
                        "B3": [
                            str(temp_note_list_states[35])
                        ],
                        "C4": [
                            str(temp_note_list_states[36])
                        ],
                        "C#4": [
                            str(temp_note_list_states[37])
                        ],
                        "D4": [
                            str(temp_note_list_states[38])
                        ],
                        "Eb4": [
                            str(temp_note_list_states[39])
                        ],
                        "E4": [
                            str(temp_note_list_states[40])
                        ],
                        "F4": [
                            str(temp_note_list_states[41])
                        ],
                        "F#4": [
                            str(temp_note_list_states[42])
                        ],
                        "G4": [
                            str(temp_note_list_states[43])
                        ],
                        "Ab4": [
                            str(temp_note_list_states[44])
                        ],
                        "A4": [
                            str(temp_note_list_states[45])
                        ],
                        "Bb4": [
                            str(temp_note_list_states[46])
                        ],
                        "B4": [
                            str(temp_note_list_states[47])
                        ],
                        "C5": [
                            str(temp_note_list_states[48])
                        ],
                        "C#5": [
                            str(temp_note_list_states[49])
                        ],
                        "D5": [
                            str(temp_note_list_states[50])
                        ],
                        "Eb5": [
                            str(temp_note_list_states[51])
                        ],
                        "E5": [
                            str(temp_note_list_states[52])
                        ],
                        "F5": [
                            str(temp_note_list_states[53])
                        ],
                        "F#5": [
                            str(temp_note_list_states[54])
                        ],
                        "G5": [
                            str(temp_note_list_states[55])
                        ],
                        "Ab5": [
                            str(temp_note_list_states[56])
                        ],
                        "A5": [
                            str(temp_note_list_states[57])
                        ],
                        "Bb5": [
                            str(temp_note_list_states[58])
                        ],
                        "B5": [
                            str(temp_note_list_states[59])
                        ],
                        "C6": [
                            str(temp_note_list_states[60])
                        ]
                    }
                ],
                "Note Types":[
                    {
                        "Semibreve": [
                            str(temp_note_type_list_states[0])
                        ],
                        "Minim": [
                            str(temp_note_type_list_states[1])
                        ],
                        "Crochet": [
                            str(temp_note_type_list_states[2])
                        ],
                        "Quaver": [
                            str(temp_note_type_list_states[3])
                        ],
                        "Semiquaver": [
                            str(temp_note_type_list_states[4])
                        ],
                        "Demisemiquaver": [
                            str(temp_note_type_list_states[5])
                        ]
                    }
                ]
            }
        )
        with open(genres_file, mode='w+', encoding='utf-8') as file: json.dump(genres_json, file, ensure_ascii=True, indent=4)
        note_states.clear()
        note_type_states.clear()
        with open(genres_file) as file:
            genres_json = json.load(file)
            for i, noteState in enumerate(genres_json[0]['Notes']):
                for j, k in enumerate(keys_json[0]['keys']): note_states.append(noteState[str(k)][0])
            for i, noteState in enumerate(genres_json[0]['Note Types']):
                for j, k in enumerate(note_types): note_type_states.append(noteState[str(k)][0])
        self.clearLayout(self.NoteGridLayout)
        self.clearLayout(self.NoteTypeGridLayout)
        self.UINotes()
        if play: threading.Thread(target=self.playNote,args=(index,)).start()
        # if play: self.playNote(index)
    def playNote(self, i):
        try:
            note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][i]}.mp3")
            play(note)
        except PermissionError as e:
            self.OpenErrorDialog('Permission Denied', e)
        except FileNotFoundError as e:
            self.OpenErrorDialog('File Not Found', e)
        else:
            note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][i]}.mp3")
            play(note)
    def threadPlayNote(self, i):
        note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][i]}.mp3")
        play(note)
    @pyqtSlot(str)
    def OpenErrorDialog(self, title, text):
        QMessageBox.critical(self, f'{title}', f"{text}", QMessageBox.Ok, QMessageBox.Ok)
    def btnGenerateClicked(self):
        global total
        total += 1
        self.progressBar = QProgressBar()
        self.btnDelete = QPushButton()
        self.btnDelete.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogDiscardButton')))
        self.btnDelete.setEnabled(False)

        self.lblStatus = QLabel('Status: Generating...')

        self.btnName = QPushButton(str(total) + '. ')
        self.btnName.setFlat(True)
        self.btnName.clicked.connect(partial(self.btnOpenPath, compile_folder))
        self.btnName.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DirOpenIcon')))

        self.btnPlay = QPushButton()
        self.btnPlay.setEnabled(False)
        self.btnPlay.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))

        self.gridMusicProgressGridLayout.addWidget(self.btnName, total, 0)
        self.gridMusicProgressGridLayout.addWidget(self.progressBar, total, 1)
        self.gridMusicProgressGridLayout.addWidget(self.lblStatus, total, 2)
        self.gridMusicProgressGridLayout.addWidget(self.btnPlay, total, 3)
        self.gridMusicProgressGridLayout.addWidget(self.btnDelete, total, 4)

        threading.Thread(target=self.generate_song, args=(self.genAlgorithms.currentText(), self.progressBar, self.btnName, self.btnPlay, self.btnDelete, self.lblStatus,)).start()
    def btnOpenPath(self, path):
        if current_platform == 'Linux' or current_platform == 'Mac': wb.open(path)
        elif current_platform == 'Windows':
            FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
            path = os.path.normpath(path)
            if os.path.isdir(path): subprocess.run([FILEBROWSER_PATH, path])
            elif os.path.isfile(path): subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
    def btnDeleteFile(self, path, btnDelete, btnPlay, btnName, lblStatus):
        try:
            btnDelete.setEnabled(False)
            btnName.setEnabled(False)
            lblStatus.setText('Status: Deleted')
            btnPlay.setEnabled(False)
            if os.path.isfile(path) or os.path.islink(path):  os.remove(path)  # remove the file
            elif os.path.isdir(path): shutil.rmtree(path)  # remove dir and all contains
            else: raise ValueError("file {} is not a file or dir.".format(path))
        except Exception as e:
            print(e)
    def updateNotes(self):
        global genres_json, genre_names, note_states, note_type_states, genres_file
        genre_names.clear()
        note_states.clear()
        note_type_states.clear()
        genres_file = all_genre_files[self.genresComboBox.currentIndex()]
        with open(genres_file) as file:
            genres_json = json.load(file)
            for i, noteState in enumerate(genres_json[0]['Notes']):
                for j, k in enumerate(keys_json[0]['keys']): note_states.append(noteState[str(k)][0])
            for i, noteState in enumerate(genres_json[0]['Note Types']):
                for j, k in enumerate(note_types): note_type_states.append(noteState[str(k)][0])
        self.clearLayout(self.NoteGridLayout)
        self.clearLayout(self.NoteTypeGridLayout)
        self.UINotes()
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None: widget.deleteLater()
                else: self.clearLayout(item.layout())
    def generate_song(self, algorithmName, progressBar, buttonName, buttonPlay, buttonDelete, labelStatus):
        seconds = float(self.inputSongLength.text())
        final_song = ''
        all_available_notes = []
        all_available_note_types = []
        num = 0
        first_note = ''
        first_note_type = ''
        order_of_notes = 0
        order_of_note_types = 0
        final_name = ''
        try:
            with open(genres_file) as file:
                genres_json = json.load(file)
                for i, noteState in enumerate(genres_json[0]['Notes'][0]):
                    if note_states[i] == 'True': all_available_notes.append(keys_json[0]['keys'][i])
                for i, note in enumerate(genres_json[0]['Note Types'][0]):
                    if note_type_states[i] == 'True': all_available_note_types.append(note_types[note])
            while True:
                if not len(all_available_notes) > 0: return
                else:
                    if algorithmName == 'Random':
                        randNote = random.randint(0, len(all_available_notes) - 1)
                        randNoteType = random.randint(0, len(all_available_note_types) - 1) # min = 0, max = 5
                        selected_note_type = all_available_note_types[randNoteType]
                        num += 1
                        # min = 0, max = 60
                        note = AudioSegment.from_mp3(f"{piano_samples}{all_available_notes[randNote]}.mp3")
                        note_length = note.duration_seconds * 1000 #milliseconds
                        note = note[:note_length / selected_note_type]
                        note = note.fade_out(2000)
                        if final_song == '': final_song = note
                        else: final_song += note
                    elif algorithmName == 'Step':
                        step_keys = []
                        step_note_keys = []
                        all_available_step_notes = []
                        if not step_keys: step_keys, step_note_keys = self.getStepNumberList()
                        for i, j in enumerate(step_keys):
                            for o, k in enumerate(all_available_notes):
                                if j == k: all_available_step_notes.append(j)
                        # for i, j in enumerate(step_note_keys):
                            # print(j)
                        # for o, k in enumerate(all_available_note_types):
                        #     print(k)
                        for i, j in enumerate(all_available_step_notes):
                            temp = step_note_keys[i]
                            selected_note_type = all_available_note_types[temp]
                            note = AudioSegment.from_mp3(f"{piano_samples}{j}.mp3")
                            print(j)
                            note_length = note.duration_seconds * 1000 #milliseconds
                            try: note = note[:note_length / selected_note_type]
                            except ZeroDivisionError: note = note[:note_length / selected_note_type + 1]
                            note = note.fade_out(selected_note_type * 1000)
                            if final_song == '': final_song = note
                            else: final_song += note
                            if i == len(all_available_step_notes): step_keys, step_note_keys = self.getStepNumberList()
                    self.updateProgressBar(progressBar, final_song.duration_seconds/seconds*100)
                    if final_song.duration_seconds >= seconds:
                        final_name = (f'{str(algorithmName)} {str(self.genresComboBox.currentText())} {str(final_song.duration_seconds)}{str()}.mp3')
                        labelStatus.setText('Status: Finished!')
                        buttonName.setText(buttonName.text() + final_name)
                        buttonPlay.setEnabled(True)
                        buttonDelete.setEnabled(True)
                        buttonDelete.clicked.connect(partial(self.btnDeleteFile,compile_folder + final_name, buttonDelete, buttonPlay, buttonName, labelStatus))
                        # self.updateProgressBar(progressBar, 100)
                        # final_song = final_song[:seconds * 1000]
                        final_song.fade_in(6000).fade_out(6000)
                        final_song.export(f"{compile_folder}{final_name}", format="mp3")
                        buttonPlay.clicked.connect(partial(self.open_mediaplayer_window, final_name))
                        break
        except Exception as e:
            print(e)
    @pyqtSlot()
    def updateProgressBar(self, progressBar, value):
        progressBar.setValue(value)
    def getStepNumberList(self):
        amount_of_numbers = random.randint(5, 15)
        # NOTE TYPES
        note_types_number = []
        startNoteType = random.randint(2, 5) # Min = 0, Max = 5
        endNoteType = random.randint(startNoteType, 5)
        try: stepNoteType = (endNoteType - startNoteType)/(amount_of_numbers-1)
        except ZeroDivisionError: stepNoteType = (endNoteType - startNoteType)/(amount_of_numbers)
        # NOTES
        numbers = []
        step_number_notes = []
        start = random.randint(0, 60)
        end = random.randint(start, 60)
        try: step = (end - start)/(amount_of_numbers-1)
        except ZeroDivisionError: step = (end - start)/(amount_of_numbers)
        for i in range(amount_of_numbers):
            i = i + 1# In this case we want to start at 1, to simplify things.
            if i == 1: 
                numbers.append(int(start))# first number
                note_types_number.append(int(startNoteType))
            if i == 2: 
                numbers.append(int(start+step))# second number
                note_types_number.append(int(startNoteType + stepNoteType))
            if i >= 3 and i < amount_of_numbers: 
                numbers.append(int(start + (i - 1) * step))# everything in bewtween
                note_types_number.append(int(startNoteType + (i - 1) * stepNoteType))# everything in bewtween
            if i == amount_of_numbers: 
                numbers.append(int(start + (amount_of_numbers-1) * step))# end
                note_types_number.append(int(startNoteType + (amount_of_numbers-1) * stepNoteType))# end
        for i, j in enumerate(numbers): step_number_notes.append(keys_json[0]['keys'][j])
        return step_number_notes, note_types_number
    def btnClearGrid(self):
        global total
        total = 0
        self.clearLayout(self.gridMusicProgress)
        load_config_file(theme)
    def open_settings_window(self):
        self.settingsUI = settingsUI()
        self.settingsUI.show()
    def open_mediaplayer_window(self, name):
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.Player = Player([file_path + '/' + compile_folder + name])
        self.Player.setStyleSheet(open("style.qss", "r").read())
        self.Player.show()

class settingsUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Music_Generator/settings.ui', self)
class PlaylistModel(QAbstractItemModel):
     
    Title, ColumnCount = range(2)
 
    def __init__(self, parent=None):
        super(PlaylistModel, self).__init__(parent)
 
        self.m_playlist = None
 
    def rowCount(self, parent=QModelIndex()):
        return self.m_playlist.mediaCount() if self.m_playlist is not None and not parent.isValid() else 0
 
    def columnCount(self, parent=QModelIndex()):
        return self.ColumnCount if not parent.isValid() else 0
 
    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column) if self.m_playlist is not None and not parent.isValid() and row >= 0 and row < self.m_playlist.mediaCount() and column >= 0 and column < self.ColumnCount else QModelIndex()
 
    def parent(self, child):
        return QModelIndex()
 
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            if index.column() == self.Title:
                location = self.m_playlist.media(index.row()).canonicalUrl()
                return QFileInfo(location.path()).fileName()
 
            return self.m_data[index]
 
        return None
 
    def playlist(self):
        return self.m_playlist
 
    def setPlaylist(self, playlist):
        if self.m_playlist is not None:
            self.m_playlist.mediaAboutToBeInserted.disconnect(
                    self.beginInsertItems)
            self.m_playlist.mediaInserted.disconnect(self.endInsertItems)
            self.m_playlist.mediaAboutToBeRemoved.disconnect(
                    self.beginRemoveItems)
            self.m_playlist.mediaRemoved.disconnect(self.endRemoveItems)
            self.m_playlist.mediaChanged.disconnect(self.changeItems)
 
        self.beginResetModel()
        self.m_playlist = playlist
 
        if self.m_playlist is not None:
            self.m_playlist.mediaAboutToBeInserted.connect(
                    self.beginInsertItems)
            self.m_playlist.mediaInserted.connect(self.endInsertItems)
            self.m_playlist.mediaAboutToBeRemoved.connect(
                    self.beginRemoveItems)
            self.m_playlist.mediaRemoved.connect(self.endRemoveItems)
            self.m_playlist.mediaChanged.connect(self.changeItems)
 
        self.endResetModel()
 
    def beginInsertItems(self, start, end):
        self.beginInsertRows(QModelIndex(), start, end)
 
    def endInsertItems(self):
        self.endInsertRows()
 
    def beginRemoveItems(self, start, end):
        self.beginRemoveRows(QModelIndex(), start, end)
 
    def endRemoveItems(self):
        self.endRemoveRows()
 
    def changeItems(self, start, end):
        self.dataChanged.emit(self.index(start, 0),
                self.index(end, self.ColumnCount))
        
class PlayerControls(QWidget):
    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    next = pyqtSignal()
    previous = pyqtSignal()
    changeVolume = pyqtSignal(int)
    changeMuting = pyqtSignal(bool)
    changeRate = pyqtSignal(float)
 
    def __init__(self, parent=None):
        super(PlayerControls, self).__init__(parent)
 
        self.playerState = QMediaPlayer.StoppedState
        self.playerMuted = False
 
        self.playButton = QToolButton(clicked=self.playClicked)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
 
        self.stopButton = QToolButton(clicked=self.stop)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setEnabled(False)
 
        self.nextButton = QToolButton(clicked=self.next)
        self.nextButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaSkipForward))
 
        self.previousButton = QToolButton(clicked=self.previous)
        self.previousButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaSkipBackward))
 
        self.muteButton = QToolButton(clicked=self.muteClicked)
        self.muteButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolume))
 
        self.volumeSlider = QSlider(Qt.Horizontal,
                sliderMoved=self.changeVolume)
        self.volumeSlider.setRange(0, 100)
 
        self.rateBox = QComboBox(activated=self.updateRate)
        self.rateBox.addItem("0.5x", 0.5)
        self.rateBox.addItem("1.0x", 1.0)
        self.rateBox.addItem("2.0x", 2.0)
        self.rateBox.setCurrentIndex(1)
 
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stopButton)
        # layout.addWidget(self.previousButton)
        layout.addWidget(self.playButton)
        # layout.addWidget(self.nextButton)
        layout.addWidget(self.muteButton)
        layout.addWidget(self.volumeSlider)
        layout.addWidget(self.rateBox)
        self.setLayout(layout)
 
    def state(self):
        return self.playerState
 
    def setState(self,state):
        if state != self.playerState:
            self.playerState = state
 
            if state == QMediaPlayer.StoppedState:
                self.stopButton.setEnabled(False)
                self.playButton.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPlay))
            elif state == QMediaPlayer.PlayingState:
                self.stopButton.setEnabled(True)
                self.playButton.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPause))
            elif state == QMediaPlayer.PausedState:
                self.stopButton.setEnabled(True)
                self.playButton.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def volume(self):
        return self.volumeSlider.value()
 
    def setVolume(self, volume):
        self.volumeSlider.setValue(volume)
 
    def isMuted(self):
        return self.playerMuted
 
    def setMuted(self, muted):
        if muted != self.playerMuted:
            self.playerMuted = muted
 
            self.muteButton.setIcon(
                    self.style().standardIcon(
                            QStyle.SP_MediaVolumeMuted if muted else QStyle.SP_MediaVolume))
 
    def playClicked(self):
        if self.playerState in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
            self.play.emit()
        elif self.playerState == QMediaPlayer.PlayingState:
            self.pause.emit()
 
    def muteClicked(self):
        self.changeMuting.emit(not self.playerMuted)
 
    def playbackRate(self):
        return self.rateBox.itemData(self.rateBox.currentIndex())
 
    def setPlaybackRate(self, rate):
        for i in range(self.rateBox.count()):
            if qFuzzyCompare(rate, self.rateBox.itemData(i)):
                self.rateBox.setCurrentIndex(i)
                return
 
        self.rateBox.addItem("%dx" % rate, rate)
        self.rateBox.setCurrentIndex(self.rateBox.count() - 1)
 
    def updateRate(self):
        self.changeRate.emit(self.playbackRate())

class Player(QWidget):
    fullScreenChanged = pyqtSignal(bool)
    def __init__(self, playlist, parent=None):
        super(Player, self).__init__(parent)
        self.colorDialog = None
        self.trackInfo = ""
        self.statusInfo = ""
        self.duration = 0
 
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
 
        self.player.durationChanged.connect(self.durationChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.playlist.currentIndexChanged.connect(self.playlistPositionChanged)
        self.player.mediaStatusChanged.connect(self.statusChanged)
        self.player.bufferStatusChanged.connect(self.bufferingProgress)
        self.player.videoAvailableChanged.connect(self.videoAvailableChanged)
        self.player.error.connect(self.displayErrorMessage)
 
        # self.videoWidget = VideoWidget()
        # self.player.setVideoOutput(self.videoWidget)
 
        self.playlistModel = PlaylistModel()
        self.playlistModel.setPlaylist(self.playlist)
 
        self.playlistView = QListView()
        self.playlistView.setModel(self.playlistModel)
        self.playlistView.setCurrentIndex(self.playlistModel.index(self.playlist.currentIndex(), 0))
 
        self.playlistView.activated.connect(self.jump)
 
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, self.player.duration() / 1000)
 
        self.labelDuration = QLabel()
        self.slider.sliderMoved.connect(self.seek)
 
        # self.labelHistogram = QLabel()
        # self.labelHistogram.setText("Histogram:")
        # self.histogram = HistogramWidget()
        # histogramLayout = QHBoxLayout()
        # histogramLayout.addWidget(self.labelHistogram)
        # histogramLayout.addWidget(self.histogram, 1)
 
        # self.probe = QVideoProbe()
        # self.probe.videoFrameProbed.connect(self.histogram.processFrame)
        # self.probe.setSource(self.player)
 
        openButton = QPushButton("Open", clicked=self.open)
 
        controls = PlayerControls()
        controls.setState(self.player.state())
        controls.setVolume(self.player.volume())
        controls.setMuted(controls.isMuted())
 
        controls.play.connect(self.player.play)
        controls.pause.connect(self.player.pause)
        controls.stop.connect(self.player.stop)
        # controls.next.connect(self.playlist.next)
        # controls.previous.connect(self.previousClicked)
        controls.changeVolume.connect(self.player.setVolume)
        controls.changeMuting.connect(self.player.setMuted)
        controls.changeRate.connect(self.player.setPlaybackRate)
        # controls.stop.connect(self.videoWidget.update)
 
        self.player.stateChanged.connect(controls.setState)
        self.player.volumeChanged.connect(controls.setVolume)
        self.player.mutedChanged.connect(controls.setMuted)
 
        # self.fullScreenButton = QPushButton("FullScreen")
        # self.fullScreenButton.setCheckable(True)
 
        # self.colorButton = QPushButton("Color Options...")
        # self.colorButton.setEnabled(False)
        # self.colorButton.clicked.connect(self.showColorDialog)
 
        displayLayout = QHBoxLayout()
        # displayLayout.addWidget(self.videoWidget, 2)
        # displayLayout.addWidget(self.playlistView)
 
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addStretch(1)
        controlLayout.addWidget(controls)
        controlLayout.addStretch(1)
        # controlLayout.addWidget(self.fullScreenButton)
        # controlLayout.addWidget(self.colorButton)
 
        layout = QVBoxLayout()
        layout.addLayout(displayLayout)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.slider)
        hLayout.addWidget(self.labelDuration)
        layout.addLayout(hLayout)
        layout.addLayout(controlLayout)
        # layout.addLayout(histogramLayout)
 
        self.setLayout(layout)
 
        if not self.player.isAvailable():
            QMessageBox.warning(self, "Service not available",
                    "The QMediaPlayer object does not have a valid service.\n"
                    "Please check the media service plugins are installed.")
 
            controls.setEnabled(False)
            self.playlistView.setEnabled(False)
            openButton.setEnabled(False)
            self.colorButton.setEnabled(False)
            self.fullScreenButton.setEnabled(False)
 
        self.metaDataChanged()
        print(playlist)
        self.addToPlaylist(playlist)
 
    def open(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Open Files")
        self.addToPlaylist(fileNames)
 
    def addToPlaylist(self, fileNames):
        for name in fileNames:
            fileInfo = QFileInfo(name)
            if fileInfo.exists():
                url = QUrl.fromLocalFile(fileInfo.absoluteFilePath())
                if fileInfo.suffix().lower() == 'm3u':
                    self.playlist.load(url)
                else:
                    self.playlist.addMedia(QMediaContent(url))
            else:
                url = QUrl(name)
                if url.isValid():
                    self.playlist.addMedia(QMediaContent(url))
 
    def durationChanged(self, duration):
        duration /= 1000
 
        self.duration = duration
        self.slider.setMaximum(duration)
 
    def positionChanged(self, progress):
        progress /= 1000
 
        if not self.slider.isSliderDown():
            self.slider.setValue(progress)
 
        self.updateDurationInfo(progress)
 
    def metaDataChanged(self):
        if self.player.isMetaDataAvailable():
            self.setTrackInfo("%s - %s" % (
                    self.player.metaData(QMediaMetaData.AlbumArtist),
                    self.player.metaData(QMediaMetaData.Title)))
 
    def previousClicked(self):
        # Go to the previous track if we are within the first 5 seconds of
        # playback.  Otherwise, seek to the beginning.
        if self.player.position() <= 5000:
            self.playlist.previous()
        else:
            self.player.setPosition(0)
 
    def jump(self, index):
        if index.isValid():
            self.playlist.setCurrentIndex(index.row())
            self.player.play()
 
    def playlistPositionChanged(self, position):
        self.playlistView.setCurrentIndex(
                self.playlistModel.index(position, 0))
 
    def seek(self, seconds):
        self.player.setPosition(seconds * 1000)
 
    def statusChanged(self, status):
        self.handleCursor(status)
 
        if status == QMediaPlayer.LoadingMedia:
            self.setStatusInfo("Loading...")
        elif status == QMediaPlayer.StalledMedia:
            self.setStatusInfo("Media Stalled")
        elif status == QMediaPlayer.EndOfMedia:
            QApplication.alert(self)
        elif status == QMediaPlayer.InvalidMedia:
            self.displayErrorMessage()
        else:
            self.setStatusInfo("")
 
    def handleCursor(self, status):
        if status in (QMediaPlayer.LoadingMedia, QMediaPlayer.BufferingMedia, QMediaPlayer.StalledMedia):
            self.setCursor(Qt.BusyCursor)
        else:
            self.unsetCursor()
 
    def bufferingProgress(self, progress):
        self.setStatusInfo("Buffering %d%" % progress)
 
    def videoAvailableChanged(self, available):
        if available:
            self.fullScreenButton.clicked.connect(
                    self.videoWidget.setFullScreen)
            self.videoWidget.fullScreenChanged.connect(
                    self.fullScreenButton.setChecked)
 
            if self.fullScreenButton.isChecked():
                self.videoWidget.setFullScreen(True)
        else:
            self.fullScreenButton.clicked.disconnect(
                    self.videoWidget.setFullScreen)
            self.videoWidget.fullScreenChanged.disconnect(
                    self.fullScreenButton.setChecked)
 
            self.videoWidget.setFullScreen(False)
 
        self.colorButton.setEnabled(available)
 
    def setTrackInfo(self, info):
        self.trackInfo = info
 
        if self.statusInfo != "":
            self.setWindowTitle("%s | %s" % (self.trackInfo, self.statusInfo))
        else:
            self.setWindowTitle(self.trackInfo)
 
    def setStatusInfo(self, info):
        self.statusInfo = info
 
        if self.statusInfo != "":
            self.setWindowTitle("%s | %s" % (self.trackInfo, self.statusInfo))
        else:
            self.setWindowTitle(self.trackInfo)
 
    def displayErrorMessage(self):
        self.setStatusInfo(self.player.errorString())
 
    def updateDurationInfo(self, currentInfo):
        duration = self.duration
        if currentInfo or duration:
            currentTime = QTime((currentInfo/3600)%60, (currentInfo/60)%60,
                    currentInfo%60, (currentInfo*1000)%1000)
            totalTime = QTime((duration/3600)%60, (duration/60)%60,
                    duration%60, (duration*1000)%1000);
 
            format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
            tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
        else:
            tStr = ""
 
        self.labelDuration.setText(tStr)
 
 
def load_config_file(*args):
    for i, j in enumerate(args):
        j.clear()
        with open(config_file) as file:
            config_json = json.load(file)
            for info in config_json:
                for themeNum in info['theme']: args[0].append(themeNum)
        print(j)
def exit_handler(): sys.exit()
if __name__ == '__main__':
    load_config_file(theme)
    atexit.register(exit_handler)
    app = QApplication(sys.argv)
    window = mainwindowUI()
    app.exec_()
