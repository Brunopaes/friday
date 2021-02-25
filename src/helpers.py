# -*- coding: utf-8 -*-
from google.cloud import bigquery
from PIL import Image

import pytesseract
import telebot
import numpy
import json
import cv2
import os


def read_json(path):
    """This function opens a json file and parses it content into a python
    dict.

    Parameters
    ----------
    path : str
        The json file path.

    Returns
    -------
    json.load : dict
        The json content parsed into a python dict.

    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(e.args[-1])


def resize(max_width, max_height, image_path, out_dir, upscale=False):
    """This function resizes images into a directory.

    Parameters
    ----------
    max_width : int
        Max resized width.
    max_height : int
        Max resized height.
    image_path : str
        Images path.
    out_dir : str
        Goal directory.
    upscale : bool
        Upscale option. Default False.

    Returns
    -------

    """
    dir_path = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(dir_path, image_path)
    images = os.listdir(image_path)

    for counter, im in enumerate(images):
        image = cv2.imread(os.path.join(image_path, im))
        height = image.shape[0]
        width = image.shape[1]

        if upscale:
            if width < max_width:
                ratio = max_width / width
                new_height = int(ratio * height)
                image = cv2.resize(image, (max_width, new_height))

                if new_height < max_height:
                    ratio = max_height / new_height
                    new_width = int(ratio * max_width)
                    image = cv2.resize(image, (new_width, max_height))
        else:
            if width > max_width:
                ratio = max_width / width
                new_height = int(ratio * height)
                image = cv2.resize(image, (max_width, new_height))

                if new_height > max_height:
                    ratio = max_height / new_height
                    new_width = int(ratio * max_width)
                    image = cv2.resize(image, (new_width, max_height))

        out_path = os.path.join(out_dir, im)
        cv2.imwrite(out_path, image)


def ocr(path, lang='eng'):
    """Optical Character Recognition function.

    Parameters
    ----------
    path : str
        Image path.
    lang : str, optional
        Decoding language. Default english.

    Returns
    -------

    """
    image = Image.open(path)

    vectorized_image = numpy.asarray(image).astype(numpy.uint8)

    vectorized_image[:, :, 0] = 0
    vectorized_image[:, :, 2] = 0

    im = cv2.cvtColor(vectorized_image, cv2.COLOR_RGB2GRAY)

    return pytesseract.image_to_string(
        Image.fromarray(im),
        lang=lang
    )[:5]


def crop_image(path, coordinates):
    """This function crops a given image.

    Parameters
    ----------
    path : str
        To be cropped image path.
    coordinates : tuple
        Cropping bounding boxes.

    Returns
    -------

    """
    Image.open(path).crop(coordinates).save(path)


def set_path():
    """This function sets gcp_settings.json in PATH.

    Returns
    -------

    """
    path = os.path.abspath('settings/gcp_settings.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path


def start_connection():
    """Function used to start connection with GCP's Big Query.

    Returns
    -------

    """
    set_path()
    return bigquery.Client()


def check_user(user):
    """This function checks user permissions.

    Parameters
    ----------
    user : int
        User id.

    Returns
    -------

    """
    if user != 144068478:
        raise AttributeError


def courier(message, chat_id=-1001164675059):
    """This function courier - through telegram bot - a message.

    Parameters
    ----------
    message : str
        To be couriered message.
    chat_id : int
        To be messaged chat id.

    Returns
    -------

    """
    telebot.TeleBot(**read_json('settings/telegram_settings.json'))\
        .send_message(chat_id, message)


class StoreMetadata:
    def __init__(self, metadata):
        self.metadata = metadata
        self.parsed_metadata = {
            'sender_id': None,
            'first_name': None,
            'last_name': None,
            'username': None,
            'chat_id': None,
            'chat_title': None,
            'message': None,
        }
        self.query = """
            INSERT INTO
                `mooncake-304003.misc.message-metadata`
            VALUES
                ({sender_id}, "{first_name}", "{last_name}", 
                "{username}", {chat_id}, "{chat_title}", 
                "{message}", CURRENT_DATETIME("America/Sao_Paulo"))
        """
        self.client = start_connection()

    def process_group(self):
        """This function processes groups metadata.

        Returns
        -------
        parsed_metadata : dict
            Parsed metadata

        """
        return {
            'sender_id': self.metadata.get('from').get('id'),
            'first_name': self.metadata.get('from').get('first_name'),
            'last_name': self.metadata.get('from').get('last_name'),
            'username': self.metadata.get('from').get('username'),
            'chat_id': self.metadata.get('chat').get('id'),
            'chat_title': self.metadata.get('chat').get('title'),
            'message': self.metadata.get('text'),
        }

    def process_private(self):
        """This function processes privates metadata.

        Returns
        -------
        parsed_metadata : dict
            Parsed metadata

        """
        return {
            'sender_id': self.metadata.get('from').get('id'),
            'first_name': self.metadata.get('from').get('first_name'),
            'last_name': self.metadata.get('from').get('last_name'),
            'username': self.metadata.get('from').get('username'),
            'chat_id': self.metadata.get('chat').get('id'),
            'chat_title': self.metadata.get('chat').get('username'),
            'message': self.metadata.get('text'),
        }

    def check_processing_type(self):
        """This function checks if it's a private or group message.

        Returns
        -------
        parsed_metadata : dict
            Parsed metadata

        """
        return {
            'private': self.process_private,
            'group': self.process_group,
            'supergroup': self.process_group,
        }.get(self.metadata.get('chat').get('type'))()

    def querying(self, parsed_metadata):
        """This function queries into GCP.

        Parameters
        ----------
        parsed_metadata : dict
            Parsed metadata

        """
        self.client.query(self.query.format(**parsed_metadata))

    def __call__(self, *args, **kwargs):
        self.querying(self.check_processing_type())
