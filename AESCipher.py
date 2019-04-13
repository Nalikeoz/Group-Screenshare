from Crypto.Cipher import AES
from hashlib import md5

ENC_KEY = md5('key').hexdigest()
PADDING_CHAR = '*'
START_OF_ENC = 'START'
IMAGE_SUFFIX = 'IMG'


class AESCipher(object):
    """
    The object if used to encrypt and decrypt
    strings.
    """
    def __init__(self):
        self.encryption_suite = AES.new(ENC_KEY)

    def encrypt(self, message):
        """
        @param message: the message that will be encrypted(string).
        @return: the function gets a string and return his AES encryption.
        """
        enc_message = message + PADDING_CHAR * (16 - len(message) % 16)
        enc_message = self.encryption_suite.encrypt(enc_message)
        return enc_message

    def decrypt(self, encrypted_message):
        """
        @param encrypted_message: an AES encrypted message with our secret key.
        @return: the function gets an encrypted message and returns his decrypted string.
        """
        dec_message = self.encryption_suite.decrypt(encrypted_message)
        dec_message = dec_message.rstrip(PADDING_CHAR)
        return dec_message

    def encrypt_image_data(self, image_data):
        """

        :param image_data: raw data of an image.
        :return: the encrypted image raw data (the the protocol).
        """
        last_16_bytes = image_data[-16:]
        enc_image = self.encrypt(last_16_bytes)
        enc_image = image_data[:-16] + START_OF_ENC + enc_image + IMAGE_SUFFIX
        return enc_image

    def decrypt_image(self, enc_image_data):
        """

        :param enc_image_data: encrypted image raw data.
        :return: the decrypted image raw data.
        """
        encrypted_bytes = enc_image_data[enc_image_data.find(START_OF_ENC) + len(START_OF_ENC):]
        dec_last_16 = self.decrypt(encrypted_bytes)
        enc_image_data = enc_image_data[:enc_image_data.find(START_OF_ENC)] + dec_last_16
        return enc_image_data
