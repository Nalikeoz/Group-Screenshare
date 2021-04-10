import socket
import pygame
from Communicator import Communicator
import StringIO
from EventsHandler import EventsHandler

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8081
SCREEN_NAME = ''
DEFAULT_DISPLAY_RESOLUTION = (800, 600)


class Client(object):
    """
    Client object define an observer.
    He can see the streamer's screen share.(multiple clients
    can see one stream).
    """
    def __init__(self):
        """
        the constructor function of the client.
        """
        self.client_socket = socket.socket()  # the socket of the client.
        self.communicator = Communicator()
        self.events_handler = EventsHandler(self.client_socket)
        self.running = True
        self.display_resolution = DEFAULT_DISPLAY_RESOLUTION
        self.screen = self.get_display()

    def connect_to_server(self):
        """
        The function connects to the server.
        """
        self.client_socket.connect((SERVER_IP, SERVER_PORT))
        print('[CLIENT] connected to streamer.')

    def get_image(self):
        """
        the function gets a new screenshot from the streamer.
        :return: a new screenshot.
        """
        try:

            message = self.communicator.get_dec_message(self.client_socket)
            output = StringIO.StringIO(message)
            image = pygame.image.load(output)
            return image

        except pygame.error:
            return None
        except socket.error:
            self.close_connection()

    def change_image_on_screen(self, image):
        """
        :param image: PIL image of the streamer's screen.
        the function updated the display image to the new image.
        """
        try:
            self.screen.blit(image, (0, 0))
            pygame.display.flip()
        except pygame.error:
            pass

    def get_display(self):
        """
        :return: a pygame screen(where the screen will be shown)
        """
        pygame.init()
        screen = pygame.display.set_mode(self.display_resolution, pygame.RESIZABLE)
        pygame.display.set_caption(SCREEN_NAME, SCREEN_NAME)
        return screen

    def run_client(self):
        while self.running:
            try:
                image = self.get_image()
                if image is not None:
                    self.change_image_on_screen(image)
                self.events_handler.display_events(self.screen)
            except pygame.error:
                self.running = False
                self.client_socket.close()

    def close_connection(self):
        """
        The function stops the client functions and disconnects
        from the stream.
        """
        self.running = False
        self.client_socket.close()


def main():
    client = Client()
    client.connect_to_server()
    client.run_client()


if __name__ == "__main__":
    main()