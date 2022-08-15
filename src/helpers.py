# -*- coding: utf-8 -*-
from imgurpython import ImgurClient
from google.cloud import bigquery
from tqdm import tqdm
from PIL import Image

import pytesseract
import youtube_dl
import requests
import telebot
import numpy
import json
import math
import cv2
import io
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
    if user not in (144068478, 196426350016331776, 852363712043417610):
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
        self.query = """
            INSERT INTO
                `mooncake-304003.misc.message-metadata`
            VALUES
                ({sender_id}, "{first_name}", "{last_name}", 
                "{username}", {chat_id}, "{chat_title}", 
                "{message}", CURRENT_DATETIME("America/Sao_Paulo"), 
                "{system_origin}")
        """
        self.client = start_connection()

    def querying(self):
        """This function queries into GCP.

        Parameters
        ----------

        Returns
        -------

        """
        self.client.query(self.query.format(**self.metadata))

    def __call__(self, *args, **kwargs):
        self.querying()


class TelegramPayloadParser:
    def __init__(self, metadata):
        self.metadata = metadata.json
        self.parsed_metadata = {
            'sender_id': None,
            'first_name': None,
            'last_name': None,
            'username': None,
            'chat_id': None,
            'chat_title': None,
            'message': None,
            'system_origin': 'Telegram'
        }

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
            'system_origin': 'Telegram'
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
            'system_origin': 'Telegram'
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

    def __call__(self, *args, **kwargs):
        return self.check_processing_type()


def discord_payload_parser(message):
    """This funtion parses discord message object into json payload.

    Parameters
    ----------
    message :
        Discord message object

    Returns
    -------

    """
    try:
        return {
            'sender_id': message.author.id,
            'first_name': None,
            'last_name': None,
            'username': message.author.name,
            'chat_id': message.guild.id,
            'chat_title': message.guild.name,
            'message': message.content,
            'system_origin': 'Discord'
        }
    except AttributeError:
        try:
            return {
                'sender_id': message.author.id,
                'first_name': None,
                'last_name': None,
                'username': message.author.name,
                'chat_id': message.author.id,
                'chat_title': message.author.name,
                'message': message.content,
                'system_origin': 'Discord'
            }
        except AttributeError:
            try:
                return {
                    'sender_id': message.author.id,
                    'first_name': None,
                    'last_name': None,
                    'username': message.author.name,
                    'chat_id': message.author.id,
                    'chat_title': message.guild.name,
                    'message': message.message.content,
                    'system_origin': 'Discord'
                }
            except AttributeError:
                return {
                    'sender_id': message.author.id,
                    'first_name': None,
                    'last_name': None,
                    'username': message.author.name,
                    'chat_id': message.author.id,
                    'chat_title': message.author.name,
                    'message': message.message.content,
                    'system_origin': 'Discord'
                }


def youtube_video_player(url):
    """This function returns youtube audio links.

    Parameters
    ----------
    url : string
        Video URL.

    Returns
    -------
    y_dl : tuple
        audio url with ffmpeg_options

    """
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 '
                          '-reconnect_delay_max 5',
        'options': '-vn'
    }

    with youtube_dl.YoutubeDL({
        'format': 'bestaudio',
        'noplaylist': 'True'
    }) as y_dl:

        return (y_dl.extract_info(
            url,
            download=False
        )['formats'][0]['url'], ffmpeg_options)


class EloCalculator:
    def __init__(self, winner, ratings, competitors):
        self.k = 50
        self.winner = winner
        self.ratings = ratings
        self.competitors = competitors
        self.response = {}

    @staticmethod
    def calculating_win_probability(rating_1, rating_2):
        return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating_2 - rating_1) / 400))

    def updating_elo(self, pa, pb):
        if self.winner == self.competitors[0]:
            ra = self.ratings[0] + (self.k * (1 - pa))
            rb = self.ratings[1] + (self.k * (0 - pb))
        else:
            ra = self.ratings[0] + (self.k * (0 - pa))
            rb = self.ratings[1] + (self.k * (1 - pb))

        self.ratings = ra, rb

    def __call__(self, *args, **kwargs):
        self.updating_elo(
            self.calculating_win_probability(*self.ratings),
            self.calculating_win_probability(*(self.ratings[::-1]))
        )

        for competitor, rating in zip(self.competitors, self.ratings):
            self.response[competitor] = rating

        return self.response


