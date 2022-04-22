import tomatopy as rtp
import pandas as pd
import streamlit as st
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

movies_list = rtp.scrape_movie_names(2008) # get top movies from 2008
movies_list = list(dict.fromkeys(movies_list)) # remove duplicates
movies_df = pd.DataFrame(movies_list)

# reviews = rtp.get_critic_reviews('https://www.rottentomatoes.com/m/x2_xmen_united')

# Build Site
st.title("Movie Data Analysis")
st.dataframe(movies_df)

option = st.selectbox('Select a Movie', movies_list)

main_info, reviews = rtp.scrape_movie_info(option)
print(main_info)
#print(reviews)

movie_scraper = MovieScraper(movie_title=option.lower())
movie_scraper.extract_metadata()

print(movie_scraper.metadata)

#print(type(main_info))

st.header(option, "Info")

for key, value in movie_scraper.metadata.items():
    st.write(key, ": ",value)

# st.header(option, "Reviews")

# for r in reviews:
#     st.write(r)

