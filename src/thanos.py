import random
import pandas
import os


if __name__ == '__main__':
    directory = r'C:\Users\Bruno\iCloudDrive\Documents' \
                r'\Playboy\Playboy Photos'

    model_dict = {
        'MODEL_ID': [],
        'MODEL_NAME': [],
        'MODEL_ALBUM': []
    }
    for i in os.listdir(directory):
        if len(i.split('-and-')) > 1:
            for j in i.split('-and-'):
                random.seed(j)
                model_dict.get('MODEL_ID').append(
                    random.randint(1, 100000)
                )
                model_dict.get('MODEL_NAME').append(j)
                model_dict.get('MODEL_ALBUM').append(i)
        else:
            random.seed(i)
            model_dict.get('MODEL_ID').append(random.randint(1, 100000))
            model_dict.get('MODEL_NAME').append(i)
            model_dict.get('MODEL_ALBUM').append(i)

    df = pandas.DataFrame(model_dict)
