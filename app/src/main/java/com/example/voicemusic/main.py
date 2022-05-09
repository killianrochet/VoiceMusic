import vlc
import os
import time
import Streaming
import sys, Ice
from os import walk
from threading import Thread
from pathlib import Path
import shutil


class PlayerI(Streaming.Player):

    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = ""
        self.skip = False
        self.listMusic = []
        self.currentMusic = "" 
        self.folder_path = "C:/Users/Killian/PycharmProjects/pythonProject/music"

    def initMedia(self, file):
        self.media = self.instance.media_new_path(file)
        self.media.add_option("sout=#standard{access=http,mux=ogg,dst:8080/music}")
        self.media.add_option("--no-sout-all")
        self.media.add_option("--sout-keep")
        self.media.get_mrl()

    def startProcessing(self, current = None):
        self.player.set_media(self.media)
        self.player.play()
        time.sleep(2)
        while True:
            if (self.player.is_playing() == 0):
                self.player.stop()
                break
            if self.skip:
                self.player.stop()
                break

    def asyncInput(self, current = None):
        while True:
            command = input(">> ")
            if command == "-skip" or command == "-quit":
                self.skip = True
                break
            if command == "-pause":
                self.player.pause()
            elif command == "-resume":
                self.player.play()
            else:
                print("else")

    def getAllMusic(self, current = None):
        self.listMusic.clear()
        for path, dirs, files in os.walk(self.folder_path):
            for filename in files:
                self.listMusic.append(filename) #changer pour affichage enlever /music
        return self.listMusic

    def choseMusic(self, musicChose, current = None):
        for music in self.listMusic:
            if(musicChose.upper() in music.upper()):
                self.currentMusic = os.path.basename(self.folder_path) + "/" + music
        self.playMusic(self.currentMusic)
    
    def playMusic(self, current = None):
        self.initMedia(self.currentMusic)
        Thread(target=self.startProcessing).start()
        Thread(target=self.asyncInput).start()

    def supprimerMusique(self, music, current = None):
        print(music)
        file_path = Path('music' + '/' + music)
        try:
            file_path.unlink()
        except OSError as e:
            print(f"Error: {e.strerror}")
        self.listMusic = self.getAllMusic()

    
    def renommerMusique(self, music, new_name, current = None):
        try:
            os.rename("music/" + music, "music/" + new_name + ".mp3")
        except OSError as e:
            print(f"Error: {e.strerror}")
        self.listMusic = self.getAllMusic()
    
    def uploadMusic(self, path, current = None):
        print(os.path.basename(path))
        shutil.move(path, 'music/')



with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("SimplePrinterAdapter", "default -p 10000")
    object = PlayerI()
    adapter.add(object, communicator.stringToIdentity("SimplePrinter"))
    adapter.activate()
    communicator.waitForShutdown()

