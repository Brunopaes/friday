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
            'ALBUM': [],
            'PICTURE': []
        }

    @staticmethod
    def getting_hash(model_name):
        random.seed(model_name)
        return random.randint(1, 1000000)

    def filling_file(self):
        for model_dir in os.listdir(r'{}\\Playboy Photos'.format(
                self.directory
        )):
            for photo in os.listdir(r'{}\\Playboy Photos\\{}'.format(
                    self.directory, model_dir
            )):
                if len(model_dir.split('-and-')) > 1:
                    for model in model_dir.split('-and-'):
                        self.model_dict.get('MODEL_ID').append(
                            self.getting_hash(model)
                        )
                        self.model_dict.get('MODEL_NAME').append(
                            ' '.join([
                                i.capitalize() for i in model.split('-')
                            ])
                        )
                        self.model_dict.get('ALBUM').append(
                            '-'.join(photo.split('-')[:-1])
                        )
                        self.model_dict.get('PICTURE').append(
                            photo
                        )
                else:
                    self.model_dict.get('MODEL_NAME').append(
                        ' '.join([
                            i.capitalize() for i in model_dir.split('-')
                        ])
                    )
                    self.model_dict.get('MODEL_ID').append(
                        self.getting_hash(model_dir)
                    )
                    self.model_dict.get('ALBUM').append(
                        '-'.join(photo.split('-')[:-1])
                    )
                    self.model_dict.get('PICTURE').append(
                        photo
                    )

    def writing_file(self):
        df = pandas.DataFrame(self.model_dict)
        df['ELO_RATING'] = 1000

        df.sort_values(['MODEL_NAME', 'PICTURE'], inplace=True)

        df.to_csv(
            r'{}\\playboyonreddit-elo.csv'.format(self.directory),
            index=False,
            encoding='latin-1'
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
            ), encoding='latin-1').ALBUM.to_list()))

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
                r'{}\Playboy Photos\{}'.format(
                    self.directory,
                    competitor
                )
            ))

    def opening_pictures(self):
        for picture, competitor in zip(
                self.pictures_paths,
                self.competitors
        ):
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
            (
                self.pil_objects[0].filename.split('\\')[-1],
                self.pil_objects[1].filename.split('\\')[-1]
            )
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
            yield ' '.join(' '.join(
                [i.capitalize() for i in competitor.split('-')]
            ).split(' ')[:-1])

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
        button.place(width=690, height=80, x=260, y=820)

        button_2 = tkinter.Button(
            self.root, text=self.competitor_name_b,
            command=lambda: self.get_winner(
                self.competitor_b,
                self.competitor_a
            )
        )
        button_2.place(width=690, height=80, x=970, y=820)

        self.root.state('zoomed')
        self.root.mainloop()

    def get_winner(self, winner, loser):
        df = pandas.read_csv(
            r'{}\\playboyonreddit-elo.csv'.format(self.directory),
            encoding='latin-1'
        )

        df_winner = df[df['PICTURE'] == winner]
        df_loser = df[df['PICTURE'] == loser]

        competitors = (
            df_winner.PICTURE.values[0],
            df_loser.PICTURE.values[0]
        )
        ratings = (
            df_winner.ELO_RATING.values[0],
            df_loser.ELO_RATING.values[0]
        )

        res = helpers.EloCalculator(
            winner, ratings, competitors
        ).__call__()

        df.loc[
            df['PICTURE'] == competitors[0], 'ELO_RATING'
        ] = res.get(competitors[0])

        df.loc[
            df['PICTURE'] == competitors[1], 'ELO_RATING'
        ] = res.get(competitors[1])

        df.to_csv(
            r'{}\\playboyonreddit-elo.csv'.format(self.directory),
            index=False,
            encoding='latin-1'
        )

        self.root.destroy()

    def __call__(self, *args, **kwargs):
        self.building_application()


if __name__ == '__main__':
    while True:
        FrontEnd(*PictureFormatter().__call__()).__call__()
