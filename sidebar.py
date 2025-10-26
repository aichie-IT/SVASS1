import streamlit as st

st.set_page_config(
    page_title="Student Survey"
)

visualise = st.Page('main.py', title='Student Survey Visualization', icon=":material/school:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
