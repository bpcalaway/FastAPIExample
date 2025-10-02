This is a very basic API example designed to cover some very specific parts of the app workflow:
- Check current location to see if you are in a claimed area and pull the data on it
- Claim an area by sending a set of vertices and a song choice, this should be decided in app
- Search a song? Haven't decided if this part of it should be in the API or not

A lot of this won't be covered in the API such as:
- determining your location or tracking where you walk
- Any kind of UI work for deciding which song you want
- Specifics for the map

In order to start this you'll need python 3.13 and pip. Then run 'pip install fastapi' and 'pip install "fastapi[standard]"'.  After that, you can run it locally with 'fastapi dev app.py' and check the endpoints on localhost:8000/docs