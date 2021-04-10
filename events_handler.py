import pygame
from communicator import Communicator
from messages import *


DEFAULT_DISPLAY_RESOLUTION = (800, 600)


class EventsHandler(object):
    def __init__(self, user_socket):
        self.display_resolution = DEFAULT_DISPLAY_RESOLUTION
        self.user_socket = user_socket
        self.communicator = Communicator()

    def display_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.user_socket.close()

            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                self.display_resolution = (width, height)
                screen = pygame.display.set_mode(self.display_resolution, pygame.RESIZABLE)
                self.communicator.send_enc_message(DisplayResolutionChange(self.display_resolution),
                                                   True, self.user_socket)


