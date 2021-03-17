<p align="center">
    <img height="200" width="200" src="https://github.com/JareBear12418/Algorythm/blob/master/icon.png" />
</p>

<p align="center">
    <a href="https://img.shields.io/github/license/JareBear12418/Algorhythm?color=blue&style=for-the-badge" alt="License">
        <img src="https://img.shields.io/github/license/JareBear12418/Algorhythm?color=blue&style=for-the-badge" /></a>
    <a href="https://img.shields.io/static/v1?label=Platform&message=Windows|Linux&color=blue&style=for-the-badge">
        <img src="https://img.shields.io/static/v1?label=Platform&message=Windows|Linux&color=blue&style=for-the-badge" /></a>
    <a href="https://img.shields.io/github/repo-size/JareBear12418/Algorythm?label=Size&style=for-the-badge" alt="Size">
        <img src="https://img.shields.io/github/repo-size/JareBear12418/Algorythm?label=Size&style=for-the-badge" /></a>
    <a href="https://img.shields.io/github/commit-activity/m/JareBear12418/Algorhythm?style=for-the-badge" alt="Commits">
        <img src="https://img.shields.io/github/commit-activity/m/JareBear12418/Algorhythm?style=for-the-badge" /></a>
    <a href="https://discord.gg/EtrSc4s">
        <img src="https://img.shields.io/discord/588186512143679488?logo=discord&style=for-the-badge" alt="Discord"></a>
    <a href="https://img.shields.io/github/v/tag/JareBear12418/Algorhythm?label=Release&logoColor=blue&style=for-the-badge">
        <img src="https://img.shields.io/github/v/tag/JareBear12418/Algorhythm?label=Release&logoColor=blue&style=for-the-badge"
            alt="Discord"></a>
    <a href="https://img.shields.io/github/languages/count/JareBear12418/Algorhythm?style=for-the-badge">
        <img src="https://img.shields.io/github/languages/count/JareBear12418/Algorhythm?style=for-the-badge"
            alt="Languages"></a>
    <a href="https://img.shields.io/github/languages/top/JareBear12418/Algorhythm?style=for-the-badge">
        <img src="https://img.shields.io/github/languages/top/JareBear12418/Algorhythm?style=for-the-badge"
            alt="Top_Language"></a>
    <a href="https://sourcery.ai">
        <img src="https://img.shields.io/badge/Sourcery-enabled-brightgreen?style=for-the-badge"
            alt="https://sourcery.ai"></a>
</p>
<br>
<p align="center">
    <a href="https://forthebadge.com">
    <img src="https://forthebadge.com/images/badges/works-on-my-machine.svg">
</p>
<p align="center">
    <a href="https://forthebadge.com">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
    <img src="https://forthebadge.com/images/badges/powered-by-qt.svg">
</a>
</p>

# Algorhythm

- Generate music algorithmically at the click of a button.

| Features       | Windows | Linux |
| -------------- | ------- | ----- |
| Generate Audio | ✔️       | ✔️     |
| Generate Video | ❌       | ✔️     |
| Theme support  | ✔️       | ✔️     |
| Sheet music    | ✔️       | ✔️     |



## Installation/Downloads
### Windows

