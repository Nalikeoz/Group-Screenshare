import socket
from select import select
from Communicator import Communicator
from Screenshot import Screenshot
from threading import Thread
from Messages import *

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8081
IMAGE_SUFFIX = 'IMG'
DEFAULT_DISPLAY_RESOLUTION = (800, 600)


class Streamer(object):
    """
    the server will be the "host" of the screen share,
    basically, will share his screen to all the
    clients.
    """
    def __init__(self):
        """
        The constructor function of the main server.
        """
        self.streamer_socket = socket.socket()
        self.online_users = {}  # {socket: display resolution}.
        self.communicator = Communicator()
        self.screenshot = Screenshot()
        self.running = True

    def bind_socket(self):
        """
        The function binds the server socket and starts listening
        for connections.
        """
        self.streamer_socket.bind((SERVER_IP, SERVER_PORT))
        self.streamer_socket.listen(1)
        print('================================================')
        print(f'[STREAMER] Starting server on: {SERVER_IP}:{str(SERVER_PORT)}))
        print('================================================')

    def new_user(self):
        """
        The function accepts a new connection,
        adds the user's socket to the online users dictionary
        and starts sending him screenshots.
        """
        client_socket, client_address = self.streamer_socket.accept()
        client_ip_address = client_address[0]
        self.online_users[client_socket] = DEFAULT_DISPLAY_RESOLUTION
        Thread(target=self.send_screenshots, args=[client_socket]).start()
        print('[STREAMER] New Online User [' + str(client_ip_address) + ']')

    def send_screenshots(self, user_socket):
        """

        :param user_socket: the socket to send screenshots to.
        the function sends screenshots to a user's socket.
        if there's no online user with that socket the function returns.
        """
        if user_socket in self.online_users.keys():
            while self.running:
                try:
                    user_display_resolution = self.online_users[user_socket]
                    image_data = self.screenshot.get_screenshot_data(image_resize=user_display_resolution) + IMAGE_SUFFIX
                    self.communicator.send_enc_message(image_data, False, user_socket)
                except (KeyError, socket.error):
                    self.remove_user(user_socket)
                    break
        else:
            return None

    def remove_user(self, user_socket):
        """

        :param user_socket: socket to remove from the online users dictionary.
        the function removes a user from the online users dictionary.
        """
        try:
            del self.online_users[user_socket]
            user_socket.close()
            print('[STREAMER] User has been disconnected.')
        except(KeyError, socket.error):
            pass

    def define_message_type(self, message, user_socket):
        """
        :param message: a new message the was received.
        :param user_socket: the socket that the message was received from.
        the function defines the message type and calls the wanted function.
        """
        if isinstance(message, DisplayResolutionChange):
            self.online_users[user_socket] = message.screen_resolution

    def run_server(self):
        while self.running:
            rlist, wlist, xlist = select(list(self.online_users.keys()) + [self.streamer_socket], [], [])
            for user_socket in rlist:
                if user_socket is self.streamer_socket:
                    self.new_user()
                else:
                    try:
                        message = self.communicator.get_dec_message(user_socket)
                        self.define_message_type(message, user_socket)
                    except:
                        self.remove_user(user_socket)


def main():
    server = Streamer()
    server.bind_socket()
    server.run_server()


if __name__ == "__main__":
    main()

