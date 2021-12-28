import streamlit as st
import pandas as pd

import src.logic as lg


st.header("PAWS Pets Available for Fostering")
st.write("\n\n\n")
df = pd.read_csv("pets_available_for_fostering.csv")
df.set_index("Name", inplace=True)
# st.write(df)


# Filters
with st.expander("Filters", expanded=True):
    msg = """
        Limit your search to pups with ratings of at least this much. 
        Note: if a dog is listed with a rating of zero it means that rating is 
        unknown.
    """
    st.write(msg)
    for rating in ["Children", "Dogs", "Cats", "Home Alone", "Activity"]:
        st.slider(
            rating, 
            # value=0, 
            value=(0,5),
            min_value=0, 
            max_value=5, 
            format = "%f paws",
            key=rating
            )

    st.slider("Age", 
        value=1, 
        min_value=0, 
        max_value=int(df["Age Filter"].max()),
        format = "%f years",
        key="Age Filter",
    )

    max_weight = int(df["Weight"].max())
    st.slider("Weight", 
        value=(0, max_weight), 
        min_value=0,
        max_value=max_weight+1,
        format = "%f lbs",
        key="Weight",
        )

# print(st.session_state)
filtered_df = lg.filter_dataframe(df)


# Main Page
for ii, row in filtered_df.iterrows():
    lg.display_pet_container(row)