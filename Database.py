import pyodbc

# The data layer of an N-tier architecture.
# A Database class that includes methods for fetching a list
# of shows from the IMDB database, and for finding the distinct genres
# and types of shows from the IMDB database. These methods are class methods
# so that they can share a single reusable connection to the database.
class Database:
    _connection = None
    ALL_GENRES = "-- All Genres --"
    ALL_TYPES = "-- All Types --"

    # Connect to the database using the CIS 275 student account.
    @classmethod
    def connect(cls):
        if cls._connection == None:
            server = 'tcp:cisdbss.pcc.edu'
            database = 'IMDB'
            username = '275student'
            password = '275student'
            cls._connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database
                + ';UID=' + username + ';PWD=' + password)

    # Fetch the most popular shows from the IMDB given a particular genre and type of show,
    # where at least a certain number of IMDB users have rated that show.
    # This works by building a slightly different query string depending on which options have
    # been selected by the user. Here's the query for both genre and type selected:
    #
    #     SELECT TOP 50 TB1.tconst, primaryTitle, RTRIM(titleType) AS titleType, startYear, averageRating, numVotes
    #     FROM title_basics AS TB1
    #     JOIN title_ratings AS TR ON TB1.tconst = TR.tconst
    #     JOIN title_genre AS TG ON TB1.tconst = TG.tconst
    #     WHERE TR.numVotes >= ?
    #     AND TG.genre = ?
    #     AND TB1.titleType = ?
    #     ORDER BY TR.averageRating DESC;
    #
    # Results from the database are wrapped in a list of Show objects.
    @classmethod
    def fetch_popular_shows(cls, genre, type, min_votes):
        from Show import Show

        # print("Fetching:", genre, type, min_votes)
        sql = '''
        SELECT TOP 50 TB1.tconst, primaryTitle, RTRIM(titleType) AS titleType, startYear, averageRating, numVotes
        FROM title_basics AS TB1
        JOIN title_ratings AS TR ON TB1.tconst = TR.tconst
        '''
        if genre != cls.ALL_GENRES:
            sql += '''
            JOIN title_genre AS TG ON TB1.tconst = TG.tconst
            '''
        sql += '''
        WHERE TR.numVotes >= ?
        '''
        if genre != cls.ALL_GENRES:
            sql += '''
            AND TG.genre = ?
            '''
        if type != cls.ALL_TYPES:
            sql += '''
            AND TB1.titleType = ?
            '''
        sql += '''
        ORDER BY TR.averageRating DESC;
        '''
        cls.connect()
        cursor = cls._connection.cursor()
        if genre != cls.ALL_GENRES and type != cls.ALL_TYPES:
            cursor.execute(sql, min_votes, genre, type)
        elif type != cls.ALL_TYPES:
            cursor.execute(sql, min_votes, type)
        elif genre != cls.ALL_GENRES:
            cursor.execute(sql, min_votes, genre)
        else:
            cursor.execute(sql, min_votes)
        shows = []
        show = cursor.fetchone()
        while show:
            shows.append(Show(show[0], show[1], show[2], show[3], show[4], show[5]))
            show = cursor.fetchone()
        return shows

    # Fetch the distinct genres from the IMDB database.
    @classmethod
    def fetch_genres(cls):
        sql = '''
        SELECT DISTINCT genre
        FROM title_genre;
        '''
        cls.connect()
        cursor = cls._connection.cursor()
        cursor.execute(sql)
        genres = []
        genre = cursor.fetchone()
        while genre:
            genres.append(genre[0])
            genre = cursor.fetchone()
        return genres

    # Fetch the distinct types of shows from the IMDB database.
    @classmethod
    def fetch_types(cls):
        sql = '''
        SELECT DISTINCT titleType
        FROM title_basics;
        '''
        cls.connect()
        cursor = cls._connection.cursor()
        cursor.execute(sql)
        types = []
        type = cursor.fetchone()
        while type:
            types.append(type[0])
            type = cursor.fetchone()
        return types
