import streamlit as st
import pandas as pd

import src.logic as lg


st.header("PAWS Pets Available for Fostering")
st.write("\n\n\n")
df = pd.read_csv("pets_available_for_fostering.csv")
df.set_index("Name", inplace=True)
st.write(df)


# Sidebar
st.sidebar.header("Filter")
msg = """
    Limit your search to pups with ratings of at least this much. 
    Note: if a dog is listed with a rating of zero it means that rating is 
    unknown.
"""
st.sidebar.write(msg)
for rating in ["Children", "Dogs", "Cats", "Home Alone", "Activity"]:
    st.sidebar.slider(
        rating, 
        value=0, 
        # value=(0,5),
        min_value=0, 
        max_value=5, 
        format = "%f paws",
        key=rating
        )

    # options = ["Unknown", "1 paw", "2 paws", "3 paw", "4 paws", "5 paws"]
    # st.sidebar.select_slider(rating, 
    #     options=options, 
    #     value=["Unknown", "5 paws"],
    #     key=f"{rating}_select")

# print(st.session_state)
filtered_df = lg.filter_dataframe(df)


# Main Page
for ii, row in filtered_df.iterrows():
    lg.display_pet_container(row)