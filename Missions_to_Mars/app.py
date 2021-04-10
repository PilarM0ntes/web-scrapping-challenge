from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():
    scrape_results = mongo.db.scrape_data.find_one()
    return render_template("index.html", data=scrape_results)


@app.route("/scrape")
def scraper():
    # Run the scrape function
    scrape_results = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.scrape_data.update({}, scrape_results, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)