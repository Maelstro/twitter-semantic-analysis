# Maciej Wójcik - Twitter crawler based on Twitter API v2

class TweetQuery:
    """Class defining a Twitter API query"""
    def __init__(self):
        self._text_query = None
        self._author_username = None
        self._mentioned_user = None
        self._exact_match = None
        self._hashtag = None
        self._to_user = None
        self._contains_url = None
        self._max_results = None

    @property
    def text_query(self):
        return self._text_query

    @text_query.setter
    def text_query(self, value: str):
        self._text_query = value

    @property
    def author_username(self):
        return self._author_username

    @author_username.setter
    def author_username(self, value: str):
        self._author_username = 'from:' + value

    @property
    def mentioned_user(self):
        return self._mentioned_user

    @mentioned_user.setter
    def mentioned_user(self, value: str):
        self._mentioned_user = '@' + value

    @property
    def exact_match(self):
        return self._exact_match

    @exact_match.setter
    def exact_match(self, value: str):
        self._exact_match = '"' + value + "'"

    @property
    def hashtag(self):
        return self._hashtag

    @hashtag.setter
    def hashtag(self, value: str):
        self._hashtag = '#' + value

    @property
    def to_user(self):
        return self._to_user

    @to_user.setter
    def to_user(self, value: str):
        self._to_user = 'to:' + value

    @property
    def contains_url(self):
        return self._contains_url

    @contains_url.setter
    def contains_url(self, value: str):
        self._contains_url = 'url:' + value

    @property
    def max_results(self):
        return self._max_results

    @max_results.setter
    def max_results(self, value: int):
        if value >= 100:
            self._max_results = 100
        elif value <= 10:
            self._max_results = 10
        else:
            self._max_results = value





