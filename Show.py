# The application logic layer of our N-tier architecture.
# Encapsulates information about a show from the IMDB database.
# Includes static methods that call matching methods in the data layer (the Database class).
# We do this to keep the UI portion of the program separate from the Database portion of the program.
class Show:
    # Construct a Show object
    def __init__(self, id, title, type, year, rating, num_votes):
        self._id = id
        self._title = title
        self._type = type
        self._year = year
        self._rating = rating
        self._num_votes = num_votes

    # Accessors. No setters are needed as the Show information won't change after we construct the object.
    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_type(self):
        return self._type

    def get_year(self):
        return self._year

    def get_rating(self):
        return self._rating

    def get_num_votes(self):
        return self._num_votes

    # Fetch a list of popular shows. We just hand this request over to the data layer.
    @staticmethod
    def fetch_popular_shows(genre, type, min_votes):
        from Database import Database

        return Database.fetch_popular_shows(genre, type, min_votes)