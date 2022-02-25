from PIL import Image

import helpers
import io
import os

client = helpers.start_connection()
query = """
    INSERT INTO
        `mooncake-304003.misc.elo-playboy`
    VALUES
        ("{}", "{}")
"""


def binarize(filepath):
    return open(filepath, "rb")


def de_binarize(bytes_):
    return Image.open(io.BytesIO(bytes_))


if __name__ == '__main__':
    directory = r'C:\Users\Bruno\iCloudDrive\Documents' \
                r'\Playboy\Playboy Photos\alejandra-guilmant'

    dict_ = {}
    for file in os.listdir(directory):
        dict_[file] = binarize(r'{}\{}'.format(directory, file))

    client.query(query=query.format('alejandra-guilmant', dict_.get('alejandra-guilmant-1.jpg')))
