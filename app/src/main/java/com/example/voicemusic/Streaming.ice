module Streaming {
    sequence<string> strTab;
    interface Player
    {
       void startProcessing();
       void asyncInput();
       strTab getAllMusic();
       void choseMusic(string musicChose);
       void playMusic();
       void initMedia(string file);
       void supprimerMusique(string music);
       void renommerMusique(string music, string newname);
       void uploadMusic(string path);
    }
}