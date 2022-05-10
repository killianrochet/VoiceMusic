package com.example.voicemusic;
import android.annotation.SuppressLint;
import android.media.MediaPlayer;
import android.os.Build;
import androidx.annotation.RequiresApi;

import com.example.voicemusic.Streaming.PlayerPrx;
import com.zeroc.Ice.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class Client
{

    String http = "http://127.0.0.1:8080/music";
    public com.zeroc.Ice.Communicator communicator;
    public com.zeroc.Ice.ObjectPrx base;
    public com.example.voicemusic.Streaming.PlayerPrx printer;
    public List<String> music;
    public MediaPlayer mediaPlayer;



    public Client() {
        this.communicator = com.zeroc.Ice.Util.initialize();
        this.base = communicator.stringToProxy("SimplePrinter:tcp -h 192.168.0.40 -p 10000");
        this.printer = com.example.voicemusic.Streaming.PlayerPrx.checkedCast(base);
    }

    public Communicator getCommunicator() {
        return communicator;
    }

    public void setCommunicator(Communicator communicator) {
        this.communicator = communicator;
    }

    public ObjectPrx getBase() {
        return base;
    }

    public void setBase(ObjectPrx base) {
        this.base = base;
    }

    public PlayerPrx getPrinter() {
        return printer;
    }

    public void setPrinter(PlayerPrx printer) {
        this.printer = printer;
    }

    public List<String> getMusic() {
        return music;
    }

    public void setMusic(List<String> music) {
        this.music = music;
    }

    public List<String> getAllMusic(){
        List<String> allMusic = new ArrayList<String>(Arrays.asList(printer.getAllMusic()));
        return allMusic;
    }

    public void jouerMusique(){
        printer.choseMusic("Lady.mp3");
    }

    public static void main(String[] args){
        Client client = new Client();
        System.out.println(Arrays.toString(client.printer.getAllMusic()));
        client.jouerMusique();
    }


}
