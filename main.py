from pydub import AudioSegment
from pydub.playback import play
import os, json, sys, random

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
if not os.path.exists(compile_folder): os.mkdir(compile_folder)
keys_file = os.path.dirname(os.path.realpath(__file__)) + '/keys.json'

note_types = {
    'whole note': 1,    #semibreve
    'half note': 2,    #minim
    'quarter note': 4,    #crochet
    'eigth note': 8,    #quaver
    'sixteenth note': 16,    #semiquaver
    'thirty-second note': 32    #demisemiquaver
}
with open(keys_file) as file:
    keys_json = json.load(file)

# for x in range(50):
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Music_Generator/mainwindow.ui', self)
        self.btnGenerate = self.findChild(QPushButton, 'btnGenerate')
        self.btnGenerate.clicked.connect(partial(self.btnGenerateClicked))
        
        self.inputSongLength = self.findChild(QDoubleSpinBox,'inputSongLength')
        self.genAlgorithms = self.findChild(QComboBox, 'genAlgorithms')
        self.genAlgorithms.addItem('Random')
        self.show()
    def btnGenerateClicked(self):
        if self.genAlgorithms.currentText() == 'Random': self.generate_song_random()
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
                    final_song = final_song[:seconds * 1000]
                    final_song.fade_in(6000).fade_out(6000)
                    final_song.export(f"{compile_folder}Final.mp3", format="mp3")
                    print('Finished')
                    return
        except Exception as e:
            print(e)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
