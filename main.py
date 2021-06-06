from flask import *
from flask_pymongo import PyMongo
from pprint import pprint
from pymongo import MongoClient
import datetime

from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "SESSION_KEY"
app.config["MONGO_URI"] = "mongodb://localhost:27017/diarydb"
mongo = PyMongo(app)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client['diarydb']
posts = db['posts']


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            return redirect('/home')
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print('u:', username, 'p:', password)

        data = mongo.db.users.find()
        for v in data:
            pprint(v)
            if v['username'] == username and v['password'] == password:
                session['user'] = {'username': username, 'password': password, 'logtime': datetime.datetime.utcnow()}

                session['login'] = 'login'
                print('user found and SESSION started')
            else:
                print('user not found...')
        return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        mongo.db.users.insert_one({'username': username,'password': password, "name": name})
        return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('login', None)
    return redirect ('/')

@app.route('/home', methods=['GET','POST'])
def home():
    postlist = {}
    plist = []


    if request.method == 'GET':

        posts = mongo.db.posts.find({'username': session['user']['username']}).sort('time', -1)
        print(posts)

        print(postlist)
        date = datetime.datetime.now()
        cdate = date.strftime("%d/%m/%Y %I:%M %p %Z")




        return render_template('home.html', posts = posts, currentuser = session['user']['username'], cdate = cdate)


    if request.method == 'POST':
        results = request.form.get("postval")
        print(request.form)
        print(request.form['post'])
        r = request.form.get("date")


        newpost = {'username': session['user']['username'], 'post': request.form['post'], 'time': request.form['date']}


        mongo.db.posts.insert(newpost)
        return redirect('/home')

@app.route('/edit', methods=['GET','POST'])
def edit():

    if request.method == 'GET':
        id = request.args.get('postid')

        return render_template('edit.html', id = id )
    if request.method == 'POST':
        print(request.form)
        npost = request.form.get('npost')
        print(npost)
        id = request.form.get('id1')
        print(id)

        #objectid = ObjectId(' '"' + str(id) + '"' + ')
        objectid = ObjectId(str(id))
        print(objectid)
        query = ({"username": session['user']['username']} and {"_id": objectid})
        print(mongo.db.posts.find({'_id': objectid}))

        print(objectid)
        print(npost)

        mongo.db.posts.update(
            {'_id': objectid},
            { '$set': {'post': npost}, } ,multi=True)
        print('Success')

        return redirect('/home')
@app.route('/delete', methods=['GET','POST'])
def delete():

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        id = request.form.get('postid')
        objectid = ObjectId(str(id))
        print(objectid)
        mongo.db.posts.remove({'_id': objectid})
        return redirect('/home')












if __name__ == '__main__':
    app.run(debug=True)