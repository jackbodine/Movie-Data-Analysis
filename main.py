import tomatopy as rtp
import pandas as pd
import streamlit as st
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
    movies_df = pd.DataFrame(movies_list)
    #movies_df.columns = ["Movie", "Critic Score", "Audience Score", "Sentiment Score"]
    st.dataframe(movies_df)

def main():
    movie = get_movie()
    reviews(movie)
    trend_finder()

if __name__ == "__main__":
    main()