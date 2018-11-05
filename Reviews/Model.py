class Model():
    def select(self):
        """
        Retrives all entries from the database.
        :return List containing two dictionaries.
        """
        pass

    def insert(self, mov_name, release_year, director, mov_rating, runtime,
                genre, review, rev_name, rev_rating):
        """
        Insert a new entry into the database.
        Fixed values per movie:
        :param mov_name: Movie name
        :param release_year: Year movie was released
        :param director: Movie Director
        :param mov_rating: Movies MPAA rating (G, PG, PG13,etc)
        :param runtime: Movie runtime in minutes
        :param genre: Associated genres for a movie
        Review Values - 
        :param review: Text of movie review
        :param rev_name: Reviewers name
        :param rev_rating: Reviewers rating of movie. (Range 0 - 5)
        """
        pass
