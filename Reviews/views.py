#!/usr/bin/env python3
# Copyright (c) 2018 Jeff Lund, Kevin Young
"""
Movie review flask app
"""

from flask import Flask, redirect, request, url_for, render_template, current_app, Blueprint
from Reviews import get_model
from .talktome import read_text
from .translate import translate_text, translate_list
from google.cloud import storage

views = Blueprint('views', __name__)

@views.route('/<language>', methods=['GET', 'POST'])
@views.route('/index/<language>', methods=['GET', 'POST'])
def main(language):
  """
  Renders landing page for movie review site. POST request changes language setting 
  and redirects back to the index page to update the displayed language within.
  """
  # Creates a list of the html page text and translates it for use in the index page.
  pageText = ['Ripe Tomatoes', 'Welcome to Ripe Tomatoes', 'A fresher movie review site', 'Please select the review language',
  	'English', 'French', 'Italian', 'Korean', 'Spanish', 'Turkish', 'Submit', 'Current language is', 
    'Movie Reviews', 'Add Movie Reviews']
  pageTranslation = translate_list(pageText, language)

  if request.method == 'POST':
     # Sets the language variable to the desired displayed language and speech.
     language = request.form['review_lang']
     return redirect(url_for('views.main', language=language))

  return render_template('index.html', lang=full_language(language), text=pageTranslation, language=language)

@views.route('/reviews/<language>', methods=['GET', 'POST'])
def reviews(language):
  """
  Renders all reviews from the model.
  POST request redirects to synth page where an audio element plays the spoken text of the selected review.
  """
  # Databases returned in tuple (Movie, Review).
  # Must be unpacked before use in render template.
  model = get_model()
  dbs = model.select(language)
  if dbs is None:
      dbs = [[],[]]
  movies = dbs[0]
  reviews = dbs[1]
  if request.method == 'POST':
      text = 'placeholder'
      id = int(request.form['synth'])
      # Find text associated with review id.
      for row in reviews.values():
          for list_element in row:
              if id == list_element['id']:
                  text = list_element['review']
      filename = read_text(text, language)
      return redirect(url_for('views.synth', filename=filename, language=language))

  # Creates a list of the html page text and translates it for use in the reviews page.
  pageText = ['Ripe Tomatoes', 'Movie Reviews!', 'Main Page', 'Add Movie Review', 'Directed By', 'Released', 'Rating', 'Runtime',
  	'minutes', 'Genre', 'Rating', 'Author']
  pageTranslation = translate_list(pageText, language)

  return render_template('reviews.html', movies=movies, reviews=reviews, text=pageTranslation, language=language)

@views.route('/submit/<language>', methods=['GET', 'POST'])
def submit(language):
  """
  Renders submission form to submit a new movie review.
  """
  # Creates a list of the html page text and translates it for use in the submit page.
  pageText = ['Ripe Tomatoes', 'Name of Movie', 'Released', 'Year', 'Director', 'Movie Rated', 'Not Rated',
  	'Runtime', 'minutes', 'Genres', 'Write your review here', 'Rating', 'Reviewed by',
  	'Submit Review', 'Main Page']

  # Defines available genres for the movie. Makes list available in GET and POST.
  genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', \
    'Documentary', 'Drama', 'Family', 'Fantasy', 'Film Noir', 'History', 'Horror', \
    'Indie','Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', \
    'Superhero', 'Thiller', 'War', 'Western']
  pageTranslation = translate_list(pageText, language)
  genresTranslation = translate_list(genres, language)

  if request.method == 'POST':
    model = get_model()
    genre_selected = [gen for gen in genres if gen in request.form]
    model.insert(request.form['mov_name'], request.form['release_year'], \
      request.form['director'], request.form['mov_rating'], \
      request.form['runtime'], ','.join(genre_selected), request.form['review'], \
      request.form['rev_name'], request.form['rev_rating'])

    return redirect(url_for('views.reviews', language=language))

  return render_template('submit.html', genres=genresTranslation, text=pageTranslation, language=language)

@views.route('/synth/<filename>/<language>')
def synth(filename, language):
    """
    Loads a given mp3 file from storage bucket to HTML5 audio element. 
    Used to play audio reviews generated from Text-to-Speech API.
    """
    bucket = storage.Client().get_bucket(current_app.config['STORAGE'])
    blob = bucket.get_blob(filename)
    audio = blob.public_url

    # Creates a list of the html page text and translates it for use in the synth page.
    pageText = ['Ripe Tomatoes', 'Your browser does not support the audio element.', 'Movie Reviews']
    pageTranslation = translate_list(pageText, language)

    return render_template('synth.html', audio=audio, text=pageTranslation, language=language)

def full_language(language):
  """ 
  Takes the language variable and returns the full language text. 
  """
  lang = {'en': 'English', 'es': 'Spanish', 'it' : 'Italian', 'fr': 'French', 'tr': 'Turkish', 'ko': 'Korean'}
  return  translate_text(lang[language], language)