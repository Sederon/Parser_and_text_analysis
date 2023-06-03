from tools.TextProcessModule import TextProcessing
from tools.ParseToolAPI import ParseToolAPI

def read_text(file_path):
    with open(file_path, "r") as file:
        return file.read()


# # Example text
# text = read_text("Text\\bbc_news1.txt")
# sum_method = 1  # 0 for cosine method, 1 - LexRank method, 2 - LSA, 3 - Luhn
# text_proc = TextProcessing(text, sum_method)
# text_proc.print_result()

parse = ParseToolAPI()
data = parse.return_result()
# print(data[0][['title', 'flair']])
# print(data[0][data[0]['flair'] == 'Political'][['title', 'flair']])

