import praw

from tools.DatabaseOperate import DataBase


class ParseToolAPI:
    def __init__(self):
        self.reddit = ''
        # self.parse()


    def write_in_db(self, page_name, number_of_records):
        db = DataBase(page_name)
        db.connect()
        subreddit = self.reddit.subreddit(page_name)

        for index, submission in enumerate(subreddit.new(limit=number_of_records+2), start=1):
            if index > 2:
                text = submission.selftext
                title = submission.title
                flair = submission.link_flair_text
                db.insert_record(title, flair, text)

        db.close()

    def read_from_db(self, page_name):
        db = DataBase(page_name)
        db.connect()
        records = db.return_records_df()
        db.close()
        return records

    def return_result(self):
        df_discuss = self.read_from_db('Discussion')
        df_worldnews = self.read_from_db('worldnews')
        df_movies = self.read_from_db('movies')

        return df_discuss, df_worldnews, df_movies

    def parse(self):
        with open("Text/cid", "r") as file:
            cid = file.readlines()
        CLIENT_ID = cid[0].strip()
        CLIENT_SECRET = cid[1].strip()
        USER_AGENT = "ResolutionSad1131"
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
        )

        # self.write_in_db('Discussion', 100)
        # self.write_in_db('worldnews', 100)
        # self.write_in_db('movies', 100)

