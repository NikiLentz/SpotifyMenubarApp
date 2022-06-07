
from SwSpotify import spotify
import rumps
import threading
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import system
import ClientVariables

class SpotifyMenubarApp(object):
    def __init__(self):
        self.app = rumps.App("SpotifyMenubarApp", title="🤨")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ClientVariables.ID,
                                               client_secret=ClientVariables.SECRET,
                                               redirect_uri=ClientVariables.URI,
                                               scope="user-modify-playback-state user-read-playback-state"))
        
        self.next_button = rumps.MenuItem(title="Next", callback=self.next_song)
        self.start_pause_button = rumps.MenuItem(title='Play/Pause', callback=self.play_pause)
        self.app.menu = [self.start_pause_button, self.next_button]
        self.current = ""
        t1 = threading.Thread(target=self.check_title_loop, args=[])
        t1.start()

    def run(self):
        self.app.run()   
    
    def play_pause(self, sender):
        if(self.sp.currently_playing()["is_playing"]):
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    def next_song(self, sender):
        self.sp.next_track()
        try:
            self.check_current_title()
        except Exception as e:
            pass

    

    def check_title_loop(self):
        self.current = ""
        while(self.current == ""):
            try:
                self.check_current_title()
            except Exception as f:
                continue
        while 1:
            time.sleep(1)
            try:
                self.check_current_title()
            except Exception as e:
                continue
        
    def check_current_title(self):
        new = spotify.get_info_mac()
        if self.current != new:
                    self.current = new
                    self.app.title = self.current[0] + ' - ' + self.current[1]
                    


if __name__ == '__main__':
    testapp = SpotifyMenubarApp()
    testapp.run()

    
    