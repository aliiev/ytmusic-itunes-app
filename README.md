# ytmusic-itunes-app

Downloads music from Youtube and moves it to iTunes for further sync.

 1. Run `python app.py`;
 2. Insert Youtube Video/Playlist URL;
 3. Click "Download" button;
 4. After successfull download open iTunes and sync with your device.

### DEPENDENCIES

 - **Packages**: PyQt5, yt-dlp, shutil, sys, os. You can install it with the command: `pip install PyQt5 yt-dlp`;
 - **[ffmpeg and ffprobe](https://www.ffmpeg.org/)**: Required for merging separate video and audio files as well as for various post-processing tasks. Just copy it to the root of the project.
