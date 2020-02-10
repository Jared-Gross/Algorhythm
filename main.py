from pydub import AudioSegment
from pydub.playback import play
import os, json, sys, random

piano_samples = 'Piano Samples/'
compile_folder = 'Compile/'
keys_file = os.path.dirname(os.path.realpath(__file__)) + '/keys.json'

note_types = {
    'whole note': 1,        #semibreve
    'half note': 2,         #minim
    'quarter note': 4,      #corctchet
    'eigth note': 8,        #quaver
    'sixteenth note': 16,    #semiquaver
    'thirty-second note': 32    #demisemiquaver
}
with open(keys_file) as file:
    keys_json = json.load(file)

final_song = ''
for x in range(50):
# while True:
    randNote = random.randint(2,5)
    selected_note = ''
    for i, note_value in enumerate(note_types):
        if randNote == i: selected_note = note_types[note_value]
    note = AudioSegment.from_mp3(f"{piano_samples}{keys_json[0]['keys'][random.randint(40,60)]}.mp3")
    note_length = note.duration_seconds * 1000 #milliseconds
    new_note_length = note_length / selected_note
    note = note[:new_note_length]
    note = note.fade_out(1500)
    if final_song == '': final_song = note
    else: final_song += note
    play(note)
final_song.fade_in(3000).fade_out(3000)
final_song.export(f"{compile_folder}Final.mp3", format="mp3")
    