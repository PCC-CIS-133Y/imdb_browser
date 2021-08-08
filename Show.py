# The application logic layer of our N-tier architecture.
# Encapsulates information about a show from the IMDB database.
# Includes static methods that call matching methods in the data layer (the Database class).
# We do this to keep the UI portion of the program separate from the Database portion of the program.
class Show:
    # Construct a Show object
    def __init__(self, show_id, title, show_type, year, rating, num_votes):
        self.__id = show_id
        self.__title = title
        self.__type = show_type
        self.__year = year
        self.__rating = rating
        self.__num_votes = num_votes

    # Accessors. No setters are needed as the Show information won't change after we construct the object.
    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_type(self):
        return self.__type

    def get_year(self):
        return self.__year

    def get_rating(self):
        return self.__rating

    def get_num_votes(self):
        return self.__num_votes

    # Fetch a list of popular shows. We just hand this request over to the data layer.
    @staticmethod
    def fetch_popular_shows(genre, show_type, min_votes):
        from Database import Database

        return Database.fetch_popular_shows(genre, show_type, min_votes)


class ShowGenre:
    ALL_GENRES = "-- All Genres --"

    # Construct a ShowGenre object
    def __init__(self, genre):
        self.__genre = genre

    # Only need one accessor
    def get_genre(self):
        return self.__genre

    # Fetch the list of genres. We just hand this request over to the data layer.
    @staticmethod
    def fetch_genres():
        # Uncomment the following two lines of code and then removed the CachedData lines below
        # to use the database.
        #
        # from Database import Database
        # return Database.fetch_genres()

        # Used cached versions of the data to save time on startup.
        # Remove these two lines if using the database above.
        from CachedData import CachedData
        return CachedData.fetch_genres()


class ShowType:
    ALL_TYPES = "-- All Types --"

    # Construct a ShowType object
    def __init__(self, show_type):
        self.__type = show_type

    # Only need one accessor
    def get_type(self):
        return self.__type

    # Fetch the list of types. We just hand this request over to the data layer.
    @staticmethod
    def fetch_types():
        # Uncomment the following two lines of code and then removed the CachedData lines below
        # to use the database.
        #
        # from Database import Database
        # return Database.fetch_types()

        # Used cached versions of the data to save time on startup.
        # Remove these two lines if using the database above.
        from CachedData import CachedData
        return CachedData.fetch_types()
