from flask import Flask, url_for, render_template, jsonify, abort, make_response

app = Flask(__name__)

# This stores our movies
movies = [
  {
    'id': 1,
    'title': 'The Shawshank Redemption', 
    'plot': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
    'director': 'Frank Darabont',
    'starring': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton'],
    'genre': 'Drama',
    'year': '1994'
  },
  {
    'id': 2,
    'title': 'The Dark Knight', 
    'plot': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
    'director': 'Christopher Nolan',
    'starring': ['Christian Bale', 'Heath Ledger', 'Aaron Eckhart'],
    'genre': 'Action',
    'year': '2008' 
  },
  {
    'id': 3,
    'title': 'The Silence of the Lambs', 
    'plot': 'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.',
    'director': 'Jonathan Demme',
    'starring': ['Jodie Foster', 'Anthony Hopkins', 'Lawrence A. Bonney'],
    'genre': 'Thriller',
    'year': '1991' 
  },
  {
    'id': 4,
    'title': 'Back to the Future', 
    'plot': 'Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the eccentric scientist Doc Brown.',
    'director': 'Robert Zemeckis',
    'starring': ['Michael J. Fox', 'Christopher Lloyd', 'Lea Thompson'],
    'genre': 'Sci-Fi',
    'year': '1985' 
  },
  {
    'id': 5,
    'title': 'Harry Potter and the Sorcerer\'s Stone', 
    'plot': 'An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.',
    'director': 'Chris Columbus',
    'starring': ['Daniel Radcliffe', 'Rupert Grint', 'Richard Harris'],
    'genre': 'Fantasy',
    'year': '2001' 
  }
]

# Home route
@app.route("/")
def home():
  return render_template("home.html")

# Entry point of our API
# Returns a list of all movies
@app.route("/api/v1.0/movies", methods=["GET"])
def get_movies():
  return jsonify({'movies': movies})  

# Get movie by id
@app.route("/api/v1.0/movies/<int:id>", methods=["GET"])
def get_movie(id):
  data = [movie for movie in movies if movie['id'] == id]
  if len(data) == 0:
    abort(404)
  return jsonify({'movie': data[0]})

# Add new movie
@app.route("/api/v1.0/movies", methods=["POST"])
def add_movie():
  if not request.json or not 'title' in request.json:
    abort(400)
  movie = {
    id: movies[-1]['id'] + 1,
    title: request.json['title'],
    plot: request.json.get('plot', ''),
    director: request.json.get('director', ''),
    genre: request.json.get('genre', ''),
    starring: request.json.get('starring', ''),
    year: request.json.get('year', '')
  }
  movies.append(movie)
  return jsonify({'movie': movie})

# Update existing movie
@app.route('/api/v1.0/movies/<int:id>', methods=['PUT'])
def update_movie(id):
  data = [movie for movie in movies if movie['id'] == id]
  if len(movie) == 0:
    abort(404)
  if not request.json:
    abort(400)
  if 'title' in request.json and type(request.json['title']) is not unicode:
    abort(400)
  if 'plot' in request.json and type(request.json['plot']) is not unicode:
      abort(400)
  
  # Update movie attribute e.g. `title` with
  # ...new attribute value from request
  # ...if request does not have an updated value
  # ...reuse the existing value for the attribute    
  data[0]['title'] = request.json.get('title', data[0]['title'])
  data[0]['plot'] = request.json.get('plot', data[0]['plot'])
  data[0]['director'] = request.json.get('director', data[0]['director'])
  data[0]['starring'] = request.json.get('starring', data[0]['starring'])
  data[0]['genre'] = request.json.get('genre', data[0]['genre'])
  data[0]['year'] = request.json.get('year', data[0]['year'])
  return jsonify({'movie': data[0]})

# Delete movie
@app.route('/api/v1.0/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
  data = [movie for movie in movies if movie['id'] == id]
  if len(data) == 0:
      abort(404)
  movies.remove(data[0])
  return jsonify({'result': True})

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Could not find that movie'}), 404)  

# Handle 400 errors
@app.errorhandler(400)
def bad_request_error(error):
  return make_response(jsonify({'error': 'Bad request'}), 400)  

if __name__ == '__main__':
  app.run(debug=True)
  
    