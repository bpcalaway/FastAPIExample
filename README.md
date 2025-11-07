This is a very basic API example designed to cover some very specific parts of the app workflow:
- Check current location to see if you are in a claimed area and pull the data on it
- Claim an area by sending a set of vertices and a song choice, this should be decided in app
- Search a song? Haven't decided if this part of it should be in the API or not

A lot of this won't be covered in the API such as:
- determining your location or tracking where you walk
- Any kind of UI work for deciding which song you want
- Specifics for the map

Setup:
In order to start this you'll need python 3.12, pip, and pipenv. Then run 'pipenv shell'.  After that, you can run it locally with 'fastapi dev app.py' and check the endpoints on localhost:8000/docs

Game Theory:
- Basic theory is that you open the app to capture a zone while out on a walk/run
    - Part of this is going to be a speed limit, I'm thinking like 7mph, to avoid cars/biking making it too easy
    - While the app is open, you're hearing the song choice from whatever is currently capturing the area.  (Maybe also the previous capture that has decayed?)
    - You need to roughly fill a loop.  Call it within a city block or so, call it within 200 meters of the start point
- Captured zones will have a song associated with it by the user.  I'm assuming spotify or soundcloud since they allow embedding during dev work
    - The song will be part of a unique lookup that includes both the user's profile name and the set of vertices associated with their walk.
    - The zone will "decay" over time, I'm thinking 24 hours.  
        - Decay is the major gameplay feature for not allowing instant recaptures.  Assuming 24 hours...
            - After 12 hours, half of your zone can be captured.
            - After 18 hours, 3/4 of your zone can be captured
        - As such, if Zone B completely envelops Zone A, but Zone A is only 12 hours old, at most half of it can be captured
        - Steal area from the decaying zone based off of the center of the Zone B area, so if it's mostly to the East you'd steal the Eastern half of Zone A
- There should probably be a limit on the maximum size you can capture, but I think it's kind of funny if there isn't one
- Some kind of leaderboard for most area captured, maybe also break it down by artist (biggest fan, local fan, etc)