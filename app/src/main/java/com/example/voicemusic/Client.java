package com.example.voicemusic;
import com.zeroc.Ice.*;

import java.util.Arrays;

public class Client
{
    public static void main(String[] args)
    {
        try(com.zeroc.Ice.Communicator communicator = com.zeroc.Ice.Util.initialize(args))
        {
            com.zeroc.Ice.ObjectPrx base = communicator.stringToProxy("SimplePrinter:default -p 10000");
            com.example.voicemusic.Streaming.PlayerPrx printer = com.example.voicemusic.Streaming.PlayerPrx.checkedCast(base);
            if(printer == null)
            {
                throw new Error("Invalid proxy");
            }
            System.out.println(Arrays.toString(printer.getAllMusic()));
        }
    }
}
