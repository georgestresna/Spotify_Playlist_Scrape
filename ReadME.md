# **Spotify Playlist Web Scraper**



### This app takes an input from the user: the link to a Spotify Playlist(accessible by right-clicking the playlist and clicking on Share -> Copy Link) and creates 2 files. 
- a .txt file, containing general info about the playlist
- a .csv file containing all of the tracks in the playlist along with the corresponding artist/s

### It has a sample playlist in the repository above. The program takes the title of the Playlist and creates the 2 files with the same title
- example: *A playlist named "Road Trip" would output 2 files, `Road_Trip.txt` and `Road_Trip.csv`*

---

The CSV is *utf-8* encoded, the deleted tracks are marked as `Unavalable song`.



---

Future improvements: Add another column to the CSV file, writing down if the song is or isn't avalable to play on Spotify.