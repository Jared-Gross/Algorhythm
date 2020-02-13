from pydub import AudioSegment
from pydub.playback import play
import os, json, sys, random,threading

from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5 import QtWidgets, uic
from functools import partial

piano_samples = 'Piano Samples/'
compile_folder = 'Compile/'
image_folder = 'Images/'
if not os.path.exists(compile_folder): os.mkdir(compile_folder)
keys_file = os.path.dirname(os.path.realpath(__file__)) + '/keys.json'
genres_file = os.path.dirname(os.path.realpath(__file__)) + '/genres.json'

note_types = {
    'Semibreve': 1,    #semibreve
    'Minim': 2,    #minim
    'Crochet': 4,    #crochet
    'Quaver': 8,    #quaver
    'Semiquaver': 16,    #semiquaver
    'Demisemiquaver': 32    #demisemiquaver
}
note_states = []
note_type_states = []
genre_names = []

with open(keys_file) as file:
    keys_json = json.load(file)
with open(genres_file) as file:
    genres_json = json.load(file)
    for i, name in enumerate (genres_json['genres']):
        genre_names.append(name['Name'][0])
    for i, noteState in enumerate(genres_json['genres'][0]['Notes']):
        for j, k in enumerate(keys_json[0]['keys']):
            note_states.append(noteState[str(k)][0])
    for i, noteState in enumerate(genres_json['genres'][0]['Note Types']):
        for j, k in enumerate(note_types):
            note_type_states.append(noteState[str(k)][0])

print(keys_json[0]['keys'])

