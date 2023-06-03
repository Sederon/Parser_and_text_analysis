from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QListWidgetItem
import pandas as pd

from ui_mainwindow import Ui_MainWindow
from tools.TextProcessModule import TextProcessing
from tools.ParseToolAPI import ParseToolAPI

class MainWindow(QMainWindow):
    """
    Current class describe application main window
    """

    def __init__(self):
        super(MainWindow, self).__init__()  # call parent constructor

        # initialize all UI elements.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Bind button events.
        self.ui.list_view_sub.clicked.connect(self.sub_item_clicked)
        self.ui.list_view_flair.clicked.connect(self.flair_item_clicked)
        self.ui.list_view_post.clicked.connect(self.post_item_clicked)
        self.ui.load_data_button.clicked.connect(self.load_data_button_clicked)

        # Variables.
        self.Data = pd.DataFrame()
        self.current_sub = pd.DataFrame()

        # Create instance of Plot class and pass plot widget to it
    # ------- UI EVENTS --------------------------------------------------------------------------------------------- #

    def load_data_button_clicked(self):
        parse = ParseToolAPI()
        self.Data = parse.return_result()
        topics = ["Discussion", "World_news", "Music"]
        self.list_view_content_change(self.ui.list_view_sub, topics)

    def sub_item_clicked(self, item):
        sub = item.text()
        if sub == "Discussion":
            df = self.Data[0]
            self.current_sub = df
            topics = self.df['flair'].unique().tolist()
            self.list_view_content_change(self.ui.list_view_flair, topics)
            self.list_view_content_change(self.ui.list_view_post, df[df['flair'] == topics[0]]['title'].tolist())
        elif sub == "World_news":
            df = self.Data[1]
            self.current_sub = df
            topics = self.df['flair'].unique().tolist()
            self.list_view_content_change(self.ui.list_view_flair, topics)
            self.list_view_content_change(self.ui.list_view_post, df[df['flair'] == topics[0]]['title'].tolist())
        elif sub == "Music":
            df = self.Data[2]
            self.current_sub = df
            topics = self.df['flair'].unique().tolist()
            self.list_view_content_change(self.ui.list_view_flair, topics)
            self.list_view_content_change(self.ui.list_view_post, df[df['flair'] == topics[0]]['title'].tolist())

    def flair_item_clicked(self, item):
        flair = item.text()
        df = self.current_sub
        self.list_view_content_change(self.ui.list_view_post, df[df['flair'] == flair]['title'].tolist())

    def post_item_clicked(self, item):
        list_view = self.sender()
        row = list_view.currentRow()
        df = self.current_sub
        self.ui.text_content.setText(df.loc[row, 'content'])

    def list_view_content_change(self, list_view, topics):
        model = QStringListModel()

        # Set the model on the list view
        list_view.setModel(model)

        # Populate the list view with items
        model.setStringList(topics)
