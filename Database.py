import pyodbc


# The data layer of an N-tier architecture.
# A Database class that includes methods for fetching a list
# of shows from the IMDB database, and for finding the distinct genres
# and types of shows from the IMDB database. These methods are class methods
# so that they can share a single reusable connection to the database.
class Database:
    __connection = None

    # Connect to the database using the CIS 275 student account.
    @classmethod
    def connect(cls):
        if cls.__connection is None:
            server = 'tcp:cisdbss.pcc.edu'
            database = 'IMDB'
            username = '275student'
            password = '275student'
            cls.__connection = pyodbc.connect(
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
    def fetch_popular_shows(cls, genre, show_type, min_votes):
        from Show import Show, ShowGenre, ShowType

        # print("Fetching:", genre, type, min_votes)
        sql = '''
        SELECT TOP 50 TB1.tconst, primaryTitle, RTRIM(titleType) AS titleType, startYear, averageRating, numVotes
        FROM title_basics AS TB1
        JOIN title_ratings AS TR ON TB1.tconst = TR.tconst
        '''
        if genre != ShowGenre.ALL_GENRES:
            sql += '''
            JOIN title_genre AS TG ON TB1.tconst = TG.tconst
            '''
        sql += '''
        WHERE TR.numVotes >= ?
        '''
        if genre != ShowGenre.ALL_GENRES:
            sql += '''
            AND TG.genre = ?
            '''
        if show_type != ShowType.ALL_TYPES:
            sql += '''
            AND TB1.titleType = ?
            '''
        sql += '''
        ORDER BY TR.averageRating DESC;
        '''
        cls.connect()
        cursor = cls.__connection.cursor()
        if genre != ShowGenre.ALL_GENRES and show_type != ShowType.ALL_TYPES:
            cursor.execute(sql, min_votes, genre, show_type)
        elif show_type != ShowType.ALL_TYPES:
            cursor.execute(sql, min_votes, show_type)
        elif genre != ShowGenre.ALL_GENRES:
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
        from Show import ShowGenre
        sql = '''
        SELECT DISTINCT genre
        FROM title_genre;
        '''
        cls.connect()
        cursor = cls.__connection.cursor()
        cursor.execute(sql)
        genres = []
        genre = cursor.fetchone()
        while genre:
            genres.append(ShowGenre(genre[0]))
            genre = cursor.fetchone()
        return genres

    # Fetch the distinct types of shows from the IMDB database.
    @classmethod
    def fetch_types(cls):
        from Show import ShowType
        sql = '''
        SELECT DISTINCT titleType
        FROM title_basics;
        '''
        cls.connect()
        cursor = cls.__connection.cursor()
        cursor.execute(sql)
        types = []
        show_type = cursor.fetchone()
        while show_type:
            types.append(ShowType(show_type[0]))
            show_type = cursor.fetchone()
        return types
