import requests
from bs4 import BeautifulSoup
import html

country = {
    "us": "get_us_address",
}

basic_info_columns = ["full_name", "gender", "title", "race", "birthday", "ssn", ]
address_columns = ["street", "city", "state", "state_full", "zip_code", "phone", "mobile" ,"height", "weight",
                   "hair_color", "blood_type", "mothers_maiden_name", "marital_status", "educational_background",
                   "employment_status", "month_salary", "occupation", "company_name", "company_size", "industry",
                   "credit_card_type", "credit_card_num", "cvv2", "credit_card_expires",
                   # "vehicle",
                   # "car_license_plate", "online_status", "online_sign", "online_bio", "interest", "fav_color",
                   # "fav_movie", "fav_music", "fav_song", "fav_book", "fav_sports", "fav_tv", "fav_movie_star",
                   # "fav_singer", "fav_food", "personality", "personal_style", "online_username", "online_password",
                   # "website", "sec_question", "sec_answer", "browser_agent", "os_system", "guid", "telephone_country_code"
                   ]
more_basic_address_columns = []
info = dict()

def get_basic_info(soup):
    basic_info = {}
    common_table = soup.find('table', class_='table common-table')
    for i, row in enumerate(common_table):
        for j, cell in enumerate(row):
            if j % 2 == 1:
                basic_info[basic_info_columns[i]] = html.unescape(cell.text)
    basic_info["first_name"], basic_info["mid_name"], basic_info["last_name"] = basic_info["full_name"].split()
    return basic_info



def get_fake_profile(name="us", city="Goodlettsville"):
    url = f"https://www.fakeaddressgenerator.com/World_Address/{country[name]}/city/{city}"

    page_source = requests.get(url).text
    soup = BeautifulSoup(page_source, 'html.parser')

    info.update(get_basic_info(soup))

    i = 0
    for row in soup.find_all("div", class_="col-sm-8 col-xs-6 right"):
        for strong in row:
            for input_tag in strong:
                # print(type(input_tag))
                try:
                    if input_tag.get("value"):
                        if address_columns[i] == "credit_card_expires":
                            info[address_columns[i]] = "07/2023"
                            i += 1
                            info[address_columns[i]] = input_tag.get("value").strip()
                        else:
                            info[address_columns[i]] = input_tag.get("value").strip()
                        i += 1

                except Exception as e:
                    pass


    return  info


def main():
    print(get_fake_profile())

if __name__ == "__main__":
    main()