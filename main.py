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

print(note_type_states)

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
            self.btnNoteState = QPushButton()
            self.btnNoteState.setEnabled(False)
            self.btnNoteState.setFlat(True)
            self.btnNoteState.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogApplyButton')) if note_states[i] == 'True' else self.style().standardIcon(getattr(QStyle, 'SP_DialogCloseButton')))
            
            self.btnNotePlay = QPushButton()
            self.btnNotePlay.setFlat(True)
            self.btnNotePlay.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
            self.btnNotePlay.clicked.connect(partial(self.btnNoteClick, j, i, self.btnNotePlay, True))
            
            self.btnNote = QPushButton(j)
            self.btnNote.setCheckable(True)
            self.btnNote.setChecked(True if note_states[i] == 'True' else False)
            self.btnNote.clicked.connect(partial(self.btnNoteClick, j, i, self.btnNote, False))
            
            self.NoteGridLayout.addWidget(self.btnNotePlay, i, 0)
            self.NoteGridLayout.addWidget(self.btnNote, i, 1)
            self.NoteGridLayout.addWidget(self.btnNoteState, i, 2)
        for i, j in enumerate(note_types):
            self.btnNoteTypeState = QPushButton()
            self.btnNoteTypeState.setEnabled(False)
            self.btnNoteTypeState.setFlat(True)
            self.btnNoteTypeState.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogApplyButton')) if note_type_states[i] == 'True' else self.style().standardIcon(getattr(QStyle, 'SP_DialogCloseButton')))
            
            self.btnNoteType = QPushButton()
            self.btnNoteType.setToolTip(j)
            self.btnNoteType.setCheckable(True)
            self.btnNoteType.setChecked(True if note_type_states[i] == 'True' else False)
            self.btnNoteType.setIcon(QtGui.QIcon(f'{image_folder}{j}.png'))
            self.btnNoteType.setIconSize(QtCore.QSize(32,32))
            
            self.NoteTypeGridLayout.addWidget(self.btnNoteType, i, 0)
            self.NoteTypeGridLayout.addWidget(self.btnNoteTypeState, i, 1)
            
    def btnNoteClick(self, name, index, state, play):
        print(state.isChecked())
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
                # play(note)
                
                if final_song.duration_seconds > seconds:
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
