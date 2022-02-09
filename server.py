from flask import Flask, render_template
import requests
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/guess/<name>')
def guess(name):
    response_api_gender = requests.get(f"https://api.genderize.io?name={name}")
    data_gender = response_api_gender.json()
    gender = data_gender["gender"]
    response_api_age = requests.get(f"https://api.agify.io?name={name}")
    data_age = response_api_age.json()
    age = data_age["age"]
    response_api_nationality = requests.get(f"https://api.nationalize.io/?name={name}")
    data_nationality = response_api_nationality.json()
    country_codes = [country["country_id"] for country in data_nationality["country"]]
    countries = []
    for code in country_codes:
        response_api_country = requests.get(f"https://restcountries.com/v3.1/alpha/{code}")
        data_country = response_api_country.json()
        country = data_country[0]["name"]["common"]
        countries.append(country)
    if countries:
        country_guess_sentence = f"I guess you are from {' or '.join(countries)}."
    else:
        country_guess_sentence = "I can not guess where you are from :/"
    return render_template("index.html", name=name.title(), gender=gender, age=age, countries=country_guess_sentence)


if __name__ == "__main__":
    app.run(debug=True)
