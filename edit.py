from flask import *
from flask_pymongo import PyMongo
from pprint import pprint
from pymongo import MongoClient
import datetime

app = Flask(__name__)
app.secret_key = "SESSION_KEY"
app.config["MONGO_URI"] = "mongodb://localhost:27017/diarydb"
mongo = PyMongo(app)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client['diarydb']
posts = db['posts']

@app.route('/edit', methods=['GET','POST'])
def edit():

    if request.method == 'GET':
        return render_template('edit.html')
    print(request.form())
    if request.method == 'POST':
        pass


