import pandas as pd
import ast 
from numpy import dot
from numpy.linalg import norm
from scipy import spatial

def get_dataframe():
    df = pd.read_csv("./utils/disha_movies.csv")
    df["genres"] = df["genres"].apply(ast.literal_eval)
    return df

def create_df_from_list_column(df, col_name):
    '''
    Takes a column of lists (col_name) from a dataframe (df)
    
    Returns a dataframe with number of columns equal to max list size 
    and each element of the row list in its own column  
    '''
    new_df = df[col_name].apply(pd.Series)
    new_df = new_df.rename(columns = lambda x : col_name + '_' + str(x))
    # print(new_df)
    return new_df

def convert_list_df_to_dummy_dataframe(list_df):
    '''
    The function gives consolidated dummy DataFrame.
    '''
    df_cols = list_df.columns.tolist()
    new_df = pd.DataFrame()
    for col in df_cols:
        if new_df.empty:
            new_df = pd.get_dummies(list_df[col])
            # print(new_df)
        else:
            new_df = pd.concat([new_df,pd.get_dummies(list_df[col])],axis=1)
    new_df = new_df.groupby(new_df.columns, axis=1).sum()
    return new_df

def get_final_input(user_choice):
    if user_choice.lower().strip() == "movie":
        return input("What movie do you want to check? \n").strip()
        # return "savING private RYAN"
    
    elif user_choice.lower().strip() == "director":
        # return  input("Who do you want to check?").strip()
        return "Lilly Wachowski"

    elif user_choice.lower().strip() == "comparison":
        # director1, director2 = input("Who do you want to compare? Add comma seprated values \n").split(",")
        # data = [director1.strip(),director2.strip()]
        data = ["Christopher Nolan","Lilly Wachowski"]
        return data
    else:
        return False

def get_cosine_similarity(list1,list2):
    # Using numpy
    return dot(list1, list2)/(norm(list1)*norm(list2))
    # Using scipy
    # return (1 - spatial.distance.cosine(list1, list2))
    
def get_result(df, final_input,user_choice):
    if user_choice.lower() == "movie":
        new_df = df.loc[df["title"].str.lower() == final_input.lower()]
        if new_df.empty:
            print('Invalid movie name "{0}". Please provide correct movie name'.format(final_input))
            return
        # print(new_df)
        result = new_df.to_dict(orient="records")[0]
        # print(result)
        print("The director(s) of the movie is {0}".format(result["director"]))
        print("The director(s) of the movie is {0}".format(new_df["director"].item()))
        # print("The genre of the movie is {0}".format(", ".join(result["genres"])))
        # print("The genre of the movie is {0}".format(", ".join(new_df["genres"].item())))
    
    elif user_choice.lower() == "director":
        # new_df = df.loc[df["director"].str.lower() == final_input.lower()]
        new_df = df[df['director'].str.lower().str.contains(final_input.lower())]
        print(new_df)
        if new_df.empty:
            print('Invalid director name "{0}". Please provide correct director name.'.format(final_input))
            return
        movie_list = new_df["title"]
        if len(movie_list) > 4:
            movie_list = ", ".join(movie_list[:4]) + "... etc"
        else:
            movie_list = ", ".join(movie_list)
        print('{0} has directed {1}'.format(final_input,movie_list))
        
        print(new_df["genres"].value_counts())
        
        new_df = create_df_from_list_column(new_df,"genres")
        new_df = convert_list_df_to_dummy_dataframe(new_df)
        # Count all genres occurrences for the given director 
        all_genres = new_df.columns
        genre_info = ""
        for genre in all_genres[:-1]:
            genre_info += genre + ": " + str(new_df[genre].sum()) + ", "
        genre_info += all_genres[-1] + ": " + str(new_df[all_genres[-1]].sum())+"."
        print('His/ Her most directed genres are {0}'.format(genre_info))
        
    else:
        genre_dict = {}
        for director in final_input:
            new_df = df[df['director'].str.lower().str.contains(director.lower())]
            if new_df.empty:
                print('Invalid director name "{0}". Please provide correct movie name'.format(director))
                return
            movie_list = new_df["title"]
            if len(movie_list) > 4:
                movie_list = ", ".join(movie_list[:4]) + "... etc"
            else:
                movie_list = ", ".join(movie_list)
                
            print('{0} has directed {1}'.format(director,movie_list))
            new_df = create_df_from_list_column(new_df,"genres")
            new_df = convert_list_df_to_dummy_dataframe(new_df)
            # Count all genres occurrences for the given director 
            all_genres = list(new_df.columns)
            genre_dict[director] = {
                "all_genres": all_genres,
                "genre_occ":{}
            }
            genre_info = ""
            for genre in all_genres:
                genre_info += genre + ": " + str(new_df[genre].sum()) + ", "
                genre_dict[director]["genre_occ"][genre] = new_df[genre].sum()
            genre_info = genre_info.rstrip(", ")
            print('His/ Her most directed genres are {0}.'.format(genre_info)) 
            print("-"*20)
        # print(genre_dict)
        comman_vector = list(set(genre_dict[final_input[0]]["all_genres"] + genre_dict[final_input[1]]["all_genres"]))
        director1_vector = [genre_dict[final_input[0]]["genre_occ"].get(x,0) for x in comman_vector]
        director2_vector = [genre_dict[final_input[1]]["genre_occ"].get(x,0) for x in comman_vector]
        print("Comman Vector: {0}".format(comman_vector))
        print("{0} Vector: {1}".format(final_input[0], director1_vector))
        print("{0} Vector: {1}".format(final_input[1], director2_vector))
        cosine_similarity = get_cosine_similarity(director1_vector,director2_vector)
        print("-"*20)
        print("Based on that, they have a cosine similarity score of {:.3f}.".format(cosine_similarity))
        
def main():
    df = get_dataframe()
    user_choice = "comparison"
    # user_choice = input('What do you want to check on IMDB? (Please choose "movie", "director", or "comparison") \n')
    final_input = get_final_input(user_choice)
    if not final_input:
        print('"{0}" is invalid option, please choose valid option. Available options are "movie", "director", or "comparison"'.format(user_choice))
        return
    get_result(df, final_input,user_choice)

if __name__ == "__main__":
    main()