Download the pre-release [here](https://github.com/JareBear12418/Algorhythm/releases).


### Linux

To install for linux, instructions are listed [here](https://github.com/JareBear12418/Algorhythm/blob/master/README.md#linux).



## Setup for Development
### Windows

Download this repository!

Installing all python libraries:

It's best practice to create a virtual enviroment with:

`virtualenv [name]`

then activate it with:

`[name]/Scripts/activate`

Install all requirements with:

`pip install -r requirements.txt`

Install Lilypond to the Algorhythm file directory.
Download [Lilypond](https://lilypond.org/windows.html) 

[Direct link](https://lilypond.org/download/binaries/mingw/lilypond-2.20.0-1.mingw.exe)

and install into the `Algorhythm` directory.. 

Next you need to download and install `ffmpeg`
Download ffmpeg [here](https://www.filehorse.com/download-ffmpeg-64/)

Extract the zip folder and copy the following files into the Algorhythm directory.

`./ffmpeg-4.3.1-win64-static/bin/ffmpeg.exe`

`./ffmpeg-4.3.1-win64-static/bin/ffplay.exe`

`./ffmpeg-4.3.1-win64-static/bin/ffprobe.exe`

That should be everything you need to install for Windows.

The Algorhythm directory should look similar to this:

```
📦_Algorhythm
 ┣ 📂Genres
 ┣ 📂GUI
 ┣ 📂Images
 ┣ 📂LilyPond <-------- Make sure LilyPond is installed into the directory to where Algorhythm is downloaded to.
 ┣ 📂Themes
 ┣ 📜.gitignore
 ┣ 📜config.json
 ┣ 📜ffmpeg.exe <------- Make sure you coped these 3 executable files here.
 ┣ 📜ffplay.exe <-----^
 ┣ 📜ffprobe.exe <--^
 ┣ 📜icon.ico
 ┣ 📜icon.png
 ┣ 📜keys.json
 ┣ 📜LICENSE
 ┣ 📜main.py
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

### Linux

Download this repository!

Installing all python libraries:

It's best practice to create a virtual enviroment with:

`virtualenv [name]`

then activate it with:

`[name]/Scripts/activate`

Install all requirements with:

`pip install -r requirements.txt`

Install ImageMagick with:

``` bash
sudo apt-get install python-wand
sudo apt-get install libmagickwand-dev
sudo apt-get install imagemagick
sudo apt-get update
sudo apt-get upgrade
```

If moviepy throws an error do the following:
go to:

`/etc/ImageMagick-6/policy.xml`

Near the bottom there is this line:

`<!-- <policy domain="path" rights="none" pattern="@*" /> -->`

comment that out or delete it and that fixes the error.

Install LilyPond with:

`sudo apt install lilypond`

Install `libnotify-bin` if you don't have `notify-send` with:

`sudo apt install libnotify-bin`

and your done, everything shoud work


## How it works

- Using nothing but raw math/algorithms to generate music.
  - Simply typing words, letters or dragging an image onto the screen and pressing a button you can generate music:
    - Alphabet
      - We assign every letter a number. (Ex. a = 1, b = 2, c = 3 ... z = 26)
      - Convert those values to the correct name files in [Piano Samples](Piano%20Samples) folder.
      - For note types (Ex. [Crochet, Minim]) we take the length of the word, for example ("bear") is 4 letters in length and 4 is closest to the value "Crochet" in our `note_types` dictionary in `main.py`
     - Image
        - Perlin Noise
          - We generate Perlin noise according to the set values in the GUI, and then we proceed with the Image section further below.
        - Fractural Noise
          - We generate Fractural noise the same way we do Perlin noise.
        - Image
          - This is basically how the whole Image algorithm generates works I've explained this as best as I could and I will most likely clear things up later on, but this is the basically how it works.
          - Due to my bad coding practices and not commenting what does what, I can't exactly say what happens, but I did write down the process elsewhere.
          - First we read all the bytes from the image using `numpy`.
          - ***NOTE*** *An image that is 16x16 will have 256 pixels, or 256 notes to play. This is why I severely limited the size in the program, of course you can easily change the maximum size value, but it will take much longer to generate the music.*
          - We read all those pixels and store them into a `numpy` array. These arrays are **NOT** in `bytes` but in `RGB`. With these RGB values, we map them between 0 and 765 *(because 255x3=765, our `RGB` values can't be greater then this value, The color would have to be white (255, 255, 255) to reach this maximum value)*
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
            - Lets say starting number is 3, ending number is 7, and length is 8
            - Then we evenly increase from 3 to 7 using only 8 numbers.
            - Ex. [3, 4, 4, 5, 5, 6, 6, 7]
            - Convert those values to the correct name files in [Piano Samples](Piano%20Samples) folder.
            - Do the exact same method but for note types. Ex. [Crochet, Minim]
          - Step (-)
            - We do the exact same thing as we did in `Step (+)` except we reverse the lists.
          - Step (Random)
            - We do the exact same thing as we did in `Step (+)` except we randomize the lists.
        - Random
          - Does everything completely at random and may get removed in later versions... 
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


## Scripts

- main.py
    - Main program file. 
- Audio_Compiler.cpp
    - C++ program to handle audio compiling alongside ffmpeg. This drastically improves performance and audio compilation time. Python is slow. While the solution implemented in Python is fast, and by no means slow, it falls short of C++ speed.
- Specs:

C++ vs Python Using the [Algorhythm.png](https://github.com/JareBear12418/Algorhythm/blob/master/icon.png) image at 32x32 (363 pixels/notes to process). 

|      Tasks       |   C++    |  Python |Difference | Speed increase %|
| ---------------- | -------- | ------- | --------- | --------------- |
| Compiling Audio  | 28.173/s | 42.06/s | 13.887/s |    +33.02%      |
| Saving Audio     | 0.793/s  | 9.81/s  | 9.017/s  |    +1,137.07%   |
| Total Time       | 28.966/s | 51.87/s | 22.904/s |    +44.16%      |

Using Image to Music algorithm was the best way to ensure that they both would have the same amount of notes to process. 

We noticed a extreme speed difference when running these test on either Linux or Windows. Both of the above tests were run on Windows. Running the C++ Audio Compiler on Linux brought the total time down to around 14 seconds.  

## Plans

- [ ] Make pre-configured genres.
- [x] Text to music
- [x] Image to music
 - [x] Generate Perlin/Fractural noise.
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
  - Will probably have to generate the first 2 notes ahead of the current note.

## FAQ

- Aren't their better music generators out there? 
    - **YES!!!** There are so much better music generators out there that use AI and Neural Networks and so on. So Yes, there are way betters ones out there then mine.

- Why did start this project? 
    - Continuing from the above answer, I don't expect to make better music then AI generated music, although my goal is to reach a similar outcome, but it's hard to beat something that can think itself. 
    - The single main reason why I started this project is to make simple piano music very easy to do. I wanted to make make a simple background piano song for some ambience, but I can't play piano that well, so I started looking for some programs that can generate music easily, I did find some great ones, that use AI, but setting one up and using one is by no means easy to do, and the average person would probably not figure it out as well. So I was like: "I'll just make my own." So, I set off on my adventure to create this, generating music, with on click, in a simple executable program, although the size of the program is pretty big, and the development installation is not easy to setup, but for the average user its great to use. 

TL;DR To make an easy to use music Generator to make music at one click.

## Credits

### Themes

  - [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
    - Full credit goes to: [ColinDuquesnoy](https://github.com/ColinDuquesnoy)

  - [qdarkgraystyle](https://github.com/mstuttgart/qdarkgraystyle)
    - Full credit goes to: [Michell Stuttgart](https://github.com/mstuttgart)

  - [Breeze](https://github.com/Alexhuszagh/BreezeStyleSheets)
    - Full credit goes to: [Alexander Huszagh](https://github.com/Alexhuszagh)

  - [classic, dark_blue, dark_orange](https://github.com/sommerc/pyqt-stylesheets)
    - Full credit goes to: [Christoph Sommer](https://github.com/sommerc)

### Scripts

  - [Perlin-Numpy](https://github.com/pvigier/perlin-numpy)
    - Full credit goes to: [Pierre Vigier](https://github.com/pvigier)

 -  [nlohmann/json](https://github.com/nlohmann/json)
    -  Full credit goes to: [Niels Lohmann](https://github.com/nlohmann)

I'm only listing these credits because there is code/files directly included in my project that
I do not own. Scripts such as PyQt5 or matplotlib, etc. won't be listed here because im not including
any direct code from them in my repository, but of course this project wouldn't be possible
without them.
