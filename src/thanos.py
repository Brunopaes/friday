# -*- coding: utf-8 -*-
from PIL import ImageTk

import helpers
import tkinter
import random
import pandas
import PIL
import os


class CreatingDB:
    def __init__(self):
        self.directory = r'C:\Users\Bruno\iCloudDrive\Documents\Playboy'
        self.model_dict = {
            'MODEL_ID': [],
            'MODEL_NAME': [],
            'MODEL_ALBUM': []
        }

    @staticmethod
    def getting_hash(model_name):
        random.seed(model_name)
        return random.randint(1, 1000000)

    def filling_file(self):
        for i in os.listdir(
                r'{}\\Playboy Photos'.format(self.directory)):
            if len(i.split('-and-')) > 1:
                for j in i.split('-and-'):
                    random.seed(j)
                    self.model_dict.get('MODEL_ID').append(
                        self.getting_hash(j)
                    )
                    self.model_dict.get('MODEL_NAME').append(j)
                    self.model_dict.get('MODEL_ALBUM').append(i)
            else:
                self.model_dict.get('MODEL_ID').append(
                    self.getting_hash(i)
                )
                self.model_dict.get('MODEL_NAME').append(i)
                self.model_dict.get('MODEL_ALBUM').append(i)

    def writing_file(self):
        df = pandas.DataFrame(self.model_dict)
        df['MODEL_ELO'] = 1000
        df['ALBUM_ELO'] = 1000

        df.to_csv(
            r'{}\\playboyonreddit-elo.csv'.format(self.directory),
            index=False
        )

    def __call__(self, *args, **kwargs):
        self.filling_file()
        self.writing_file()


class PictureFormatter:
    def __init__(self):
        self.directory = r'C:\Users\Bruno\iCloudDrive\Documents\Playboy'
        self.competitors = self.choosing_opponents()
        self.pictures_paths = self.choosing_pictures()
        self.pil_objects = []

    def choosing_opponents(self):
        competitors_list = list(set(
            pandas.read_csv(r'{}\\playboyonreddit-elo.csv'.format(
                    self.directory
                )
            ).MODEL_ALBUM.to_list()))

        competitor_a, competitor_b = (
            random.choice(competitors_list),
            random.choice(competitors_list)
        )

        while competitor_a == competitor_b:
            competitor_b = random.choice(competitors_list)

        return competitor_a, competitor_b

    def choosing_pictures(self):
        for competitor in self.competitors:
            yield random.choice(os.listdir(
                r'{}\\Playboy Photos\{}'.format(
                    self.directory,
                    competitor
                )
            ))

    def opening_pictures(self):
        for picture, competitor in zip(self.pictures_paths, self.competitors):
            yield PIL.Image.open(r'{}\Playboy Photos\{}\{}'.format(
                self.directory,
                competitor,
                picture
            ))

    def merging_pictures(self, pictures):
        for picture in pictures:
            self.pil_objects.append(picture)

        min_dimension = (700, 800)

        picture_a = self.pil_objects[0].resize(min_dimension)
        picture_b = self.pil_objects[1].resize(min_dimension)

        merged_picture = PIL.Image.new(
            'RGB',
            (2 * picture_a.size[0], picture_a.size[0]),
            (250, 250, 255)
        )

        merged_picture.paste(picture_a, (0, 0))
        merged_picture.paste(picture_b, (picture_a.size[0], 0))

        return merged_picture

    def __call__(self, *args, **kwargs):
        return (
            self.merging_pictures(self.opening_pictures()),
            (
                self.pil_objects[0].filename.split('\\')[-1],
                self.pil_objects[1].filename.split('\\')[-1]
            ),
            self.competitors
        )


class FrontEnd:
    def __init__(self, picture, filenames, competitors):
        self.directory = r'C:\Users\Bruno\iCloudDrive\Documents\Playboy'
        self.picture = picture,
        self.filename_a, self.filename_b = filenames
        self.competitor_a, self.competitor_b = competitors
        self.competitor_name_a, self.competitor_name_b = \
            self.formatting_names(competitors)

        self.root = tkinter.Tk()
        self.root.geometry("1920x1080")

    @staticmethod
    def formatting_names(competitors):
        for competitor in competitors:
            yield ' '.join(
                [i.capitalize() for i in competitor.split('-')]
            )

    def building_application(self):
        frame = tkinter.Frame(self.root, width=600, height=400)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.45)

        img = ImageTk.PhotoImage(self.picture[0])

        label = tkinter.Label(
            frame,
            image=img
        )
        label.pack()

        button = tkinter.Button(
            self.root, text=self.competitor_name_a,
            command=lambda: self.get_winner(
                self.competitor_a,
                self.competitor_b
            )
        )
        button.place(width=690, x=260, y=820)

        button_2 = tkinter.Button(
            self.root, text=self.competitor_name_b,
            command=lambda: self.get_winner(
                self.competitor_b,
                self.competitor_a
            )
        )
        button_2.place(width=690, x=970, y=820)

        self.root.state('zoomed')
        self.root.mainloop()

    def get_winner(self, winner, loser):
        df = pandas.read_csv(r'{}\\playboyonreddit-elo.csv'.format(self.directory))

        df_winner = df[df['MODEL_ALBUM'] == winner]
        df_loser = df[df['MODEL_ALBUM'] == loser]

        competitors = (df_winner.MODEL_ALBUM.values[0], df_loser.MODEL_ALBUM.values[0])
        ratings = (df_winner.ALBUM_ELO.values[0], df_loser.ALBUM_ELO.values[0])

        res = helpers.EloCalculator(winner, ratings, competitors).__call__()

        df.loc[
            df['MODEL_ALBUM'] == competitors[0], 'ALBUM_ELO'
        ] = res.get(competitors[0])

        df.loc[
            df['MODEL_ALBUM'] == competitors[1], 'ALBUM_ELO'
        ] = res.get(competitors[1])

        df.to_csv(
            r'{}\\playboyonreddit-elo.csv'.format(self.directory),
            index=False
        )

        self.root.destroy()

    def __call__(self, *args, **kwargs):
        self.building_application()


if __name__ == '__main__':
    while True:
        FrontEnd(*PictureFormatter().__call__()).__call__()
    # helpers.EloCalculator('a', (1200, 1000), ('a', 'b')).__call__()
