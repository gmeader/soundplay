Soundplay.exe is a Windows command line program that plays music files when MIDI note commands are received. The source code is the file soundplay.py, a Python program.

You must have a MIDI controller keyboard connected to your computer.

The text file: config.cfg tells the program what audio file to play when a given MIDI note is received. The config.cfg file must be in the same folder as soundplay.exe

Sample config.cfg:

[FILES]
60 = amenfull.wav
62 = Canon.mp3
64 = Happy song.mp3
65 = britta.ogg

In this file you must have a line with the text "[FILES]". After that you have lines with a MIDI note number, an equals sign and a filename. Each of these lines assigns an audio file to be played when a specified MIDI note is received. You put the audio files in the same folder as soundplay.exe, or you can put a complete path to an audio file in config.cfg, like this: 
    C:\Users\gmeader\SoundPlay\amenfull.wav

You must open a Command Prompt window in Windows to run soundplay. Do this by typing cmd in the search box in the lower left of your screen.

cd into the folder where you have soundplay and type soundplay to run the program.

You will see something like the following:
===================
pygame 2.5.0 (SDL 2.28.0, Python 3.9.2)
Hello from the pygame community. https://www.pygame.org/contribute.html
Reading config file:  config.cfg
{'60': 'amenfull.wav', '62': 'Canon.mp3', '64': 'Happy song.mp3', '65': 'britta.ogg'}
MIDI_Note Audio_file
     60   amenfull.wav
     62   Canon.mp3
     64   Happy song.mp3
     65   britta.ogg
MIDI input port: 1
MIDI Input device name: Arturia MiniLab mkII
====================
It is telling you that pygame is running (code that gets the MIDI commands and plays sound files)
It shows you what's in the config.cfg file.
It tells you which MIDI device it is listening to to recieve MIDI commands.

When you press a key on the MIDI keyboard, it displays the received command, and if that command is assigned to an audio file, it shows you that.
===================
CH: 0 CMD: 9 NOTE: 60 C5 VEL: 82
PLAY: amenfull.wav LEN: 7.0 sec.
Play
CH: 0 CMD: 8 NOTE: 60 C5 VEL: 0
STOP
=====================
When you release the key, it stops playing
