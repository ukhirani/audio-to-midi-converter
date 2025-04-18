import pyaudio
import tkinter as tk
from tkinter import ttk
import numpy as np
import threading
import aubio
import mido
import time
import queue
import pygame
import sys
midiportame = 'VirtualPort'

image_paths = {
    
    'default':"E:\\HarshvardhanAndUmang\\GUI Images\\Main_bg1.png",
    '0':"E:\\HarshvardhanAndUmang\\GUI Images\\C1.png",
    '1':"E:\\HarshvardhanAndUmang\\GUI Images\\C#1.png",  
    '2':"E:\\HarshvardhanAndUmang\\GUI Images\\D1.png",
    '3':"E:\\HarshvardhanAndUmang\\GUI Images\\D#1.png",  
    '4':"E:\\HarshvardhanAndUmang\\GUI Images\\E2.png",  
    '5':"E:\\HarshvardhanAndUmang\\GUI Images\\F1.png",
    '6':"E:\\HarshvardhanAndUmang\\GUI Images\\F#1.png",  
    '7':"E:\\HarshvardhanAndUmang\\GUI Images\\G1.png",  
    '8':"E:\\HarshvardhanAndUmang\\GUI Images\\G#1.png", 
    '9':"E:\\HarshvardhanAndUmang\\GUI Images\\A1.png",  
    '10':"E:\\HarshvardhanAndUmang\\GUI Images\\A#1.png", 
    '11':"E:\\HarshvardhanAndUmang\\GUI Images\\B1.png",  
    
}
pygame.init()


keytobedisplayed = None


def guimodule():
    
    global keytobedisplayed 
    

    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption('AUDIO TO MIDI')
    
        # Define the positions and dimensions for the default image (x, y, width, height)
    default_image_rect = pygame.Rect(100, 100, 601, 515)

    # Flags to keep track of which key is pressed

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Clear the screen
        screen.fill((143, 185, 168))  # Grey background

        # Blit (draw) the image corresponding to the pressed key or the default image
        if keytobedisplayed != None:
            screen.blit(pygame.transform.scale(images[str(keytobedisplayed)], (default_image_rect.width, default_image_rect.height)), default_image_rect.topleft)
        else:
            screen.blit(pygame.transform.scale(images['default'], (default_image_rect.width, default_image_rect.height)), default_image_rect.topleft)

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
    sys.exit()

    
    
    
images = {guikey: pygame.image.load(path) for guikey, path in image_paths.items()}

midiqueue = queue.Queue()

audio = pyaudio.PyAudio()
CHUNK = 1024  
FORMAT = pyaudio.paInt16

current_stream = audio.open(format=FORMAT, channels=1, rate=44100, input=True,
                            input_device_index=1, frames_per_buffer=CHUNK)

def frequency_to_note(frequency):
    
    global keytobedisplayed

    if frequency <= 0:
        return None
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    base_frequency = 261.63  
    semitones_from_c4 = 12 * np.log2(frequency / base_frequency)
    note = int(round(semitones_from_c4)) % 12
    octave = int(round(semitones_from_c4 / 12))
    note_str = f"{note_names[note]}{octave}"
    print(note_str)
    return int(round(semitones_from_c4)) + 60

def audiocapture():
    
    global keytobedisplayed

    if current_stream:
        samplerate = 44100
        win_s = 4096  
        hop_s = 1024  
        pitch_detection = aubio.pitch("yin", win_s, hop_s, samplerate)
        while True:
            # print("global ",keytobedisplayed)   
            data = current_stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            pitches = pitch_detection(audio_data)
            f0 = pitches[0]
            key = frequency_to_note(f0) 
            
            midiqueue.put(key)  

def themidiprinter():
    
    global keytobedisplayed

    while True:
        midisignal = midiqueue.get()
        print(midisignal)
        if midisignal is None:
            # with threading.Lock:   
                keytobedisplayed = None
        else:
            if midisignal in range(0, 128):
                # with threading.Lock():
                    print(midisignal)
                    keytobedisplayed = midisignal%12
                    with mido.open_output(midiportame) as port:
                        port.send(mido.Message('note_on', note=int(midisignal), velocity=100))
                        
                    # Sleep thread separately
                    time.sleep(0.01)
                    
                    with mido.open_output(midiportame) as port:
                        port.send(mido.Message('note_off', note=int(midisignal), velocity=100))

# Create and start the threads
listentoaudiothread = threading.Thread(target=audiocapture)
themidiprinterthread = threading.Thread(target=themidiprinter)
guimodulethread = threading.Thread(target=guimodule)

listentoaudiothread.start()
themidiprinterthread.start()
guimodulethread.start()

# import pyaudio
# import tkinter as tk
# from tkinter import ttk
# import numpy as np
# import threading
# import aubio
# import rtmidi
# import time
# import queue
# import pygame
# import sys

# midiportame = 'VirtualPort'

