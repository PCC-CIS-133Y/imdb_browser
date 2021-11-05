from Database import Database
from CachedData import CachedData


class ShowService:
    # Fetch a list of popular shows. We just hand this request over to the data layer.
    @staticmethod
    def fetch_popular_shows(genre, show_type, min_votes):
        return Database.fetch_popular_shows(genre, show_type, min_votes)

    # Fetch the list of genres. We just hand this request over to the data layer.
    @staticmethod
    def fetch_genres():
        # Uncomment the following line of code and then removed the CachedData line below
        # to use the database.
        #
        # return Database.fetch_genres()

        # Used cached versions of the data to save time on startup.
        # Remove this line if using the database above.
        return CachedData.fetch_genres()

    # Fetch the list of types. We just hand this request over to the data layer.
    @staticmethod
    def fetch_types():
        # Uncomment the following line of code and then removed the CachedData line below
        # to use the database.
        #
        # return Database.fetch_types()

        # Used cached versions of the data to save time on startup.
        # Remove this line if using the database above.\
        return CachedData.fetch_types()
