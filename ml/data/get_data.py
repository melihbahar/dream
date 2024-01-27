import pandas as pd


def get_data():
    url = 'https://drive.google.com/file/d/1kqnB4J8FuF1k8xLIvfbPE1jsqUwd3wVH/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]
    return pd.read_csv(path).set_index('Id')
