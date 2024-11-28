import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
# from sklearn.metrics.pairwise import cosine_similarity
# import seaborn as sns

print("***************************** Movie Recommender System ******************************************")
print()
print()
print(" Press 1 - To see the data visualization of the data set")
print(" Press 2 - To Directly find a new movie recommendation ")
print()
print()
print("***************************************************************************************************")
print()
mode = int(input("Enter Your choice here : "))


def find_similar_movies(name_of_the_movie):
    User_movie_rating = movie_matrix[name_of_the_movie]
    list_name = movie_matrix.columns.values
    if(mode == 1):
        print("***************************** ", name_of_the_movie,
              " rating Data ******************************************")
        print(User_movie_rating.head())
        print("******************************************************************************************", "\n")
    # similar = movie_matrix.corrwith(User_movie_rating)

    # similar = movie_matrix.corr()
    # similar = similar[name_of_the_movie]
    lis = []
    final_dict = dict()

    for x in range(len(movie_matrix.columns)):
        corr_value = movie_matrix[movie_matrix.columns[x]].corr(
            User_movie_rating)
        movie_name = list_name[x]
        if (isinstance(corr_value, np.float64) and np.isnan(corr_value) == False):
            final_dict[movie_name] = corr_value
    #         print("Float-> ",temp)
    #         lis.append(corr_value)
        else:
            pass

    recommendation = list()
    for key, value in sorted(iter(final_dict.items()), key=lambda k_v: (k_v[1], k_v[0])):
        # recommendation.append(str(key)+" ---> "+str(value))
        recommendation.append(str(key))
        # print("%s: %s" % (key, value))

    print("**************************************** Movie Recommendations ***************************************************", '\n')
    # print(final_dict)
    recommendation.reverse()
    for i in range(6):
        print(recommendation[i], '\n')
    print("******************************************************************************************************************", '\n')


def cos_sim(a, b, keys):
    dot_product = 0.0
    a_sum = 0
    b_sum = 0
    # print(keys)
    # print(a,'\n\n',b)
    for i in keys:
        dot_product = dot_product + (a[i] * b[i])
        a_sum = a_sum + math.pow(a[i], 2)
        b_sum = b_sum + math.pow(b[i], 2)
    a_sum = math.sqrt(a_sum)
    b_sum = math.sqrt(b_sum)
    if((a_sum*b_sum) == 0):
        print(keys)
    return dot_product / (a_sum * b_sum)


def find_similar_movies_cosine_sim(name_of_the_movie):
    User_movie_rating = movie_matrix[name_of_the_movie]
    list_name = movie_matrix.columns.values
    lis_1 = []
    final_dict_1 = dict()
    dic = dict()

    # print("Length-->>>",len(list_name))
    for x in range(len(list_name)):
        # print(x,"-->",len(list_name))
        b = movie_matrix[movie_matrix.columns[x]].values
        a = movie_matrix[name_of_the_movie]
        # print(a[])
        for i in range(1, 500):  # limiting user Rating to 500 users

            # print("Temp ->>>",a[i])
            if (isinstance(a[i], np.float64) and np.isnan(a[i]) == False):
                dic[i] = a[i]
        dic_1 = dict()
        new_list_a_name = dic.keys()

        for i in range(500):  # limiting user Rating to 500 users
            if (isinstance(b[i], np.float64) and np.isnan(b[i]) == False):
                dic_1[i] = b[i]
        new_list_b_name = dic_1.keys()

        new_list = list(set(new_list_a_name).intersection(new_list_b_name))
        # print("new_list_a_name -> ",len(new_list_a_name),'\n')
        # print("new_list_b_name -> ",len(new_list_b_name),'\n')
        # print("new_list",len(new_list))

        # ------------------------------------------------------------------------
        #print("a dict -> ",a,"\n\n")
        # print("b dict -> ",b,"\n\n").
        # print(new_list)
        # print(len(new_list))
        # print("********************************************************************")
        # -----------------------------------------------------------------------------

        if(new_list):
            similarity = cos_sim(dic, dic_1, new_list)
            final_dict_1[list_name[x]] = similarity
        print(x, "-->", len(list_name))

    recommendation_1 = list()
    for key, value in sorted(iter(final_dict_1.items()), key=lambda k_v: (k_v[1], k_v[0])):
        # recommendation.append(str(key)+" ---> "+str(value))
        recommendation_1.append(str(key))
        # print("%s: %s" % (key, value))

    print("**************************************** Movie Recommendation ***************************************************", '\n')
    # print(final_dict)
    recommendation_1.reverse()
    for i in range(6):
        print(recommendation_1[i], '\n')
    print("******************************************************************************************************************", '\n')


