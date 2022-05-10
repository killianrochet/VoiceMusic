import vlc
import os
import time
import Streaming
import sys, Ice
from os import walk
from threading import Thread
from pathlib import Path
import shutil
import speech_recognition as sr
import re
import unidecode


class PlayerI(Streaming.Player):

    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = ""
        self.skip = False
        self.listMusic = []
        self.currentMusic = ""
        self.folder_path = "C:/Users/Killian/PycharmProjects/pythonProject/music"
        self.myText = ""
        self.r = sr.Recognizer()
        self.action_list = ["joue", "lis", "play", "pause", "arret", "stop", "quitte", "augment", "redui"]
        self.action = ''
        self.subject = ""

    def initMedia(self, file):
        self.media = self.instance.media_new_path(file)
        self.media.add_option("sout=#standard{access=http,mux=ogg,dst=:8080/music}")
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

    def speechToText(self, current = None):

        with sr.Microphone() as source:
            print("Calibration...")
            self.r.adjust_for_ambient_noise(source, duration=2)
            print("Micro calibré, vous pouvez parler !")

            audio = self.r.listen(source, phrase_time_limit=4)

            print("Ecoute terminée, traitement...")
            try :
                self.MyText = self.r.recognize_google(audio, language="fr-FR")
                self.MyText = self.MyText.lower()
                self.MyText = unidecode.unidecode(self.MyText)
                print(self.MyText)
                readSTT(self.MyText)
            except :
                print("Erreur lors de la commande vocale")

    def readSTT(self, axiome_value, current = None):
        decompose = re.split(r' +', axiome_value)

        for i in range(len(self.action_list)):
            for j in range(len(decompose)):
                if re.match(rf"{self.action_list[i]}.", decompose[j]) or re.match(decompose[j], self.action_list[i]):
                    self.action = self.action_list[i]
                    decompose.remove(decompose[j])
                    break
                if self.action != '': break

        print(self.action)
        self.subject = " ".join(decompose)
        actionRead(self.action, self.subject)

    def actionRead(self, action, current = None):
        if(action in ("lis", "joue")):
            self.choseMusic(self.subject)
            print(f"Lancement de la musique : {self.subject}")
        elif(action == "play"):
            print("Reprise de la musique")
        elif(action == "pause"):
            print("Mise en pause de la musique")
        elif(action in ("stop", "arret")):
            print("Arrêt de la musique")
        elif(action == "augment"):
            print("Augmentation du volume")
        elif(action == "redui"):
            print("Baisse du volume")
        elif(action == "quitte"):
            print("Fermeture de l'application")
        else:
            print("Aucune action prévue détectée")




with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("SimplePrinterAdapter", "default -p 10000")
    object = PlayerI()
    adapter.add(object, communicator.stringToIdentity("SimplePrinter"))
    adapter.activate()
    communicator.waitForShutdown()

