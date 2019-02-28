# COSC 560 Programming Assignment 1
## Dakota Sanders & Andrey Karnauch

### Section 1: Installation
To run our HTTP server, install Python 3, which can be found [here](https://www.python.org).

### Section 2: Operation
Once installed, the server can be started by running `[your python installation] router.py`. 
From there, open up a browser and navigate to `localhost:8888`. Our server runs on port 8888.

![](./screenshots/homepage.png "Homepage")

If you see a screen like the provided screenshot, our program is running. Normally a web server is configured to serve content out of a certain directory. We have chosen to configure ours to serve from the root of our repository. 

Page A and page B demonstrate our ability to handle basic `GET` requests. Page C and page D demonstrate our ability to handle form data via `POST` requests and `multipart/form-data`.

![](./screenshots/survey.png "Survey")

Page C allows the user to fill out a survey asking basic user information. Upon submitting, the site sends a `POST` request to our server, which handles the data and stores it in a text file inside of `data/survey.txt` in the repository.

Page D allows the user to upload a file, which sends a `multipart/form-data` request to the server. To assist grading, we store the file in `data/` in the repository to be accessed as needed.

### Section 3: Code Structure
To assist in grading, we will lay out a basic overview of the structure of our code.

`router.py` is our direct server code. It opens a socket and connects on port 8888. Once it receives a connection, it spawns a new helper thread to handle the request. This allows `router` to be as available as possible to handle new requests.

These helper threads instantiate an object of type `RequestParser`, which can parse the request for important information. It then instantiates a `Responder` object, which uses that information to send a correct HTTP response to the user.