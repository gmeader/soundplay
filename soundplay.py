# command line program to play an audio file when a MIDI note is received
# a config file has the midi note numbers and the audiofile paths
from pygame import mixer, midi, time
import pygame
import sys
import configparser

is_playing = False
song_channel = False
sound_path = False
note_number = 0

config_filename = 'config.cfg'
print ('Reading config file: ',config_filename)
config = configparser.RawConfigParser()
config.read(config_filename)
files_dict = dict(config.items('FILES'))
print(files_dict)
if files_dict:
    print('MIDI_Note','Audio_file')
for note in files_dict:
    print('    ',note,' ', files_dict[note])

def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'S', 'A#', 'B']
    note = number % 12
    octave = str(int((number - note) / 12))
    # print(number, note, octave)
    return notes[note]+octave

def play(sound_path):
    # play audio file
    global is_playing, song_channel
    if sound_path:
        song = mixer.Sound(sound_path)
        song_length = song.get_length()
        print('PLAY:',sound_path,'LEN:',"{0:.1f}".format(song_length), 'sec.')
        song_channel = mixer.Channel(2)

        # play
        if not is_playing:
            if song_channel:
                is_playing = True
                print('Play')
                song_channel.play(song)

def stop_playing():
    # stop
    global is_playing, song_channel
    if is_playing:
        is_playing = False
        print('STOP')
        if song_channel:
            song_channel.stop()

def pause():
    # pause
    global is_playing, song_channel
    if not is_playing:
        is_playing = True
        print('UnPaused')
        if song_channel:
            song_channel.unpause()
    else:
        print('Paused')
        is_playing = False
        if song_channel:
            song_channel.pause()

# Volume
# global is_playing, song_channel
# if song_channel:
#    song_channel.set_volume(volume/100)



pygame.init()
mixer.init()
pygame.midi.init()

midi_input_id = pygame.midi.get_default_input_id()
if midi_input_id > -1:
    print ('MIDI input port:',midi_input_id)
    (interf, name, input, output, opened) = pygame.midi.get_device_info(midi_input_id)
    midi_input_device_name = str(name, 'utf-8')
    print('MIDI Input device name:', midi_input_device_name)

else:
    print('No MIDI devices found.')
    sys.exit()

midi_in = pygame.midi.Input(midi_input_id)

while True:
    # get MIDI input
    if midi_in.poll():
        midi_event = midi_in.read(1)[0]
        timestamp = midi_event[1]
        midi_data = midi_event[0]
        channel = midi_data[0] & 0x0F
        command = midi_data[0] >> 4
        note_number = midi_data[1]
        velocity = midi_data[2]
        if command == 9 or command == 8:
            print("CH:",channel, "CMD:",command, "NOTE:",note_number, number_to_note(note_number), 'VEL:',velocity)
            if command == 9:
                # play
                if str(note_number) in files_dict:
                    sound_path = files_dict[str(note_number)]
                    #print ('sound_path:',sound_path)
                    play(sound_path)
                else:
                    print ('note_number:',note_number)
            if command == 8:
                # stop playing
                stop_playing()
        elif command == 11:
            print("CH:", channel, "CMD: CC", "Controller:", note_number, 'VAL:',velocity)

        elif command == 14:
            print("CH:", channel, "PitchBend", "V1:", note_number, 'V2:', velocity)
        elif midi_data[0] == 240  or midi_data[0] == 127:
            print("SYSEX", midi_data)
        else:
            print(midi_event)






