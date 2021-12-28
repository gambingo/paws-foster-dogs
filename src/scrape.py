import requests

from bs4 import BeautifulSoup
import pandas as pd


def make_soup(url):
    r = requests.get(url)
    page_source = r.text
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup


def build_dataframe():
    fostering_homepage = "https://www.pawschicago.org/how-to-help/foster/pets-available-for-fostering"
    soup = make_soup(fostering_homepage)
    df = thumbnails_to_dataframe(soup)
    return df


def thumbnails_to_dataframe(soup):
    df = pd.DataFrame()
    
    dog_div = soup.find("article", {"class": "dogs"})
    pet_divs = dog_div.find_all("div", {"class": "adopt-pet"})
    for pet in pet_divs:
        thumbnail_data = parse_pet_title_div(pet)

        print(thumbnail_data["Name"])
        details_data = get_pet_details(thumbnail_data["Link"])
        data = {**thumbnail_data, **details_data}
        df = df.append(data, ignore_index=True)

    df.set_index("Name", inplace=True)
    return df


def parse_pet_title_div(pet):
        link = pet.find("a")
        name = pet.find("h3").get_text()
        img = pet.find("img")
        foster_type = pet.find("h6").get_text()
        location = pet.find("h5").get_text()

        data = {
            "Name":         name,
            "Foster Type":  foster_type,
            "Location":     location,
            "Link":         link["href"],
            "Image":        img["src"],
        }
        return data


def get_pet_details(pet_url):
    url = "https://www.pawschicago.org/" + pet_url
    soup = make_soup(url)
    rating_data = scrape_ratings(soup)
    details_data = scrape_facts(soup)
    data = {**rating_data, **details_data}
    return data
    

def scrape_ratings(soup):
    data_found = {}
    rating_class_names = {
        "Children":      "grey-bg children clearfix",
        "Dogs":           "light-grey-bg dogs clearfix",
        "Cats":           "grey-bg cats clearfix",
        "Home Alone":    "light-grey-bg home_alone clearfix",
        "Activity":      "grey-bg activity clearfix",
    }

    class_name_scores = {
       "r1 active": 1,
       "r2 active": 2,
       "r3 active": 3,
       "r4 active": 4,
       "r5 active": 5,
       "rating_default r0": 0,
    }

    for rating_name, classname in rating_class_names.items():
        rating_element = soup.find("div", {"class": classname})
        rating_element = rating_element.find("span", {"class": "rating_default"})

        rating_found = None
        for rating in class_name_scores.keys():
            element = rating_element.find("span", {"class": rating})
            if element is not None:
                rating_found = rating

        if rating_found is None:
            # print(rating_element)
            rating_found = "rating_default r0"

        data_found[rating_name] = class_name_scores[rating_found]

    return data_found


def scrape_facts(soup):
    data_found = {}

    facts_class_to_descr = {
        "Breed":    "floating-tabs breed-dog",
        "Gender":   "floating-tabs gender grey-bg",
        "Age":      "floating-tabs age",
        "Weight":   "floating-tabs weight grey-bg",
        "Location": "floating-tabs location",
    }

    for fact, class_name in facts_class_to_descr.items():
        try:
            _div = soup.find("div", {"class": class_name})
            _text = _div.find("p").get_text()
            data_found[fact] = _text
        except AttributeError:
            pass

    return data_found


def clean_dataframe(df):
    df["Weight"] = df["Weight"].apply(
        lambda x: float(x.replace("lbs", ""))
    )

    df["Age Filter"] = df["Age"].apply(
        lambda 
    )


def numeric_age(string_age):
    if "Year" in string_age:
        return float(string_age.split(" ")[0])
    if "Month" in string_age:
        return float(string_age.split(" ")[0])/12



if __name__ == '__main__':
    df = build_dataframe()
    df.to_csv("pets_available_for_fostering.csv")