class ImgurDownloader:
    """This class downloads images from imgur website.

    Can handle albums and solo images.

    # >>> from imgur import ImgurDownloader
    # >>> ImgurDownloader('https://imgur.com/a/test', 'test-dir').__call__()

    """
    def __init__(self, imgur_url, filename):
        self.credentials = read_json('settings.json')
        self.imgur_url = imgur_url
        self.filename = filename
        self.path = os.path.abspath('../data/{}'.format(self.filename))
        self.checkpoint = 0

        self.client = self.authenticate()
        self.id, self.is_album = self.check_and_parse_url()
        self.check_directory()

    # used in __init__
    def authenticate(self):
        """This function authenticates into imgur api.

        Returns
        -------
        ImgurClient: imgurpython.client.ImgurClient
            The imgur connection instance.

        """
        return ImgurClient(**self.credentials)

    # used in __init__
    def check_and_parse_url(self):
        """This function checks if the given url is an album or a solo image.

        Returns
        -------
        spliced_url : str
            Solo image/Album id.

        True, False : bool
            True if is an album, False otherwise.

        """
        spliced_url = self.imgur_url.split('/')
        if spliced_url[3] == 'a':
            return spliced_url[-1], True
        return spliced_url[-1].split('.')[0], False

    # used in __init__
    def check_directory(self):
        """This function checks if on the given path the directory exists. If
        exists add it into the self.checkpoint the index of the most recent
        file - For not overwriting images. Otherwise, create the directory.

        Returns
        -------

        """
        if os.path.exists(self.path):
            try:
                self.checkpoint += len(os.listdir(self.path))
            except TypeError:
                self.checkpoint += 0
            except IndexError:
                self.checkpoint += 0
        else:
            os.makedirs(self.path)

    # used in download_image_list
    @staticmethod
    def requesting_images(url_):
        """Make GET submissions on the given url.

        Parameters
        ----------
        url_ : str
            Image url.

        Returns
        -------
        requests : bytes
            The website content.

        """
        return requests.get(url_).content

    # used in download_image_list
    def filename_format(self, idx, extension):
        """This function formats the filepath by adding its abspath and
        extension.

        Parameters
        ----------
        idx : int
            The image index - For not overwriting.
        extension : str
            Image extension.

        Returns
        -------
        formatted_filepath : str
            The formatted filepath.

        """
        return self.path + '/' + self.filename + '-{}.{}'. \
            format(idx + self.checkpoint, extension)

    # used in download_image_list
    @staticmethod
    def get_extension(img):
        """This function gets the image extension (jpg, png and others).

        Parameters
        ----------
        img : imgurpython.imgur.models.image.Image()
            The imgur image.

        Returns
        -------
        ext : str
            The image extension

        """
        return img.link.split('.')[-1]

    # used in __call__
    def get_image_list(self):
        """This function retrieves the list of images from imgur url.

        Returns
        -------
        img_list : iterator
            The images list.

        """
        if self.is_album:
            return self.client.get_album_images(self.id)
        return [self.client.get_image(self.id)]

    # used in __call__
    def download_image_list(self, image_list):
        """This function iterates through the image list.

        Parameters
        ----------
        image_list : iterator
            The images list.

        Returns
        -------

        """
        for idx, img in tqdm(
                enumerate(image_list, 1),
                total=len(image_list),
                desc=self.filename
        ):
            filename = self.filename_format(idx, self.get_extension(img))
            image_bytes = self.requesting_images(img.link)

            with io.open(filename, 'wb') as file:
                file.write(image_bytes)

    def __call__(self, *args, **kwargs):
        self.download_image_list(self.get_image_list())