# for x in range(50):
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Music_Generator/mainwindow.ui', self)
        self.btnGenerate = self.findChild(QPushButton, 'btnGenerate_2')
        self.btnGenerate.clicked.connect(partial(self.btnGenerateClicked))

        self.inputSongLength = self.findChild(QDoubleSpinBox,'inputSongLength_4')
        
        self.genAlgorithms = self.findChild(QComboBox, 'genAlgorithms_4')
        self.genAlgorithms.setToolTip('Diffrent algorithms of music generation.')
        self.genAlgorithms.addItem('Random')
        
        self.genresComboBox = self.findChild(QComboBox, 'genresComboBox')
        self.genresComboBox.addItems(genre_names)
        self.genresComboBox.currentIndexChanged.connect(self.updateNotes)
        
        self.NoteGridLayout = self.findChild(QGridLayout,'NoteGridLayout')
        self.NoteTypeGridLayout = self.findChild(QGridLayout,'NoteTypeGridLayout')
        
        self.actionExport = self.findChild(QAction, 'actionExport')
        self.actionExport.setStatusTip('Export all saved genres to *.csv')
        
        self.progressBar = self.findChild(QProgressBar,'progressBar')
        
        self.UINotes()
        self.show()
        
    def UINotes(self):
        for i, j in enumerate(keys_json[0]['keys']):
            self.btnNote = QPushButton(j)
            self.btnNote.setCheckable(True)
            self.btnNote.setChecked(True if note_states[i] == 'True' else False)
            self.btnNote.clicked.connect(partial(self.btnNoteClick, j, i, self.btnNote, True))
            if '#' in j or 'b' in j:
                if note_states[i] == 'True':
                    self.btnNote.setStyleSheet("background-color: #4DFF33; color: black")
                else:
                    self.btnNote.setStyleSheet("background-color: #FF3335; color: black")
                self.btnNote.setFixedSize(28,64)
            else:
                if note_states[i] == 'True':
                    self.btnNote.setStyleSheet("background-color: #7FFF8E; color: black")
                else:
                    self.btnNote.setStyleSheet("background-color: #FF7F7F; color: black")
                self.btnNote.setFixedSize(36,64)
            self.NoteGridLayout.addWidget(self.btnNote, 0, i)
        for i, j in enumerate(note_types):
            self.btnNoteType = QPushButton()
            self.btnNoteType.setFixedSize(40,40)
            self.btnNoteType.setToolTip(j)
            self.btnNoteType.setCheckable(True)
            self.btnNoteType.setChecked(True if note_type_states[i] == 'True' else False)
            self.btnNoteType.setIcon(QtGui.QIcon(f'{image_folder}{j}.png'))
            self.btnNoteType.setIconSize(QtCore.QSize(32,32))
            self.btnNoteType.setStyleSheet("background-color: #7FFF8E" if note_type_states[i] == 'True' else "background-color: #FF7F7F")

            self.btnNoteType.clicked.connect(partial(self.btnNoteClick, j, i, self.btnNoteType, False))
            self.NoteTypeGridLayout.setColumnStretch(0,3)
            self.NoteTypeGridLayout.addWidget(self.btnNoteType, 0, i)
            
    def btnNoteClick(self, name, index, state, play):
        global genres_json, genre_names, note_states
        temp_note_type_list_states = note_type_states
        temp_note_list_states = note_states
        temp_last_selected_genre = self.genresComboBox.currentIndex()
        for i, j in enumerate(note_types):
            if j == name:
                if temp_note_type_list_states[i] == 'True': temp_note_type_list_states[i] = 'False'
                else: temp_note_type_list_states[i] = 'True'
        for i, j in enumerate(keys_json[0]['keys']):
            if j == name:
                if temp_note_list_states[i] == 'True': temp_note_list_states[i] = 'False'
                else: temp_note_list_states[i] = 'True'
                
        for i, j in enumerate(genre_names):
            if self.genresComboBox.currentText() == j:
                genres_json['genres'].pop(i)
                genres_json['genres'].append(
                    {
                        "Name":[
                            str(j)
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
                
                with open(genres_file, mode='w+', encoding='utf-8') as file:
                    json.dump(genres_json, file, ensure_ascii=True, indent=4)
        # print(state.isChecked())

        genre_names.clear()
        note_states.clear()
        note_type_states.clear()
        
        with open(genres_file) as file:
            genres_json = json.load(file)
            for i, name in enumerate (genres_json['genres']):
                genre_names.append(name['Name'][0])
            for i, noteState in enumerate(genres_json['genres'][temp_last_selected_genre]['Notes']):
                for j, k in enumerate(keys_json[0]['keys']):
                    note_states.append(noteState[str(k)][0])
            for i, noteState in enumerate(genres_json['genres'][temp_last_selected_genre]['Note Types']):
                for j, k in enumerate(note_types):
                    note_type_states.append(noteState[str(k)][0])
        
        self.genresComboBox.clear()
        self.genresComboBox.addItems(genre_names)
        self.clearLayout(self.NoteGridLayout)
        self.clearLayout(self.NoteTypeGridLayout)
        self.UINotes()
        
        if play: threading.Thread(target=self.playNote,args=(index,)).start()
    def playNote(self, i):
        note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][i]}.mp3")
        play(note)
        return
    def btnGenerateClicked(self):
        if self.genAlgorithms.currentText() == 'Random': threading.Thread(target=self.generate_song_random).start()
    def updateNotes(self):
        global genres_json, genre_names, note_states
        genre_names.clear()
        note_states.clear()
        note_type_states.clear()
        with open(genres_file) as file:
            genres_json = json.load(file)
            for i, name in enumerate (genres_json['genres']):
                genre_names.append(name['Name'][0])
            for i, noteState in enumerate(genres_json['genres'][self.genresComboBox.currentIndex()]['Notes']):
                for j, k in enumerate(keys_json[0]['keys']):
                    note_states.append(noteState[str(k)][0])
            for i, noteState in enumerate(genres_json['genres'][self.genresComboBox.currentIndex()]['Note Types']):
                for j, k in enumerate(note_types):
                    note_type_states.append(noteState[str(k)][0])
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
    def generate_song_random(self):
        seconds = float(self.inputSongLength.text())
        print('Generating...')
        final_song = ''
        try:
            while True:
                randNote = random.randint(2,5) # min = 0, max = 5
                selected_note = ''
                for i, note_value in enumerate(note_types):
                    if randNote == i: selected_note = note_types[note_value]
                # min = 0, max = 60
                note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][random.randint(40,60)]}.mp3")
                note_length = note.duration_seconds * 1000 #milliseconds
                note = note[:note_length / selected_note]
                note = note.fade_out(2000)
                if final_song == '': final_song = note
                else: final_song += note
                self.progressBar.setValue(final_song.duration_seconds/seconds*100)
                if final_song.duration_seconds > seconds:
                    self.progressBar.setValue(100)
                    # final_song = final_song[:seconds * 1000]
                    final_song.fade_in(6000).fade_out(6000)
                    final_song.export(f"{compile_folder}Final.mp3", format="mp3")
                    print('Finished')
                    break
        except Exception as e:
            print(e)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
