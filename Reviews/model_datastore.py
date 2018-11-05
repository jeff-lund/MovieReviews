# Cloud Datastore model
from flask import current_app
from google.cloud import datastore
from .translate import translate_text, translate_list

# Movie Model
# Holds static details for a given movie.
# :param mov_name: Name of the movie
# :param director: Director
# :param mov_rating: MPAA rating (i.e G, PG-13, R, etc)
# :param runtime: Runtime in minutes
# :param genre: Genre categories for a movie. Multiple genres are allowed. Stored in a single string
# with each value seperated by a comma.

# Review Model
# Hold reviews. mov_name acts as a key to associate each entry with Movie model.
# :param mov_name: Name of the movie
# :param review: Text of the review
# :param rev_name: Reviewers Name
# :param rev_rating: Reviewers rating, 1-5

def get_client():
    """
    Returns datastore client connection.
    """
    return datastore.Client(current_app.config['PROJECT_ID'])

def select(language):
  """
  Retrieves information from movies and reviews databases. Inserts both into
  dictionaries using the movie's name as the keyself.
  :return List of dictionaries. Movies database in index 0, reviews database in index 1.
  """
  ds = get_client()
  movies_query = ds.query(kind='Movie', order=['mov_name']).fetch()
  movies = {translate_text(m['mov_name'], language): {
      'release_year': m['release_year'],
      'director': m['director'],
      'mov_rating': m['mov_rating'],
      'runtime': m['runtime'],
      'genre': translate_list(m['genre'].split(','), language)}
      for m in movies_query}
  review_query = ds.query(kind='Review').fetch()
  reviews = dict()
  id = 0
  for row in review_query:
    if translate_text(row['mov_name'], language) not in reviews:
      reviews[translate_text(row['mov_name'], language)] = []

    reviews[translate_text(row['mov_name'], language)].append({
      'review':translate_text(row['review'], language),
      'rev_name':row['rev_name'],
      'rev_rating':row['rev_rating'],
      'id': id})
    id += 1
  return [movies, reviews]

def insert(mov_name, release_year, director, mov_rating,
		runtime, genre, review, rev_name, rev_rating):
  """
  Inserts a new review into databases. If it is the first review for a movies
  then a new entry is created in movies database. Otherwise only review information
  is inserted.
  """
  ds = get_client()
  key = ds.key('Movie', mov_name)
  if ds.get(key) is None:
    with ds.transaction():
      key = ds.key('Movie', mov_name)
      movie = datastore.Entity(key=key)
      movie.update({
        'mov_name': mov_name,
        'release_year': release_year,
        'director': director,
        'mov_rating': mov_rating,
        'runtime': runtime,
        'genre': genre
      })
      ds.put(movie)

  with ds.transaction():
    key = ds.key('Review')
    new_rev = datastore.Entity(key=key)
    new_rev.update({
      'mov_name': mov_name,
      'review': review,
      'rev_name': rev_name,
      'rev_rating': rev_rating
    })
    ds.put(new_rev)

