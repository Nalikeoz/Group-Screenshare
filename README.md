# Screen-Share-Stream
The program allows you sharing your screen to multiple users at a time,
while all data (screenshots) are encrypted with AES encryption.
In Addition, every client can change his display resolution and still enjoy a good looking 
image.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation
The program uses some libraries that are not included in the basic python 2.7 pack and
in order to make the project up and running you may install the following libraries:
```
pip install StringIO
pip install pygame
pip install pycrypto
pip install pillow
```

## Deployment
In order to start using the the project you'll have to follow the following steps:
1. Open **Client.py** with a text editor and change the SERVER_IP const to your streamer's local IP address.
2. Run **Streamer.py** file and wait for a 'Server started [...]' message.
3. Run **Client.py** to start watching the screen share stream (you may run more than one client).

## Built With
* [PyCharm](https://www.jetbrains.com/pycharm/) - Working framework.
* [Python 2.7](https://www.python.org/)         - Programming language.

## Author
* **Nadav Shamir** - [Nalikeoz](https://github.com/Nalikeoz)
