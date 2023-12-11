import os
import tkinter
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from threading import *
import time
import math

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title('Music Player')
root.geometry('400x480')
pygame.mixer.init()

list_of_songs = []
n = 0

scrollable_frame = customtkinter.CTkScrollableFrame(master=root, width=300, height=200)
scrollable_frame.place(relx=.5, rely=.3, anchor=tkinter.CENTER)

def add_music():
    dossier = "music"
    noms_fichiers = os.listdir(dossier)
    for fichier in noms_fichiers:
        label = customtkinter.CTkLabel(scrollable_frame, text=f"{fichier}")
        label.bind("<Button-1>", lambda event, name=f"{dossier}/{fichier}": play_music(name))
        label.pack()
        list_of_songs.append(f"{dossier}/{fichier}")


add_music()

def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(.4)
        progressbar.set(pygame.mixer.music.get_pos() / 1000000)

def threading():
    t1 = Thread(target=progress)
    t1.start()


is_playing = False  # Ajouter une variable pour suivre l'état de lecture

def play_music(song_name=None):
    global n, is_playing

    if song_name:  # Si un nouveau morceau est passé, chargez-le et commencez à jouer
        threading()
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(.5)
        is_playing = True  # La musique est en cours de lecture

    elif is_playing:  # Si la musique est en cours de lecture, mettez-la en pause
        pygame.mixer.music.pause()
        is_playing = False

    else:  # Si la musique est en pause, reprenez la lecture
        pygame.mixer.music.unpause()
        is_playing = True


def skip_forward():
    global n
    n += 1
    if n >= len(list_of_songs):
        n = 0
    play_music(list_of_songs[n])

def skip_back():
    global n
    n -= 1
    if n < 0:
        n = len(list_of_songs) - 1
    play_music(list_of_songs[n])


def volume(value):
    pygame.mixer.music.set_volume(value)


play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

skip_f = customtkinter.CTkButton(master=root, text='>', command=skip_forward, width=2)
skip_f.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

skip_b = customtkinter.CTkButton(master=root, text='<', command=skip_back, width=2)
skip_b.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_= 0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=.5, rely=.85, anchor=tkinter.CENTER)


root.mainloop()