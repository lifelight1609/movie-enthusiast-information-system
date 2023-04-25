from flask import Flask, render_template, request
from pymongo import MongoClient
from db import get_movies_on_name, get_top10_movies_on_score,get_movies_on_genre,get_movies_released_in_year,get_movies_on_country,get_movies_on_multiple_inputs, add_movies, db_delete_movie
from visualisation import generate_plots

app = Flask(__name__)

# load configuration from .ini file
app.config.from_pyfile('.ini')

# create MongoClient instance
client = MongoClient(app.config['MONGO_URI'])

# check connection to database
if client:
    print("Connected to MongoDB database.")

db = client['movie_enth']
collection = db['movies']

@app.route('/')
def home():
    results = list()
    query = request.form.get("query")
    return render_template("index.html")

@app.route('/movies', methods=["GET", "POST"])
def display_top_movies():  
        results = []
        try:
            query_results = get_top10_movies_on_score(collection)
            for x in query_results: 
                results.append(x)
            return render_template("top_movies.html", results=results,count=len(results))
          
        except Exception as error:
            print("In error" , error)
            return render_template("error.html")

@app.route('/results', methods=["GET", "POST"])
def display_results():
 
        results = []
        try:
            moviename = request.form['name']
            genre = request.form['genre']            
            country = request.form['country']
            year = request.form['year']
            criteria = {}
            
            if moviename:
                query_results = get_movies_on_name(collection, moviename)
            if genre != "select":
                query_results = get_movies_on_genre(collection, genre)
            if year !="select":
                year = int(year)
                query_results = get_movies_released_in_year(collection, year)               
            if country != "select":
                query_results = get_movies_on_country(collection, country)
            
            if genre != "select" and year != "select" and  country != "select" and moviename !="":
                criteria = {
                    "genre": { "$regex": genre, "$options": "i" },
                    "year": year,
                    "country": { "$regex": country, "$options": "i" },
                    "name": { "$regex": moviename, "$options": "i" }
                }
                query_results = get_movies_on_multiple_inputs(collection, criteria)
                
            #print(query_results)
            for x in query_results: 
                results.append(x)

            return render_template("results.html", results=results,count=len(results))
        
        except Exception as error:
            print("In error" , error)
            return render_template("error.html")


@app.route('/dashboard',methods=["GET", "POST"])
def dashboard():
    try:
        plots = generate_plots(collection)
        return render_template("dashboard.html", visualisation_plots=plots)
          
    except Exception as error:
        print("In error" , error)
        return render_template("error.html")

@app.route('/about')
def about():
    print("about")
    return render_template('about.html')

@app.route('/addmovie',methods=['GET','POST'])
def add_movie():
    return render_template('addMovie.html')

@app.route('/insertmovie',methods=['GET','POST'])
def insert_movie():
    try:
        moviename = request.form['name']
        genre = request.form['genre']            
        country = request.form['country']
        year = int(request.form['year'])
        rating = request.form['rating']
        score = float(request.form['score'])            
        star = request.form['star']
        runtime = int(request.form['runtime'])
        
        new_movie = {
                    "name": moviename,
                    "rating": rating,
                    "genre": genre,
                    "year": year,
                    "country": country,
                    "score": score,
                    "star": star,
                    "runtime": runtime
                    }
        result = add_movies(collection, new_movie)
        success = True
        return render_template('addMovie.html', success=success)
    except Exception as error:
        print("In error" , error)
        return render_template("error.html")


@app.route('/deletemovie',methods=['GET','POST'])
def delete_movie():
    return render_template('deleteMovie.html')

@app.route('/deletedmovie',methods=['GET','POST'])
def deleted_movie():
    try:
        moviename = request.form['name']
        deletemovie = {"name": moviename}
        db_delete_movie(collection, deletemovie)
        success = True
        return render_template('deleteMovie.html', success=success)
    except Exception as error:
        print("In error" , error)
        return render_template("error.html")

@app.route('/Contact',methods=['GET','POST'])
def Contact():
    return render_template('contact.html')

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)


