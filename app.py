from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# set up flask
app = Flask(__name__)

#tell python how to connect to mongo with pymongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define route for the html page

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# set up scraping route
@app.route("/scrape")
# accesses database, scrapes new data, updates database
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"  

#tells flask to run

if __name__ == "__main__":
   app.run()