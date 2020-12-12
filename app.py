# Import the dependencies
from flask import Flask, jsonify, render_template, redirect
from scrape_mars import scrape
import pymongo
from flask_pymongo import PyMongo

# Initialize the flask app
app = Flask(__name__)

# Connect to the mongo database
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)


# The home route which is our display page. It takes the information from the mars storage database that we've scraped into.
@app.route("/")
def home():
    marsdata = mongo.db.mars_data.find_one()
    return render_template('index.html', structure = marsdata)

# This route is run when the "TO MARS!" button is pressed. If the database has information in it then it is emptied.
# Then it runs the scrape function and then stores it in the mongo database. It finally reroutes back to the initial
# page so that the user never sees a page change.

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