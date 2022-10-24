from flask import Flask, render_template, redirect
import pymongo
import mars_scrape

app = Flask(__name__)

# setup mongo connection
conn = 'mongodb+srv://cbarraza:Gramercy1@cluster0.q26pfay.mongodb.net/Cluster0'
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
    # Find one record of data from the mongo database
    mars_data = db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that button will trigger the scrape function
@app.route("/mars_scrape")

def scrape():
    #?
    mars_data = db.collection.find_one()

    # Run the scrape function and save the results to a variable
    mars_data = mars_scrape.scrape()

    # Update the Mongo database using update and upsert=True
    db.collection.update_one({}, {"$set": mars_data}, upsert=True)
   
    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)