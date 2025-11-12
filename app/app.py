import streamlit as st

from pipeline.pipeline import AnimeRecommendationPipeline

st.set_page_config(page_title='Anime Recommender', layout='wide')


@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()


pipeline = init_pipeline()

st.title('Anime Recommender System')

query = st.text_input('Enter your anime preferences. ex, : light hearted anime with school setting')

if query:
    with st.spinner('Fetching recommendations for you ...'):
        response = pipeline.recommend(query)
        st.markdown('### Recommendations')
        st.write(response)
