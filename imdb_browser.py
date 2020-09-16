import os
import pygubu
# Next two imports are required for pyinstaller to work properly.
from pygubu.builder import ttkstdwidgets
from pygubu.builder.widgets import scrollbarhelper
import tkinter as tk
from Database import Database
from Show import *
import webbrowser

class ShowBrowserApp:
    PROJECT_PATH = os.path.dirname(__file__)
    PROJECT_UI = os.path.join(PROJECT_PATH, "imdb_browser.ui")

    # Setup the app
    def __init__(self, master):
        self.load_ui()
        self.setup_treeview()
        self.setup_genres()
        self.setup_types()
        self.fetch_data()

    # Load the User Interface from the imdb_browser.ui file and store references to the
    # widgets that we'll need later on as properties of the app class.
    def load_ui(self):
        self._builder = builder = pygubu.Builder()
        builder.add_resource_path(ShowBrowserApp.PROJECT_PATH)
        builder.add_from_file(ShowBrowserApp.PROJECT_UI)
        self._mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)

        self._tree = self._builder.get_object('table_view')
        self._genre_combo = self._builder.get_object('genre_combo')
        self._type_combo = self._builder.get_object('type_combo')
        self._min_votes_entry = self._builder.get_object('min_votes_entry')
        self._show_imdb_button = self._builder.get_object('show_imdb_button')

    # Setup the treeview widget to display information about shows from IMDB.
    def setup_treeview(self):
        tree = self._tree
        self.create_treeview_style()
        tree.configure(columns = (0, 1, 2, 3, 4, 5), displaycolumns = (1, 2, 3, 4, 5), style="Custom.Treeview")

        tree.heading(1, text="Title", anchor=tk.W)
        tree.heading(2, text="Type")
        tree.heading(3, text="Year")
        tree.heading(4, text="Rating")
        tree.heading(5, text="Num Votes")

        tree.column(1, width=250)
        tree.column(2, anchor=tk.CENTER, width=100)
        tree.column(3, anchor=tk.CENTER, width=100)
        tree.column(4, anchor=tk.CENTER, width=100)
        tree.column(5, anchor=tk.CENTER, width=100)

        tree.tag_configure('odd', background='#ccffff')

    # Setup the genres combobox so that the user can select which genre to browse.
    def setup_genres(self):
        self._genre_combo['values'] = [ShowGenre.ALL_GENRES] + [x.get_genre() for x in Database.fetch_genres()]
        self._genre_combo.current(0)

    # Setup the types combobox so that the user can select which types of shows to browse.
    def setup_types(self):
        self._type_combo['values'] = [ShowType.ALL_TYPES] + [x.get_type() for x in Database.fetch_types()]
        self._type_combo.current(0)

    # The user selected a new genre.
    def genre_changed(self, event):
        # print("New Genre: " + self._genre_combo.get())
        self.fetch_data()

    # The user selected a new type of show.
    def type_changed(self, event):
        # print("New Type: " + self._type_combo.get())
        self.fetch_data()

    # The data includes the number of IMDB users who rated a particular show. Shows with
    # more ratings tend to have more reliable ratings. The user has changed the minimum
    # number of ratings that a particular show must have before it appears in the list.
    # Shows with more ratings aren't necessarily better than shows with fewer ratings, but
    # you are less likely to get weird results if you ignore shows with fewer ratings.
    def min_votes_changed(self, event):
        # print("Min votes: " + self._min_votes_entry.get())
        self.fetch_data()

    # Convert a Show object to a tuple of values.
    @staticmethod
    def show_to_tuple(show):
        return (
            show.get_id(),
            show.get_title(),
            show.get_type(),
            show.get_year(),
            show.get_rating(),
            show.get_num_votes()
        )

    # Fetch a list of Shows from the database and display them in the treeview.
    def fetch_data(self):
        for i in self._tree.get_children():
            self._tree.delete(i)
        self._show_imdb_button['state'] = tk.DISABLED
        genre = self._genre_combo.get()
        type = self._type_combo.get()
        try:
            min_votes = int(self._min_votes_entry.get())
        except:
            min_votes = 1000
        if min_votes < 1000:
            min_votes = 1000
        # print("Fetching:", genre, type, min_votes)
        data = Show.fetch_popular_shows(genre, type, min_votes)
        for i in range(len(data)):
            val = data[i]
            self._tree.insert('', 'end', values=ShowBrowserApp.show_to_tuple(val), tag='odd' if (i % 2) else 'even')

    # The user clicked on a show in the treeview. Enable the "Show IMDB Page" button.
    def show_selected(self, event):
        focus = self._tree.focus()
        # print(focus)
        self._show_imdb_button['state'] = tk.NORMAL
        # print("Show selected:", self._tree.item(focus))


    # Fix bug in alternating colors in Treeview for later versions of tkinter
    @staticmethod
    def fixed_map(option, style):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]

    # Set up a custom style for the treeview so that it looks a little more attractive.
    # The code will work fine without this, but the UI will look a little bland.
    def create_treeview_style(self):
        style = tk.ttk.Style()

        # fix for bug in alternating colors in Treeview in later versions of tkinter
        # see https://bugs.python.org/issue36468 for details
        style.map('Treeview', foreground=ShowBrowserApp.fixed_map('foreground', style),
                  background=ShowBrowserApp.fixed_map('background', style))

        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.configure("Custom.Treeview.Heading",
                        background="dark blue", foreground="white", relief="flat", font=('Arial Black', 10, 'bold'))
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])
        return style

    # The user clicked the Show IMDB Page button. Launch that page in the default browser.
    def show_imdb_page(self):
        selected_item = self._tree.item(self._tree.focus())
        print(selected_item)
        webbrowser.open('https://imdb.com/title/' + selected_item['values'][0])

    def run(self):
        self._mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("IMDB Popular Show Browser")
    root.tk.call('info', 'patchlevel')
    app = ShowBrowserApp(root)
    app.run()

