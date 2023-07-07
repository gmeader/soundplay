# command line program to play an audio file when a MIDI note is received
# a config file has the midi note numbers and the audiofile paths
from pygame import mixer, midi, time
import pygame
import sys
import configparser

is_playing = False
song_channel = False
sound_path = False
song=False
note_number = 0

config_filename = 'config.cfg'
print ('Reading config file: ', config_filename)
config = configparser.RawConfigParser()
config.read(config_filename)
files_dict = dict(config.items('FILES'))
#print(files_dict)
files_display=[]
if files_dict:
    print('MIDI_Note','Audio_file')
for note in files_dict:
    print('    ',note,' ', files_dict[note])
    files_display.append( str(note)+' '+ files_dict[note])


def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'S', 'A#', 'B']
    note = number % 12
    octave = str(int((number - note) / 12))
    # print(number, note, octave)
    return notes[note]+octave

def play(sound_path):
    # play audio file
    global is_playing, song_channel, status
    if sound_path:
        song = mixer.Sound(sound_path)
        song_length = song.get_length()
        print('PLAY:',sound_path,'LEN:',"{0:.1f}".format(song_length), 'sec.')
        status = 'PLAY: '+sound_path + ' LEN: '+"{0:.1f}".format(song_length)+ 'sec.'
        song_channel = mixer.Channel(2)

        # play
        if not is_playing:
            if song_channel:
                is_playing = True
                #print('Play')
                song_channel.play(song)

def stop_playing():
    # stop
    global is_playing, song_channel
    if is_playing:
        is_playing = False
        #print('STOP')
        if song_channel:
            song_channel.stop()

def pause():
    # pause
    global is_playing, song_channel
    if not is_playing:
        is_playing = True
        #print('UnPaused')
        if song_channel:
            song_channel.unpause()
    else:
        #print('Paused')
        is_playing = False
        if song_channel:
            song_channel.pause()

# Volume
# global is_playing, song_channel
# if song_channel:
#    song_channel.set_volume(volume/100)



pygame.init()
pygame.display.set_caption('My Game!')
BACKGROUND = (0,0,0)
TEXTCOLOR = (0, 100, 0)
fontsize = 20
smallfontsize = 14
margin_x = 10  # pixels from the left
margin_y = 10  # pixels from the top
spacing_y = 4  # pixels between lines
WINDOW = pygame.display.set_mode((640, 480))
pygame.display.set_caption('SoundPlay')
font = pygame.font.Font(pygame.font.get_default_font(), fontsize)
font_small = pygame.font.Font(pygame.font.get_default_font(), smallfontsize)
message1 = ''
message3 = ''
message4 = ''

mixer.init()
pygame.midi.init()

midi_input_id = pygame.midi.get_default_input_id()
if midi_input_id > -1:
    print ('MIDI input port:',midi_input_id)
    (interf, name, input, output, opened) = pygame.midi.get_device_info(midi_input_id)
    midi_input_device_name = str(name, 'utf-8')
    print('MIDI Input device name:', midi_input_device_name)
    message2 = 'MIDI In: '+midi_input_device_name

else:
    print('No MIDI devices found.')
    message2 = 'No MIDI devices found.'
    sys.exit()

midi_in = pygame.midi.Input(midi_input_id)
status='STOP'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
            #print("CH:",channel, "CMD:",command, "NOTE:",note_number, number_to_note(note_number), 'VEL:',velocity)
            message3 = "CH: "+str(channel) + " CMD: "+str(command) + " NOTE: " + str(note_number) +' '+ number_to_note(note_number) + ' VEL:'+str(velocity)
            if command == 9:
                # play
                if str(note_number) in files_dict:
                    sound_path = files_dict[str(note_number)]
                    #print ('sound_path:',sound_path)
                    message4 = sound_path
                    play(sound_path)
                else:
                    print ('note_number:',note_number)
            if command == 8:
                # stop playing
                status = 'STOP'
                stop_playing()
        elif command == 11:
            #print("CH:", channel, "CMD: CC", "Controller:", note_number, 'VAL:',velocity)
            message3 = "CH: " + str(channel) + " CMD: CC  Controller: "+ str(note_number) + ' VAL: '+str(velocity)

        elif command == 14:
            #print("CH:", channel, "PitchBend", "V1:", note_number, 'V2:', velocity)
            message3 = "CH: " + str( channel) + " PitchBend V1: " + str(note_number) + ' V2: ' + str(velocity)
        elif midi_data[0] == 240  or midi_data[0] == 127:
            pass #print("SYSEX", midi_data)
        else:
            print(midi_event)


    if is_playing:
        message1 = status # +' '+str(mixer.sound.get_pos() / 1000)
    else:
        message1 = status

    WINDOW.fill(BACKGROUND)
    block=[]
    txt_rect = []
    for index, text in enumerate(files_display):
        block = font_small.render(text, True, (125, 150, 125))
        txt_rect = block.get_rect()
        txt_rect.topleft = (margin_x, (margin_y + 130) + index * (smallfontsize + spacing_y))
        WINDOW.blit(block, txt_rect)

    block1 = font.render(message1, True, (25, 255, 25))
    block2 = font.render(message2, True, (125, 125, 0))
    block3 = font.render(message3, True, (255, 100, 25))
    block4 = font.render(message4, True, (125, 125, 200))
    txt_rect = block1.get_rect()
    # txt_rect.center = WINDOW.get_rect().center
    txt_rect.topleft = (margin_x, margin_y + 4 * (fontsize + spacing_y))
    WINDOW.blit(block1, txt_rect)
    txt_rect.topleft = (margin_x, margin_y + 1 * (fontsize + spacing_y))
    WINDOW.blit(block2, txt_rect)
    txt_rect.topleft = (margin_x, margin_y + 2 * (fontsize + spacing_y))
    WINDOW.blit(block3, txt_rect)
    txt_rect.topleft = (margin_x, margin_y + 3 * (fontsize + spacing_y))
    WINDOW.blit(block4, txt_rect)
    pygame.display.flip()






