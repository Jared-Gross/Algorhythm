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
| Sheet music | ✔️  | ✔️ |

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

Install ImageMagick with (Only Linux compatable):
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

Install LilyPond with **Linux**:
`sudo apt install lilypond`

**Windows**:
Download:
https://lilypond.org/windows.html

Direct link:
https://lilypond.org/download/binaries/mingw/lilypond-2.20.0-1.mingw.exe

Install to the current working directory. 

and your done, everything shoud work

## How it works
- Using nothing but raw math/algorithms to generate music.
  - Simpling typing words, letters or dragging an image onto the screen and pressing a button you can generate music:
    - Alphabet
      - We assign every letter a number. (Ex. a = 1, b = 2, c = 3 ... z = 26)
      - Convert those values to the correct name files in [Piano Samples](Piano%20Samples) folder.
      - For note types (Ex. [Crochet, Minim]) we take the length of the word, for example ("bear") is 4 letters in length and 4 is closest to the value "Crochet" in our `note_types` dictionary in `main.py`
     - Image
        - Perlin Noise
          - We generate perlin noise according to the set values in the GUI, and then we proceed with the Image section further below.
        - Fractral Noise
          - We generate fratral noise the same way we do Perlin noise.
        - Image
          - This is basicly how the whole Image algorithm generates works I've explained this as best as I could and I will most likely clear things up later on, but this is the basicly how it works.
          - Due to my bad coding practices and not commenting what does what, I can't exactly say what happens, but I did write down the process elsewhere.
          - First we read all the bytes from the image using `numpy`.
          - ***NOTE*** *An image that is 16x16 will have 256 pixels, or 256 notes to play. This is why I severly limited the size in the program, of course you can easily change the maxinum size value, but it will take much longer to generate the music.*
          - We read all those pixels and store them into a `numpy` array. These arrays are **NOT** in `bytes` but in `RGB`. With these RGB values, we map them between 0 and 765 *(because 255x3=765, our `RGB` values can't be greater then this value, The color would have to be white (255, 255, 255) to reach this maxinum value)*
          - After that, we map those numbers between the amount of notes we have. Say for example, our current pixel is (146, 242, 10) in the range between 0-765 this number is 398. Knowing these three numbers, we can map it between 0-61, which is the amount of notes we have. 
          - After the above, we know that our pixel is 398 in the range of: 0-765, But this doesn't tell us what note we need to play, so we need to scale this down to a range of 0-61, we achieve this with: `notes_value = [int(minAmountOfNotes + ((sum(row) - fixedRangeMin) / (fixedRangeMax - fixedRangeMin)) * (maxAmountOfNotes - minAmountOfNotes)) for row in res]` A better snippet of this is as the following: 
            ```python 
            fixedRangeMin = 0
            fixedRangeMax = 255*3
            minAmountOfNotes = 0
            maxAmountOfNotes = 61
            sum = 398 # sum[146, 242, 10]
            print(int(minAmountOfNotes + ((sum - fixedRangeMin) / 
                                          (fixedRangeMax - fixedRangeMin)) * 
                                          (maxAmountOfNotes - minAmountOfNotes)))
            ```
          - However this code works isn't important, **it works!**
          - Running the above code we get `31`, so in the range from `0-765` with the number `398` gives us: `31` in the range from `0-61`.
          - And that is the note value that we play.
          - A near exact process happens for the `note_type` or the duration of the note, just on a smaller scale.
          - and Repeat.
     - Mathematical algorithms:
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
        - Relation
          - Relation (W)
            - Pick a random starting number from 1 to 61, a random increasing amount, and a random boolean.
            - Then if our random boolean is true, we increase our starting number by our random increasing amount
              - Starting number = 31, Increase amount = 3, Random boolean = True.
              - We would do 31 + 3 = 34
            - Next we generate another random boolean and increasing amount, BUT we using our new starting number (34)
              - Number = 34, Increase amount = 2, Random boolean = False.
              - We would do 34 - 2 = 32.
            - and repeat!
          - Relation (R)
            - This works exactly the same way as `Relation (W)` except: instead of our starting number being between 1 and 61, we generate a random starting number and ending number. example: (12, 45)
            - We repeat the exact same steps as in `Relation (W)` but we stay with in the Range of these numbers: (12, 45).
- TL;DR: **MAGIC!!!**


## Plans
- [ ] Make pre-configured genres.
- [x] Text to music
- [x] Image to music
 - [x] Generate Perlin/Fractral noise.
 - [x] Add custom images.
  - [x] Exclude transparent pixels
- [x] Possibly make the generation process faster.
- [x] Better visual GUI
- [ ] Better quality sounds *(from a real piano and not an electric one)*.
- [x] Generate Sheet Music with [Mingus](https://bspaans.github.io/python-mingus/) and [LilyPond](https://lilypond.org).
- [ ] More than just piano sounds.
  - [ ] Guitar
  - [ ] Violin
  - [ ] Chello
  - [ ] Bass
  - [ ] Organ
  - For the time being you can change the sounds yourself by going to the [Piano Samples](Piano%20Samples) folder and edit them yourself. ***DO NOT CHANGE THE FILE NAMES! If you do the program will not work and it will crash and it will be very bad.***

## ToDo 
- [ ] Add play and stop button for playing the generated Audio.
- [ ] `.qss` for Live control buttons.
- [x] Try and make noise generator faster.
- [x] Remake entire UI and UX.
  - Using other widgets.

## Bugs
- [ ] Fix minor bugs with sheet music generator. 
- [ ] Audio clipping with `demisemiquaver` & `semiquaver` notes.
  - Possible needs a longer fade, or better quality sounds.
- [ ] Threads not stopping, the threads don't want to die.
- [ ] Pressing live with a multiplier enabled plays `x` amount of live music. *(but I might leave this as a feature, becuase why not?)*
- [x] Don't add live generated music to Generated list in GUI
- [ ] Live play needs a whole remake to sound similar to generated music.
  - Will probally have to generate the first 2 notes ahead of the current note.


## Credits
[QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
Full credit goes to: [ColinDuquesnoy](https://github.com/ColinDuquesnoy)

[qdarkgraystyle](https://github.com/mstuttgart/qdarkgraystyle)
Full credit goes to: [Michell Stuttgart](https://github.com/mstuttgart)

[Breeze](https://github.com/Alexhuszagh/BreezeStyleSheets)
Full credit goes to: [Alexander Huszagh](https://github.com/Alexhuszagh)

[classic, dark_blue, dark_orange](https://github.com/sommerc/pyqt-stylesheets)
Full credit goes to: [Christoph Sommer](https://github.com/sommerc)

[Perlin-Numpy](https://github.com/pvigier/perlin-numpy)
Full credit goes to: [Pierre Vigier](https://github.com/pvigier)
