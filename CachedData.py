class CachedData:
    @staticmethod
    def fetch_genres():
        from Show import ShowGenre

        return [
            ShowGenre("Action"),
            ShowGenre("Adult"),
            ShowGenre("Adventure"),
            ShowGenre("Animation"),
            ShowGenre("Biography"),
            ShowGenre("Comedy"),
            ShowGenre("Crime"),
            ShowGenre("Documentary"),
            ShowGenre("Drama"),
            ShowGenre("Family"),
            ShowGenre("Fantasy"),
            ShowGenre("Film-Noir"),
            ShowGenre("Game-Show"),
            ShowGenre("History"),
            ShowGenre("Horror"),
            ShowGenre("Music"),
            ShowGenre("Musical"),
            ShowGenre("Mystery"),
            ShowGenre("News"),
            ShowGenre("Reality-TV"),
            ShowGenre("Romance"),
            ShowGenre("Sci-Fi"),
            ShowGenre("Short"),
            ShowGenre("Sport"),
            ShowGenre("Talk-Show"),
            ShowGenre("Thriller"),
            ShowGenre("War"),
            ShowGenre("Western")
        ]

    @staticmethod
    def fetch_types():
        from Show import ShowType

        return [
            ShowType("movie"),
            ShowType("short"),
            ShowType("tvEpisode"),
            ShowType("tvMiniSeries"),
            ShowType("tvMovie"),
            ShowType("tvSeries"),
            ShowType("tvShort"),
            ShowType("tvSpecial"),
            ShowType("video"),
            ShowType("videoGame")
        ]