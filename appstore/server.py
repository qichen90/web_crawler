from flask import Flask, render_template
import pymongo
from settings import MONGO_URI, MONGO_DATABASE

app = Flask(__name__, static_folder = "images")

@app.route("/")
def hello():
	client = pymongo.MongoClient(MONGO_URI)
	db = client[MONGO_DATABASE]
	apps = db["AppstoreItem"].find()
	client.close()
	return render_template("appstore_index.html", apps=apps)

if __name__ == "__main__":
	app.run(debug=True)# enable debugging feature to show some error