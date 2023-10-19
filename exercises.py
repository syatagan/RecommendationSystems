import pandas as pd
import numpy as np
from Src.utils import check_df
from Src.utils import grab_col_names

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

movie = pd.read_csv('Datasets/movie.csv')
xmovie_df = movie.copy()

genres_list = movie["genres"].unique()
target_set = set()
for xgen in genres_list:
    split_list = xgen.split("|")
    for xstr in split_list:
        target_set.add(xstr)

len(target_set)
for xcategory in target_set:
    xmovie_df[xcategory] = xmovie_df.apply(lambda x: 1 if xcategory in x["genres"] else 0,axis=1)

xmovie_df.head()