column_names = ['user_id', 'item_id', 'rating', 'timestamp']

# reading ratings data set
df = pd.read_csv('ratings.csv', sep='\t', names=column_names)

if(mode == 1):
    print("***************************** User Rating Sample Data count ***************************************", "\n")
    print(df.count(), "\n")
    print("***************************************************************************************************", "\n")
    print("***************************** User Rating Sample Data ***************************************", "\n")
    print(df.head(), "\n")
    print("********************************************************************************************************", "\n")

# reading movies data set
movie_titles = pd.read_csv('movies')

if(mode == 1):
    print("***************************** Movie list Sample Data *************************************************", "\n")
    print(movie_titles.head(), "\n")
    print("******************************************************************************************************", "\n")

# merging the movie dataset with ratings data set
df = pd.merge(df, movie_titles, on='item_id')

if(mode == 1):
    print("***************************** Movie list with user ratings  *************************************************", "\n")
    # print(df.head(),"\n")
    print(df.groupby('title')['rating'].mean(
    ).sort_values(ascending=False).head(10))
    print("**************************************************************************************************************", "\n")


ratings = pd.DataFrame(df.groupby('title')['rating'].mean())

if(mode == 1):
    print("***************************** Movie Rating mean values *************************************************", "\n")
    print(ratings.head(), "\n")
    print("********************************************************************************************************", "\n")

ratings['rating_numbers'] = pd.DataFrame(df.groupby('title')['rating'].count())
if(mode == 1):
    print("***************************** Movie Rating mean values and counts *******************************************", "\n")
    print(ratings.head(), "\n")
    print("**************************************************************************************************************", "\n")

# Visualization Graphs


def show_histogram_num_of_ratings():
    plt.hist(ratings['rating_numbers'], bins=70)

    plt.title("Number of ratings histogram")
    plt.show()


def show_histogram_avg_rating_per_movie():
    plt.hist(ratings['rating'], bins=70)
    plt.title("Average rating per movie histogram")
    plt.show()


def show_joinplot_ratings_numratings():
    sns.jointplot(x='rating', y='num of ratings', data=ratings, alpha=0.5)
    plt.show()


if(mode == 1):
    # show_histogram_num_of_ratings()
    # show_histogram_avg_rating_per_movie()
    # show_joinplot_ratings_numratings()
    ratings['num of ratings'] = pd.DataFrame(
        df.groupby('title')['rating'].count())
    ratings.head()

    plt.figure(figsize=(10, 4))
    plt.xlabel('number of ratings')
    plt.ylabel('Frequency')
    ratings['num of ratings'].hist(bins=70)

    plt.show()

    plt.figure(figsize=(10, 4))
    plt.xlabel('ratings')
    plt.ylabel('users')
    ratings['rating'].hist(bins=70)
    plt.show()

    sns.jointplot(x='rating', y='num of ratings', data=ratings, alpha=0.5)
    plt.show()


movie_matrix = df.pivot_table(
    index='user_id', columns='title', values='rating')
if(mode == 1):
    print("***************************** Movies with each user rating data  ***************************************", "\n")
    print(movie_matrix.head())
    print("********************************************************************************************************", "\n")
    print("***************************** Movie Rating with highest rating count ***********************************", "\n")
    print(ratings.sort_values('rating_numbers', ascending=False).head(10))
    print("********************************************************************************************************", "\n")
print("------------------------------------------------------------------------------------------")

name = input("Enter a Movie :")
find_similar_movies(name)
