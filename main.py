from pydub import AudioSegment
from pydub.playback import play
import os, json, sys, random, threading, glob, datetime, atexit, subprocess
import webbrowser as wb
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
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
        # if play: threading.Thread(target=self.playNote,args=(index,)).start()
        if play: self.playNote(index)
    def playNote(self, i):
        try:
            note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][i]}.mp3")
            play(note)
            return
        except PermissionError as e:
            self.OpenErrorDialog('Permission Denied', e)
        except FileNotFoundError as e:
            self.OpenErrorDialog('File Not Found', e)
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
        self.VideoWindow = VideoWindow(name)
        self.VideoWindow.setFixedSize(300,100)
        self.VideoWindow.show()

class settingsUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Music_Generator/settings.ui', self)

class VideoWindow(QMainWindow):
    def __init__(self, name):
        super(VideoWindow, self).__init__()
        self.audioName = name
        self.minute = 0
        self.second = 0
        self.durationSecond = 0
        self.durationMinute = 0
        self.setWindowTitle(name) 
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        
        self.lblTimeStart = QLabel()
        self.lblTimeEnd = QLabel()

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(partial(self.openFile, '', True))
        
        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.lblTimeStart)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.lblTimeEnd)

        layout = QVBoxLayout()
        # layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        # layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.openFile(file_path + '/' + compile_folder + self.audioName, False)

    def openFile(self, fileName, openFileDialog):
        if openFileDialog:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Audio",
                    os.path.dirname(os.path.abspath(__file__)) + '/' + compile_folder, "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")
            if fileName.endswith('.mp4'):
                reader = imageio.get_reader(fileName)
                fps = reader.get_meta_data()['fps']
                fileName = fileName.replace('.mp4', '.avi')
                writer = imageio.get_writer(fileName, fps=fps)
                for im in reader: writer.append_data(im[:, :, :])
                writer.close()
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        self.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState: self.mediaPlayer.pause()
        else: self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState: self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else: self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.second = int(position/1000%60)
        self.minute = int(position/1000/60)
        self.lblTimeStart.setText("{:02d}:{:02d}".format(self.minute, self.second))
        self.lblTimeEnd.setText("{:02d}:{:02d}".format(self.durationMinute, self.durationSecond))
        # self.lblTime.setText(str(self.minute) + ':' + str(self.second) + '/' + str(self.durationMinute) + ':' + str(self.durationSecond))
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.durationMinute = int(duration/1000 / 60)
        self.durationSecond = int(duration/1000%60)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
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
