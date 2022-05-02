from numpy import integer
import tomatopy as rtp
import pandas as pd
import streamlit as st
import numpy as np
from typing import List
import nltk 
from rotten_tomatoes_scraper.rt_scraper import MovieScraper
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from review_scraper import *
from segtok.segmenter import split_single
import re

from flair.models import TextClassifier
from flair.data import Sentence

classifier = TextClassifier.load('en-sentiment')

def make_sentences(text):
    sentences = [sent for sent in split_single(text)]
    return sentences

def predict(sentence):
    if sentence == "":
        return 0
    text = Sentence(sentence)
    classifier.predict(text)
    value = text.labels[0].to_dict()['value'] 
    if value == 'POSITIVE':
        print(text.to_dict())
        print(text.to_dict())
        result = text.to_dict()['all labels'][0]['confidence']
    else:
        print(text.to_dict())
        print(text.to_dict())
        result = -(text.to_dict()['all labels'][0]['confidence'])
    return round(result, 3)

def get_scores(sentences):
    results = []
    
    for i in range(0, len(sentences)): 
        results.append(predict(sentences[i]))
    return results

def get_sum(scores):
    
    result = round(sum(scores), 3)
    return result


def get_movie():
    #movies_list = rtp.scrape_movie_names(2008) # get top movies from 2008
    #movies_list = list(dict.fromkeys(movies_list)) # remove duplicates
    #movies_df = pd.DataFrame(movies_list)
    movies_df = pd.read_csv("movies.csv")
    movies_df.columns = ["id", "movie"]
    movies_list = movies_df["movie"].values.tolist()

    # Build Site
    st.title("Rotton Tom")
    #st.dataframe(movies_df)

    option = st.selectbox('Select a Movie', movies_list)

    header = option + " Info"
    option = option.lower()
    movie_scraper = MovieScraper(movie_title=option)
    movie_scraper.extract_metadata()

    #print(type(main_info))
    
    st.header(header)

    # for key, value in movie_scraper.metadata.items():
    #     st.write(key, ": ",value)

    col1, col2 = st.columns(2)
    col1.metric("Critic Score", movie_scraper.metadata.get("Score_Rotten"))
    col2.metric("Audience Score", movie_scraper.metadata.get("Score_Audience"))

    return option


def reviews(option):
    st.header("Reviews")

    run(option)

    header_list = ["NA", "freshness", "source", "review", "date"]
    df = pd.read_csv("reviews.csv", names=header_list)
    st.dataframe(df)
    df = df["review"].dropna()

    # st.dataframe(df)
    SIA = SentimentIntensityAnalyzer()

    Pos = []
    Neu = []
    Neg = []

    for r in df:
        # st.write(r)
        Pos.append(SIA.polarity_scores(r).get("pos"))
        Neu.append(SIA.polarity_scores(r).get("neu"))
        Neg.append(SIA.polarity_scores(r).get("neg"))

    pos_score = sum(Pos) / len(Pos)
    neu_score = sum(Neu) / len(Neu)
    neg_score = sum(Neg) / len(Neg)

    print("Positive Score: ", pos_score)
    print("Neutral Score: ", neu_score)
    print("Negative Score: ", neg_score)

    #st.write("Pos + Neg Polarity Score: ", (pos_score + neu_score) * 100)
    #st.write("Neg / Pos Score: ", 100 - (neg_score / pos_score) * 100)
    #st.write("Pos / (Neg + Pos) Score: ",  (pos_score / (neg_score + pos_score)) * 100)

    st.dataframe(df)

    df["sentences"] = df.apply(make_sentences)
    df["scores"] = df["sentences"].apply(get_scores)
    df['scores_sum'] = df["scores"].apply(get_sum)
    #st.dataframe(df)

    sum_flair = df['scores_sum'].sum()
    size_flair = df['scores_sum'].size
    avg_flair = sum_flair / size_flair * 100

    col1, col2 = st.columns(2)
    #col1.metric("Pos + Neg Polarity Score", int((pos_score + neu_score) * 100))
    #col2.metric("Neg / Pos Score", int(100 - (neg_score / pos_score) * 100))
    col1.metric("VADER Sentiment Score", int((pos_score / (neg_score + pos_score)) * 100))
    col2.metric("Flair Sentiment Score", int(avg_flair))

    if option == "anaconda":
        st.balloons()

