from flask import Flask, jsonify, render_template, redirect
from scrape_mars import scrape
import pymongo
from flask_pymongo import PyMongo
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)
#db = client.marsDB

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    marsdata = mongo.db.mars_data.find_one()
    return render_template('index.html', structure = marsdata)


@app.route("/scrape")
def scrape_html():
    if "mars_data" in mongo.db.list_collection_names():
        collection = mongo.db['mars_data']
        collection.drop()
    html_structure = scrape()
    data = mongo.db.mars_data
    data.insert_one(html_structure)
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)