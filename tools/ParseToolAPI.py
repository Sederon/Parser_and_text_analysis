import praw

from tools.DatabaseOperate import DataBase


class ParseToolAPI:
    def __init__(self):
        CLIENT_ID = "I57YvYdCsFcYO4IEB0ffVg"
        CLIENT_SECRET = "TTaTRzJkhNKefupPUPhPUpf9eYWb-A"
        USER_AGENT = "ResolutionSad1131"
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
        )

        subreddit = reddit.subreddit('Discussion')
        for index, submission in enumerate(subreddit.new(limit=12), start=1):
            if index > 2:
                text = submission.selftext
                title = submission.title
                flair = submission.link_flair_text
                print((title, flair, text))
