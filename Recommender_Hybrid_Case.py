#############################################################
# RECOMMENDATION PROJECT
# Business Problem

############################################################

############################################################
# DUTY 1 : Prepare Data
# Stage 1: Read  movie, rating Datasets.
# Stage 2: Merge rating and movie datasets on movieId values.
# Stage 3: Create a list for movies whose vote number < 1000 as rare_movies
# Stage 4: Create a pivot table with rows includes userID , columns includes Movie titles and rating for value parameters.
# Stage 5: Create a function for all stages.
############################################################

import pandas as pd
import numpy as np
from Src.utils import check_df
from Src.utils import grab_col_names

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

movie = pd.read_csv('Datasets/movie.csv')
rating = pd.read_csv('Datasets/rating.csv')
check_df(movie)
check_df(rating)
df = movie.merge(rating, how="left", on="movieId")
df.head()
"""create a dataframe for movie rating_counts"""
comment_counts = pd.DataFrame(df["title"].value_counts())
comment_counts.reset_index(inplace=True)
comment_counts.columns = ["title","count"]
comment_counts.shape ### 27262 movie
""" Create a list rare_movies for movies have ratings <= 1000"""
rare_movies = comment_counts[comment_counts["count"] <= 1000]
rare_movies.shape ### 24103 movie has less then 1000 ratings
""" Create a list common_movies that has ratings > 1000 """
common_movies = comment_counts[comment_counts["count"] > 1000]
common_movies.shape ### 3159 movie in common group

df[df["title"].isin(common_movies["title"].values)].shape
### i will analyse this data, common movie_ratings
# shape : total ratings for common movies (17766015, 6)

user_movie_df = df[df["title"].isin(common_movies["title"].values)].\
                pivot_table(index=["userId"], columns=["title"], values="rating")
# i want to test
user_movie_df.iloc[0:10,0:20]

############################################################################################
def prepare_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie.csv')
    rating = pd.read_csv('datasets/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    """create a dataframe for movie rating_counts"""
    comment_counts = pd.DataFrame(df["title"].value_counts())
    comment_counts.reset_index(inplace=True)
    comment_counts.columns = ["title", "count"]
    """ Create a list rare_movies for movies have ratings <= 1000"""
    rare_movies = comment_counts[comment_counts["count"] <= 1000]
    """ Create a list common_movies that has ratings > 1000 """
    common_movies = comment_counts[comment_counts["count"] > 1000]
    user_movie_df = df[df["title"].isin(common_movies["title"].values)]. \
        pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df
#####################################
a = prepare_user_movie_df()
# for test
a.iloc[0:5,0:10]


#################################################################################3
# DUTY 2 :
# Stage 1:Choose a random user
# Stage 2: Create a random_user_df dataframe for movies watched by random user.
# Stage 3: Create a list movies_watched for the movies and gave ratings by random user.
###############################################################################
random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values)
random_user ### random_user = 28941
random_user_df = user_movie_df[user_movie_df.index == random_user]
### random user watched following movies
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
### random users watched following 33 movies and his ratings
user_movie_df.loc[user_movie_df.index == random_user, movies_watched].T

###################################################################################
# DUTY 3 :
# Stage 1 : create a new dataframe movies_watched_df for the data
# Stage 2:  Her birkullancınınseçiliuser'inizlediğifilmlerinkaçınıizlediğinibilgisinitaşıyanuser_movie_countadındayeni birdataframeoluşturu
# Stage 3:  Seçilenkullanıcınınoy verdiğifilmlerinyüzde60 veüstünüizleyenlerinkullanıcıid’lerindenusers_same_moviesadındabirlisteoluşturunuz
###################################################################################
## All ratings in the user_movie_df about watched movies by random user.
movies_watched_df = user_movie_df[movies_watched]

user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]

##user_movie_count[user_movie_count["movie_count"] > len(movies_watched) * 0.6].sort_values("movie_count", ascending=False) 4139 users
## i choose 20 for len(movies_watched) * 0.6
perc=20
user_movie_count[user_movie_count["movie_count"] > perc].sort_values("movie_count", ascending=False) # 3202 users
user_movie_count[user_movie_count["movie_count"] == 33].count() ## 17 users

### same movies watched by following users 3202 users
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

##################################################################
# DUTY 4:
# Stage 1: user_same_movieslistesiiçerisindekiseçili userile benzerlik gösteren kullanıcıların id’lerininbulunacağı şekilde movies_watched_dfdataframe’inifiltreleyiniz.
# Stage 2: Kullanıcılarınbirbirleriileolankorelasyonlarınınbulunacağıyeni bircorr_dfdataframe’ioluşturunuz.
# Stage 3: Seçilikullanıcıileyüksekkorelasyonasahip(0.65’in üzerindeolan) kullanıcılarıfiltreleyerektop_usersadındayeni birdataframeoluşturunuz
# Stage 4 : top_usersdataframe’ineratingverisetiilemerge ediniz
#################################################################

final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                     movies_watched_df[movies_watched_df.index == random_user]])
## creation corelation dataframe
corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()
corr_df.head()

top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][["user_id_2", "corr"]].reset_index(drop=True)
top_users = top_users.sort_values(by='corr', ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]

#################################################################
# DUTY 5 :
# Stage 1:   Her bir kullanıcının corrve ratingdeğerlerinin çarpımından oluşan weighted_ratingadındayeni birdeğişkenoluşturunuz.
# Stage 2:  Film id’sive her bir filme ait tüm kullanıcılarınweighted rating’lerininortalamadeğeriniiçerenrecommendation_dfadındayeni birdataframeoluşturunuz.
# Stage 3:  recommendation_dfiçerisindeweighted rating'i3.5'ten büyükolanfilmleriseçinizveweighted rating’egöresıralayınız.
# Stage 4:  movie verisetindenfilm isimlerinigetirinizvetavsiyeedilecekilk 5 filmi seçiniz
##################################################################
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()

movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)

recommended_movies = movies_to_be_recommend.merge(movie[["movieId", "title"]]).head(5)

## i check film genres value all of them contains Drama
movie[movie["movieId"].isin(recommended_movies["movieId"].values) ]
movie[movie["title"].isin(movies_watched) ]


###################################################################
# ITEM BASED RECOMMENDATION
# DUTY 1
# Stage 1:   movie, rating verisetlerini okutunuz.
# Stage 2:  Seçilikullanıcının5 puanverdiğifilmlerdenpuanıengüncelolanfilminid'sininalınız.
# Stage 3:  User based recommendation bölümündeoluşturulanuser_movie_dfdataframe’iniseçilenfilm id’sinegörefiltreleyiniz.
# Stage 4:  Filtrelenen dataframe’ikullanarak seçili filmle diğer filmlerin korelasyonunu bulunuz ve sıralayınız.
# Stage 5:  Seçilifilm’inkendisiharicindeilk 5 film’Iöneriolarakveriniz
###################################################################

movie = pd.read_csv('datasets/movie.csv')
rating = pd.read_csv('datasets/rating.csv')

user_movie_df = prepare_user_movie_df()
random_user = 28941

rating.loc[(rating["userId"] == random_user) & (rating["rating"] == 5)].sort_values("timestamp",ascending=False) ### movie_id = 7
xMovie_Id = 7
xMovie_title = movie[movie["movieId"] == xMovie_Id] ### Sabrina (1995)

xmovie_ratings = user_movie_df['Sabrina (1995)']
cor_list = user_movie_df.corrwith(xmovie_ratings).sort_values(ascending=False).head(6).index

## for test
user_movie_df[(user_movie_df[cor_list].fillna(0) > 0)][cor_list]
