
def get_movies_on_name(collection, moviename):    
    similar_movies = collection.find({"name": {"$regex": moviename, "$options": 'i'}})
    return similar_movies
    
def get_movies_on_genre(collection, genre):
    movies = collection.find({"genre": {"$regex": genre, "$options": "i"}}).limit(20)
    return movies
    
def get_top10_movies_on_score(collection):
    top_10_scores = collection.find().sort("score", -1).limit(20)
    return top_10_scores
    
def get_movies_released_in_year(collection, year):
    movies = collection.find({"year": year}).limit(20)
    return movies

def get_movies_on_country(collection, country):
    movies = collection.find({"country": {"$regex": country, "$options": "i"}}).limit(20)
    return movies
    
def get_movies_on_multiple_inputs(collection, criteria):
    
    movies = collection.find({"$and": [criteria]})
    # movies = collection.find(criteria).limit(20)
    return movies
    
def add_movies(collection, new_movie):
    print(new_movie)
    collection.insert_one(new_movie)
    
def db_delete_movie(collection, deletemovie):
    collection.delete_one(deletemovie)
