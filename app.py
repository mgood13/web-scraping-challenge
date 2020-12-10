from flask import Flask, jsonify, render_template
from scrape_mars import scrape



app = Flask(__name__)


@app.route("/")
def home():
    greeting = 'hello'
    return jsonify(greeting)


@app.route("/scrape")
def scrape_html():
    html_structure = scrape()
    print('here')
    return render_template('index.html', structure = html_structure)




if __name__ == '__main__':
    app.run(debug=True)