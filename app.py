import os
import requests
from covid import Covid
from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    url = 'http://api.ipstack.com/check?access_key=a2acd36ecdb97d72073d65b752df8eb3'
    r = requests.get(url)
    js = r.json()
    strs = js['country_name']
    covid = Covid()
    try:
        data = covid.get_status_by_country_name(strs)
    except:
        data = covid.get_status_by_country_name(js['country_code'])
    
    
    return render_template("index.html", country=strs, country_code=js['country_code'], city=js['city'], cases=data["confirmed"])


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    app.run()