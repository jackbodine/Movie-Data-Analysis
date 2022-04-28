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

    df = pd.read_csv("reviews.csv")
    df.columns = ["NA", "freshness", "source", "review", "date"]
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

    col1, col2, col3 = st.columns(3)
    col1.metric("Pos + Neg Polarity Score", int((pos_score + neu_score) * 100))
    col2.metric("Neg / Pos Score", int(100 - (neg_score / pos_score) * 100))
    col3.metric("Pos / (Neg + Pos) Score", int((pos_score / (neg_score + pos_score)) * 100))

    if option == "anaconda":
        st.balloons()

def trend_finder():
    st.title("Trend Finder")
    data_set_option = st.selectbox('Select a Dataset', range(2000, 2021))

    movies_list = rtp.scrape_movie_names(data_set_option) # get top movies from 1950
    movies_list = list(dict.fromkeys(movies_list)) # remove duplicates
    movies_list = movies_list[1:20]
    movies_df = pd.DataFrame(movies_list)
    #movies_df.columns = ["Movie", "Critic Score", "Audience Score", "Sentiment Score"]
    st.dataframe(movies_df)

    #movie_scores_df = pd.DataFrame
    #movies_scores_df.columns = ["Critic Score", "Audience Score", "Sentiment Score"]

    sentiment_score:List[integer] = []
    audience_score:List[integer] = []
    rotten_score:List[integer] = []

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

            audience_score.append(int(movie_scraper.metadata.get("Score_Audience")))
            rotten_score.append(int(movie_scraper.metadata.get("Score_Rotten")))
            sentiment_score.append(score)

        except:
            print("Movie Failed...")
            sentiment_score.append(0)
            audience_score.append(0)
            rotten_score.append(0)

    print("SENTIMENT_SCORE: ", sentiment_score)
    print("AUDIENCE_SCORE: ", audience_score)
    print("ROTTEN_SCORE: ", rotten_score)

    movies_df['Sentiment Score'] = sentiment_score
    movies_df['Audience Score'] = audience_score
    movies_df['Rotten Score'] = rotten_score

    # movies_df["Sentiment Score"] = pd.to_numeric(movies_df["Sentiment Score"])
    # movies_df["Audience Score"] = pd.to_numeric(movies_df["Audience Score"])
    # movies_df["Rotten Score"] = pd.to_numeric(movies_df["Rotten Score"])

    movies_df = movies_df.dropna() 
    movies_df.sort_values(by=['Sentiment Score'])

    st.dataframe(movies_df)

    movies_df.drop(0, axis=1, inplace=True) 

    st.line_chart(movies_df)

def main():
    movie = get_movie()
    reviews(movie)
    trend_finder()

if __name__ == "__main__":
    main()