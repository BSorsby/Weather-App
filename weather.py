from flask import Flask, render_template, request
import requests

app=Flask(__name__)
app.static_folder = 'static'

api_key = 'YOUR_API_KEY' #enter your API key here, see read.me file
 
#home page
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

#results page
@app.route('/results', methods=['POST'])
def get_results():
    city = request.form['city']
    data = get_weather(city)
    # take to error page if city not found
    if (data["cod"] == "404") or (city ==''):
        return render_template("error.html",
                                city = city)
    else:
        location = data["name"]
        temp = data["main"]["temp"]
        country = data["sys"]["country"]
        weather = data["weather"][0]["description"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
    return render_template("results.html",
                            city = city.capitalize(),
                            location=location,
                            temp=temp,
                            weather = weather.capitalize(),
                            country = country,
                            feels_like = feels_like,
                            temp_min = temp_min,
                            temp_max = temp_max)
  


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=".format(city)
    url = base_url + api_key + "&units=metric"
    r=requests.get(url)
    return r.json()

if __name__ == "__main__":
    app.run(debug=True)
