# spotify-virtual-room
This web application allows people democratically change the spotify song that is playing. There is a virtual room, refered by a room code, a host, who has full control of the playback state and can skip or play any song of his choice, and guests, people who can vote to change skip the song that is currently playing and, if the host allows, can also play/pause the song.  ps: I did not developed this webapp. I followed a tutorial. The credits goes to Tech With Tim https://www.youtube.com/c/TechWithTim

REQUIREMENTS:
  Django 4.0.4
  Node.js v16.14.2
  
To run this code on your local device, it is necessary to go to music_controller/spotify/credentials.py and add the CLIENT_ID and CLIENT_SECRET credentials there. To get those credentials, you need to create an account at Spotify and then create a new app at https://developer.spotify.com/dashboard/applications


Setting up (after the you add the CLIENT_ID and CLIENT_SECRET to music_controller/spotify/credentials.py)
  1. Open a terminal window, `cd` into music_controller and run `py manage.py runserver`
  2. Then, on a new terminal window at music_controller/frontend, run `npm run dev`
  3. After that, on your local browser, go to http//:127.0.0.1:8000
  4. Enjoy