def trend_finder():
    st.title("Trend Finder")
    data_set_option = st.selectbox('Select a Dataset', range(2000, 2021))

    movies_list = rtp.scrape_movie_names(data_set_option) # get top movies from 1950
    movies_list = list(dict.fromkeys(movies_list)) # remove duplicates
    movies_list = movies_list[1:5]
    movies_df = pd.DataFrame(movies_list, columns =['Name'])
    #movies_df.columns = ["Movie", "Critic Score", "Audience Score", "Sentiment Score"]
    st.dataframe(movies_df)

    #movie_scores_df = pd.DataFrame
    #movies_scores_df.columns = ["Critic Score", "Audience Score", "Sentiment Score"]

    sentiment_score:List[integer] = []
    audience_score:List[integer] = []
    rotten_score:List[integer] = []

    a_r_difference = []
    s_r_difference = []
    s_a_difference = []

    if st.button('Analyze!'):
        for movie in movies_list:
            print("Analysing ", movie)
            run(movie)
            try:

                option_2 = movie.lower()
                movie_scraper = MovieScraper(movie_title=option_2)
                movie_scraper.extract_metadata()


                df = pd.read_csv("reviews.csv")
                df.columns = ["NA", "freshness", "source", "review", "date"]
                df = df["review"].dropna()

                SIA = SentimentIntensityAnalyzer()


                Pos = []
                Neu = []
                Neg = []

                for r in df:
                    # st.write(r)
                    Pos.append(SIA.polarity_scores(r).get("pos"))
                    Neu.append(SIA.polarity_scores(r).get("neu"))
                    Neg.append(SIA.polarity_scores(r).get("neg"))

                pos_score = sum(Pos) / len(Pos)
                neu_score = sum(Neu) / len(Neu)
                neg_score = sum(Neg) / len(Neg)

                print("Positive Score: ", pos_score)
                print("Neutral Score: ", neu_score)
                print("Negative Score: ", neg_score)

                score = int((pos_score / (neg_score + pos_score)) * 100)

                a_score = int(movie_scraper.metadata.get("Score_Audience"))
                r_score = int(movie_scraper.metadata.get("Score_Rotten"))
                s_score = score

                audience_score.append(a_score)
                rotten_score.append(r_score)
                sentiment_score.append(s_score)

                a_r_difference.append(abs(a_score - r_score))
                s_r_difference.append(abs(s_score - r_score))
                s_a_difference.append(abs(s_score - a_score))

            except:
                print("Movie Failed...")
                sentiment_score.append(0)
                audience_score.append(0)
                rotten_score.append(0)

                a_r_difference.append(0)
                s_r_difference.append(0)
                s_a_difference.append(0)

        print("SENTIMENT_SCORE: ", sentiment_score)
        print("AUDIENCE_SCORE: ", audience_score)
        print("ROTTEN_SCORE: ", rotten_score)

        movies_df['Sentiment Score'] = sentiment_score
        movies_df['Audience Score'] = audience_score
        movies_df['Rotten Score'] = rotten_score

        movies_df['a_r_difference'] = a_r_difference
        movies_df['s_r_difference'] = s_r_difference
        movies_df['s_a_difference'] = s_a_difference

        # movies_df["Sentiment Score"] = pd.to_numeric(movies_df["Sentiment Score"])
        # movies_df["Audience Score"] = pd.to_numeric(movies_df["Audience Score"])
        # movies_df["Rotten Score"] = pd.to_numeric(movies_df["Rotten Score"])

        movies_df = movies_df.dropna() 

        st.dataframe(movies_df)

        movies_df = movies_df.sort_values(by=['Sentiment Score'])

        #st.dataframe(movies_df_2)
        st.write("Movie with largest Sentiment Score: ", movies_df["Name"][0])

        movies_df = movies_df.sort_values(by=['Sentiment Score'], ascending=False)
        st.write("Movie with lowest Sentiment Score: ", movies_df["Name"][0])

        movies_df = movies_df.sort_values(by=['a_r_difference'])
        st.write("Movie with largest Audience-Rotten Difference: ", movies_df["Name"][0])

        movies_df = movies_df.sort_values(by=['s_r_difference'])
        st.write("Movie with largest Sentiment-Rotten Difference: ", movies_df["Name"][0])

        movies_df = movies_df.sort_values(by=['s_a_difference'])
        #st.dataframe(movies_df)
        st.write("Movie with largest Sentiment-Audience Difference: ", movies_df["Name"][0])

        movies_df = movies_df.sort_values(by=['Sentiment Score'])
        movies_df.drop("Name", axis=1, inplace=True) 

        st.line_chart(movies_df)

def combo():
    st.title("Combination Finder")

    top_movies_df = pd.read_csv("IMDB-Movie-Data.csv")
    #top_movies_df.columns = ["Rank","Title","Genre","Description","Director","Actors","Year","Runtime (Minutes)","Rating","Votes","Revenue (Millions)","Metascore"]
    st.dataframe(top_movies_df)
    Dict = dict()
    Dict_rev = dict()

    combinations = pd.DataFrame()

    for index, movie in top_movies_df.iterrows():
        #print(movie)
        director = movie['Director']
        metascore = movie["Metascore"]
        revenue = movie["Revenue (Millions)"]
        actors_str = movie["Actors"]
        actors = actors_str.split(",")

        for a in actors:
            combo = director + "_" + a
            try:
                score_list = Dict.get(combo)
                score_list.append(metascore)
                Dict[combo] = score_list
            except:
                score_list = []
                score_list.append(metascore)
                Dict[combo] = score_list

            try:
                rev_list = Dict_rev.get(combo)
                rev_list.append(revenue)
                Dict_rev[combo] = rev_list
            except:
                rev_list = []
                rev_list.append(revenue)
                Dict_rev[combo] = rev_list

    combo_names = []
    combo_avg_scores = []
    combo_avg_rev = []

    min_movies = st.slider('Minimum number of collaborations.', 1, 4)

    for k in Dict:
        v = Dict.get(k)
        v2 = Dict_rev.get(k)
        avg_score = sum(v)/len(v)
        avg_rev = sum(v2)/len(v2)
        if len(v) >= min_movies:
            combo_names.append(k)
            combo_avg_scores.append(avg_score)
            combo_avg_rev.append(avg_rev)

    combinations["id"] = combo_names
    combinations["avg_metascore"] = combo_avg_scores
    combinations["avg_Revenue"] = combo_avg_rev

    st.dataframe(combinations)
    

def main():
    movie = get_movie()
    if st.button('Get Sentiment Score'):
        reviews(movie)
    trend_finder()
    combo()

if __name__ == "__main__":
    main()