import io
import webbrowser
import requests
from flask import Flask, render_template
from urllib.request import urlopen
from PIL import Image
import base64

app = Flask(__name__)

class NewsApp:
    def __init__(self):
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=0b5f016413dd45cdb800cb781669752c').json()

    def load_news_item(self, index):
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            base64_data = base64.b64encode(raw_data).decode('utf-8')
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url).read()
            base64_data = base64.b64encode(raw_data).decode('utf-8')

        heading = self.data['articles'][index]['title']
        details = self.data['articles'][index]['description']
        url = self.data['articles'][index]['url']

        return base64_data, heading, details, url

news_app = NewsApp()

@app.route('/')
def index():
    index = 0  # You can set the index of the initial news item here.
    photo, heading, details, url = news_app.load_news_item(index)
    return render_template('index.html', photo=photo, heading=heading, details=details, url=url, current_index=index)

@app.route('/<int:index>')
def show_news_item(index):
    photo, heading, details, url = news_app.load_news_item(index)
    return render_template('index.html', photo=photo, heading=heading, details=details, url=url, current_index=index)

if __name__ == '__main__':
    app.run(debug=True)
