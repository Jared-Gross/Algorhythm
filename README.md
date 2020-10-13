<p align="center"><img src="https://github.com/JareBear12418/Algorythm/blob/master/icon.png" /></p>

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-windows|linux-blue.svg)](PLATFORM)
[![Size](https://img.shields.io/github/repo-size/JareBear12418/Algorythm?label=Size)](SIZE)
# Algorhythm
- Generate music algorithmically at the click of a button.

| Features | Windows  | Linux  |
| ------- | --- | --- |
| Generate Audio | ✔️ | ✔️ |
| Generate Video | ❌  | ✔️ |
| Theme support | ✔️  | ✔️ |

## Installation
### Windows
Download [here](https://drive.google.com/file/d/1IqwMJ4RBeJ685IE8fRP0bJ18oboslgtH/view?usp=sharing)!

### Linux
Download this repository!

It's best practice to create a virtual enviroment with:

`virtualenv [name]`

then activate it with:

`[name]/Scripts/activate`

Install all requirements with:

`pip install -r requirements.txt`

Install ImageMagick with:
```
sudo apt-get install python-wand
sudo apt-get install libmagickwand-dev
sudo apt-get install imagemagick
sudo apt-get update
sudo apt-get upgrade
```
If moviepy still has running properly do the following:
go to:

`/etc/ImageMagick-6/policy.xml`

Near the bottom there is this line:

`<!-- <policy domain="path" rights="none" pattern="@*" /> -->`

comment that out or delete it.

and your done, everything shoud work

## How it works
- Using nothing but raw math/algorithms to generate music.
  - Simpling typing words or letters and pressing a button you can generate music:
    - Alphabet
      - We assign every letter a number. (Ex. a = 1, c = 3, z = 26)
      - Convert those values to the correct name files in [Piano Samples](Piano%20Samples) folder.
      - For note types (Ex. [Crochet, Minim]) we take the length of the word, for example ("bear") is 4 letters in length and 4 is closest to the value "Crochet" in our `note_types` dictionary in `main.py`
   - Mathematics algorithms:
      - Step
        - Step (+)
          - Pick three random numbers (starting number, ending number, and length)
          - Lets say starting number is 3, ending number is 7, and lenght is 8
          - Then we evenly increase from 3 to 7 using only 8 numbers.
            - Ex. [3, 4, 4, 5, 5, 6, 6, 7]
          - Convert those values to the correct name files in [Piano Samples](Piano%20Samples) folder.
          - Do the exact same method but for note types. Ex. [Crochet, Minim]
        - Step (-)
          - We do the exact same thing as we did in `Step (+)` except we reverse the lists.
        - Step (Random)
          - We do the exact same thing as we did in `Step (+)` except we randomize the lists.
      - Random
        - Does everything completly at random and may get removed in later versions... 
        - *this was just a 'Proof of concept'*
- TL;DR: **MAGIC!!!**


## Plans
- [ ] Make pre-configured genres.
- [x] Text to music
- [ ] Image to music
- [x] Possibly make the generation process faster.
- [x] Better visual GUI
- [ ] Better quality sounds.
- [ ] More than just piano sounds.
  - For the time being you can change the sounds yourself by going to the [Piano Samples](Piano%20Samples) folder and edit them yourself. ***DO NOT CHANGE THE FILE NAMES! If you do the program will not work and it will crash.***
- Better generating algorithms.

## ToDo 
- [ ] Add play and stop button for playing the generated Audio.
- [ ] `.qss` for Live control buttons.

## Bugs
- [ ] Audio clipping with `demisemiquaver` & `semiquaver` notes.
  - Possible needs a longer fade, or better quality sounds.
- [ ] Threads not stopping
- [ ] Pressing live with a multiplier enabled. *(but I might leave this as a feature)*
- [ ] Don't add live generated music to Generated list in GUI

## Credits
[QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
Full credit goes to: [ColinDuquesnoy](https://github.com/ColinDuquesnoy)

[qdarkgraystyle](https://github.com/mstuttgart/qdarkgraystyle)
Full credit goes to: [mstuttgart](https://github.com/mstuttgart)

[Breeze](https://github.com/Alexhuszagh/BreezeStyleSheets)
Full credit goes to: [Alexhuszagh](https://github.com/Alexhuszagh)

