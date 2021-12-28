import streamlit as st


def pet_container(row):
    link = "https://www.pawschicago.org" + row["Link"]
    st.subheader(f"[{row.name}]({link})")
    col1, col2, col3 = st.columns([2, 3, 3])
    
    col1.image(row["Image"])
    
    details = f"""
        - {row['Breed']}
        - {row['Age']}
        - {row['Gender']}
        - {row['Weight']} lbs.
        - {row['Location']}
    """
    col2.markdown(details)

    rating_names = ["Children", "Dogs", "Cats", "Home Alone", "Activity"]
    ratings = ""
    for rating in rating_names:
        value = int(row[rating])
        ratings += f"- {rating}: {value if value != 0 else 'Unknown'}\n"
    col3.markdown(ratings)

    st.markdown("---")


def display_pet_container(row):
    try:
        pet_container(row)
    except ValueError:
        pass


def filter_dataframe(df):
    ratings = ["Children", "Dogs", "Cats", "Home Alone", "Activity"]
    for rating in ratings:
        # lower_limit = st.session_state[rating][0]
        # upper_limit = st.session_state[rating][1]
        # df = df[df[rating] >= lower_limit]
        # df = df[df[rating] <= upper_limit]
        limit = st.session_state[rating]
        df = df[df[rating] >= limit]
    return df