# image_paths = {
#     'default': "E:\\HarshvardhanAndUmang\\GUI Images\\Main_bg1.png",
#     '0': "E:\\HarshvardhanAndUmang\\GUI Images\\C1.png",
#     '1': "E:\\HarshvardhanAndUmang\\GUI Images\\C#1.png",
#     '2': "E:\\HarshvardhanAndUmang\\GUI Images\\D1.png",
#     '3': "E:\\HarshvardhanAndUmang\\GUI Images\\D#1.png",
#     '4': "E:\\HarshvardhanAndUmang\\GUI Images\\E2.png",
#     '5': "E:\\HarshvardhanAndUmang\\GUI Images\\F1.png",
#     '6': "E:\\HarshvardhanAndUmang\\GUI Images\\F#1.png",
#     '7': "E:\\HarshvardhanAndUmang\\GUI Images\\G1.png",
#     '8': "E:\\HarshvardhanAndUmang\\GUI Images\\G#1.png",
#     '9': "E:\\HarshvardhanAndUmang\\GUI Images\\A1.png",
#     '10': "E:\\HarshvardhanAndUmang\\GUI Images\\A#1.png",
#     '11': "E:\\HarshvardhanAndUmang\\GUI Images\\B1.png",
# }

# pygame.init()

# keytobedisplayed = None


# def guimodule():
#     global keytobedisplayed

#     screen = pygame.display.set_mode((800, 800))
#     pygame.display.set_caption('AUDIO TO MIDI')

#     # Define the positions and dimensions for the default image (x, y, width, height)
#     default_image_rect = pygame.Rect(100, 100, 601, 515)

#     # Flags to keep track of which key is pressed

#     # Main game loop
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         # Clear the screen
#         screen.fill((143, 185, 168))  # Grey background

#         # Blit (draw) the image corresponding to the pressed key or the default image
#         if keytobedisplayed is not None:
#             screen.blit(pygame.transform.scale(images[str(keytobedisplayed)], (default_image_rect.width, default_image_rect.height)), default_image_rect.topleft)
#         else:
#             screen.blit(pygame.transform.scale(images['default'], (default_image_rect.width, default_image_rect.height)), default_image_rect.topleft)

#         # Update the display
#         pygame.display.update()

#     # Quit Pygame
#     pygame.quit()
#     sys.exit()


# images = {guikey: pygame.image.load(path) for guikey, path in image_paths.items()}

# midiqueue = queue.Queue()

# audio = pyaudio.PyAudio()
# CHUNK = 1024
# FORMAT = pyaudio.paInt16

# current_stream = audio.open(format=FORMAT, channels=1, rate=44100, input=True,
#                             input_device_index=2, frames_per_buffer=CHUNK)


# def frequency_to_note(frequency):
#     global keytobedisplayed

#     if frequency <= 0:
#         return None
#     note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
#     base_frequency = 261.63
#     semitones_from_c4 = 12 * np.log2(frequency / base_frequency)
#     note = int(round(semitones_from_c4)) % 12
#     octave = int(round(semitones_from_c4 / 12))
#     note_str = f"{note_names[note]}{octave}"
#     # print(note_str)
#     return int(round(semitones_from_c4)) + 60


# def audiocapture():
#     global keytobedisplayed

#     if current_stream:
#         samplerate = 44100
#         win_s = 4096
#         hop_s = 1024
#         pitch_detection = aubio.pitch("yin", win_s, hop_s, samplerate)
#         while True:
#             # print("global ", keytobedisplayed)
#             data = current_stream.read(CHUNK)
#             audio_data = np.frombuffer(data, dtype=np.int16)
#             audio_data = audio_data.astype(np.float32) / 32768.0
#             pitches = pitch_detection(audio_data)
#             f0 = pitches[0]
#             key = frequency_to_note(f0)

#             midiqueue.put(key)


# def themidiprinter():
#     global keytobedisplayed

#     midiout = rtmidi.RtMidiOut()

#     # Choose the appropriate method based on the version of rtmidi
#     if hasattr(midiout, 'open_virtual_port'):
#         midiout.openVirtualPort(midiportame)
#     else:
#         midiout.openVirtualPort(midiportame)

#     while True:
#         midisignal = midiqueue.get()
#         print(midisignal)
#         if midisignal is None:
#             keytobedisplayed = None
#         else:
#             if midisignal in range(0, 128):
#                 print(midisignal)
#                 note_on = [0x90, midisignal, 100]  # Note On
#                 note_off = [0x80, midisignal, 100]  # Note Off

#                 midiout.sendMessage(note_on)
#                 time.sleep(0.01)
#                 midiout.sendMessage(note_off)

                


# # Create and start the threads
# listentoaudiothread = threading.Thread(target=audiocapture)
# themidiprinterthread = threading.Thread(target=themidiprinter)
# guimodulethread = threading.Thread(target=guimodule)

# listentoaudiothread.start()
# themidiprinterthread.start()
# guimodulethread.start()

