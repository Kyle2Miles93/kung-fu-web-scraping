from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/kungFu"
mongo = PyMongo(app)

@app.route("/")
def index():
    sifus = mongo.db.sifus.find_one()
    return render_template("index.html", sifus=sifus)

@app.route("/scrape")
def scrape():
    sifus = mongo.db.sifus
    sifus_data = scraping.scrape_all()
    sifus.update({}, sifus_data, upsert=True)
    print("Scraping Sucessful!")
    return redirect('/', code=302) 

if __name__ == "__main__":
   app.run(debug=True)