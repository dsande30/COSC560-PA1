# COSC 560 Programming Assignment 1
## Dakota Sanders & Andrey Karnauch

### Section 1: Installation
To run our HTTP server, install Python 3, which can be found [here](https://www.python.org).

### Section 2: Operation
Once installed, the server can be started by running `[your python installation] router.py`. 
From there, open up a browser and navigate to `localhost:8888`. Our server runs on port 8888.

![](./screenshots/homepage.png "Homepage")

If you see a screen like the provided screenshot, our program is running. Normally a web server is configured to serve content out of a certain directory. We have chosen to configure ours to serve from the `site/` directory in our repository.

**NOTE:** Our code has only been tested on Safari and Google Chrome. For some reason, file uploads do not work on Safari, and will cause problems. Do not upload files on Safari.

Page A and page B demonstrate our ability to handle basic `GET` requests. Page C and page D demonstrate our ability to handle form data via `POST` requests and `multipart/form-data`. There are also links to the directory listing page and file uploads page.

![](./screenshots/survey.png "Page C")

Page C allows the user to fill out a survey asking basic user information. Upon submitting, the site sends a `POST` request to our server, which handles the data and stores it in a text file inside of `data/survey.txt` in the repository.

Page D allows the user to upload a file, which sends a `multipart/form-data` request to the server. To assist grading, we store the file in `data/` in the repository to be accessed as needed.
**NOTE:** We make no guarantees as to the speed of the upload process. This may take quite a while, especially for large files. We do not implement a loading screen, but you may find that your browser indicates the progress of the upload.

![](./screenshots/dir.png "Directory Listing")

The directory listing page shows all available pages within the `site/` subdirectory of our repository. It also shows the file sizes. These are clickable links, which will direct you to the file or directory you choose.

![](./screenshots/uploads.png "File uploads")

The file upload page allows you to see all files uploaded from Page D. To simplify this process for the sake of this project, we only allow a limited number of file extensions to be redownloaded, which are listed at the top of the page. To view the file, simply click on the link provided. **NOTE:** The server does support any type of file upload, just not redownload.

### Section 3: Code Structure
To assist in grading, we will lay out a basic overview of the structure of our code.

`router.py` is our direct server code. It opens a socket and connects on port 8888. Once it receives a connection, it spawns a new helper thread to handle the request. This allows `router` to be as available as possible to handle new requests.

These helper threads instantiate an object of type `RequestParser`, which can parse the request for important information. It then instantiates a `Responder` object, which uses that information to send a correct HTTP response to the user.