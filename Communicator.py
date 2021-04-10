import socket
import pickle
from AESCipher import AESCipher


LEN_OF_LENGTH = 6
BYTES_AMOUNT = 1024
PICKLE_BIT = 'T'
IMAGE_SUFFIX = 'IMG'


class Communicator(object):
    def __init__(self):
        self.aes_cipher = AESCipher()

    def send_enc_message(self, message, to_pickle, client_socket):
        """
        :param message: message to send over the socket.
        :param to_pickle: a boolean which means whether to pickle the message to not.
        :param client_socket: the socket to send the message on.
        """
        if to_pickle:
            message = f'{pickle.dumps(message)}{PICKLE_BIT}'

        if message.find(IMAGE_SUFFIX) != -1:
            encrypted_message = self.aes_cipher.encrypt_image_data(message[:-len(IMAGE_SUFFIX)])

        else:
            encrypted_message = self.aes_cipher.encrypt(message)
        # message sending protocol:
        # first you send the length of the message
        # and then the message itself.
        try:
            client_socket.send(str(len(encrypted_message)).zfill(LEN_OF_LENGTH))
            client_socket.send(encrypted_message)
        except socket.error:
            client_socket.close()
        except Exception as e:
            pass

    def get_dec_message(self, client_socket):
        """
        :param client_socket: the client to receive the message from.
        :return: the client's message.
        """
        message_length = self.get_message_length(client_socket)
        encrypted_message = self.get_message_by_length(message_length, client_socket)
        if encrypted_message.find(IMAGE_SUFFIX) is not -1:
            return self.aes_cipher.encrypt_image_data(encrypted_message[:-len(IMAGE_SUFFIX)])
        decrypted_message = self.aes_cipher.decrypt(encrypted_message)
        if decrypted_message[-1:] == PICKLE_BIT:
            return pickle.loads(decrypted_message)
        return decrypted_message

    @staticmethod
    def get_message_length(client_socket):
        """
        the function receives the length of the message.
        :return: the message length
        """
        message_length = ""
        while len(message_length) != LEN_OF_LENGTH:
            message_length += client_socket.recv(LEN_OF_LENGTH - len(message_length))
        return int(message_length)

    @staticmethod
    def get_message_by_length(message_length, client_socket):
        """
        :param message_length: the length of the message.
        :param client_socket: the socket to listen on.
        :return: the message that was received.
        """
        content = ""
        while len(content) != message_length:
            content += client_socket.recv(message_length - len(content))
        return content


