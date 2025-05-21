from tkinter import *
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import webbrowser
from PIL import Image, ImageTk  # For handling background image (JPG)

# Loading the data from the csv file to a pandas dataframe
movies_data = pd.read_csv('movies.csv')

selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

# Convert text to vector value
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Checks for similarity
similarity = cosine_similarity(feature_vectors)

mshow_features = movies_data[['title', 'genres', 'overview', 'director', 'vote_average', 'homepage']].copy()

fd = {
    'title': [],
    'genres': [],
    'overview': [],
    'director': [],
    'vote_average': [],
    'homepage': [],
}
fdf = pd.DataFrame(fd)

def para(inp):
    new_input = ""
    for i, letter in enumerate(inp):
        if i % 70 == 0:
            new_input += '\n'
        new_input += letter
    new_input = new_input[1:]
    return new_input

def linkcheck(link, title):
    if link == 'nan':
        tlink = title
        tlink = tlink.replace(' ', '+')
        link = "https://www.google.com/search?q=" + tlink + "+movie"
    return link

def create_search_window():
    global search, mv, name, bg_image
    search = Tk()
    search.geometry("2560x1440")
    search.title("Movie Recommendation System")
    search.attributes('-fullscreen', True)

    # Load and set background image
    try:
        image = Image.open("images/background.jpg")  # Replace with your image name
        image = image.resize((search.winfo_screenwidth(), search.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        bg_label = Label(search, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image 'background.jpg' not found. Using default background color.")
        bg_frame = Frame(search, bg="#2C3E50")
        bg_frame.place(relwidth=1, relheight=1)
        bg_label = Label(bg_frame, bg="#34495E", borderwidth=0)
        bg_label.place(relwidth=1, relheight=1)

    mrs = Label(search, text="Movie Recommendation System", font=("Calibri", 35), bg="#34495E", fg="#ECF0F1").place(relx=0.5, rely=0.2, anchor=CENTER)

    def temp_text(e):
        name.delete(0, "end")

    # Styled Frame for search bar
    namebg = Frame(search, bg="#ECF0F1", bd=2, relief="groove", highlightbackground="#BDC3C7", highlightthickness=2)
    namebg.place(relx=0.5, rely=0.4, anchor=CENTER, width=800, height=70)
    mv = StringVar()
    name = Entry(namebg, textvariable=mv, font=("Calibri", 18), bg="#ECF0F1", fg="#2C3E50", insertbackground="#2C3E50", borderwidth=0)
    name.insert(0, "Enter movie name")
    name.place(relx=0.5, rely=0.5, anchor=CENTER, width=780, height=60)
    name.bind("<FocusIn>", temp_text)
    name.bind("<Return>", lambda event: recommender())

    # Search button
    sbutton = Button(search, text="Search", font=("Calibri", 16), bg="#E74C3C", fg="white", borderwidth=0, command=recommender, activebackground="#C0392B", activeforeground="white")
    sbutton.place(relx=0.45, rely=0.5, anchor=CENTER, width=120, height=50)

    # Quit button
    qbutton = Button(search, text="Quit", font=("Calibri", 16), bg="#E74C3C", fg="white", borderwidth=0, command=search.destroy, activebackground="#C0392B", activeforeground="white")
    qbutton.place(relx=0.55, rely=0.5, anchor=CENTER, width=120, height=50)

def recommender():
    global top_30, sresult
    top_30 = []
    movie_name = mv.get()
    list_of_all_titles = movies_data['title'].tolist()

    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    close_match = find_close_match[0]

    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    print('Movies suggested for you : \n')

    i = 1

    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['title'].values[0]
        if (i < 30):
            top_30.append(title_from_index)
            i += 1
    print(top_30)
    search.destroy()
    moviedata(top_30)
    show_results()

def moviedata(movie):
    global fdf
    fdf = pd.DataFrame(fd)  # Reset fdf to clear previous results
    for m in movie:
        for i, title in enumerate(mshow_features['title']):
            if title == m:
                x = i
                fdf.loc[mshow_features.index[x]] = mshow_features.iloc[x]
    nrows = fdf.shape[0]
    number = list(range(1, nrows + 1))
    fdf['number'] = number
    fdf.set_index('number', inplace=True)
    print(fdf)

def quitter():
    sresult.destroy()
    create_search_window()  # Reopen the search window

def show_results():
    global sresult, bg_image_result
    sresult = Tk()
    sresult.geometry("2560x1440")
    sresult.title("Movie Recommendation System")
    sresult.attributes('-fullscreen', True)

    # Load and set background image
    try:
        image = Image.open("images/background.jpg")  # Replace with your image name
        image = image.resize((sresult.winfo_screenwidth(), sresult.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_image_result = ImageTk.PhotoImage(image)
        bg_label = Label(sresult, image=bg_image_result)
        bg_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image 'background.jpg' not found. Using default background color.")
        bg_frame_result = Frame(sresult, bg="#2C3E50")
        bg_frame_result.place(relwidth=1, relheight=1)
        bg_label_result = Label(bg_frame_result, bg="#34495E", borderwidth=0)
        bg_label_result.place(relwidth=1, relheight=1)

    accent_color = "#E74C3C"
    dname1 = str(fdf['director'][1])
    dname2 = str(fdf['director'][2])
    dname3 = str(fdf['director'][3])
    dname4 = str(fdf['director'][4])
    rate1 = str(fdf['vote_average'][1])
    rate2 = str(fdf['vote_average'][2])
    rate3 = str(fdf['vote_average'][3])
    rate4 = str(fdf['vote_average'][4])
    bgc = "#34495E"
    textbg = "#3498DB"
    titlefont = ("Calibri", 28)
    ovfont = ('Calibri', 16, 'bold')

    # Movie 1
    l1 = Label(sresult, text=str(fdf['title'][1]), font=titlefont, bg=bgc, fg=accent_color, cursor="hand2")
    link1 = str(fdf['homepage'][1])
    title1 = str(fdf['title'][1])
    link1 = linkcheck(link1, title1)
    l1.bind('<Button-1>', lambda x: webbrowser.open_new(link1))
    l1.place(x=200, y=50)
    ovbgcl = Frame(sresult, bg="#D5DBDB", bd=2, relief="groove")
    ovbgcl.place(x=170, y=100, width=550, height=140)
    d1 = Text(sresult, font=ovfont, bg=textbg, fg="white", height=5, width=60, borderwidth=0)
    d1.insert(1.0, str(fdf['overview'][1]))
    d1.config(state=DISABLED)
    d1.place(x=180, y=110)
    drc1 = Frame(sresult, bg="#E57373", bd=2, relief="groove")
    drc1.place(x=180, y=260, width=550, height=60)
    director = Label(sresult, text="Director: ", font=ovfont, bg="#E57373", fg='white').place(x=190, y=270)
    director_name = Label(sresult, text=dname1, font=ovfont, bg="#E57373", fg='white').place(x=280, y=270)
    rating = Label(sresult, text="Rating: ", font=ovfont, bg="#E57373", fg='white').place(x=190, y=300)
    rate_name = Label(sresult, text=rate1, font=ovfont, bg="#E57373", fg='white').place(x=260, y=300)

    # Movie 2
    l2 = Label(sresult, text=str(fdf['title'][2]), font=titlefont, bg=bgc, fg=accent_color, cursor="hand2")
    link2 = str(fdf['homepage'][2])
    title2 = str(fdf['title'][2])
    link2 = linkcheck(link2, title2)
    l2.bind('<Button-1>', lambda x: webbrowser.open_new(link2))
    l2.place(x=200, y=400)
    ovbgc2 = Frame(sresult, bg="#D5DBDB", bd=2, relief="groove")
    ovbgc2.place(x=170, y=450, width=550, height=140)
    d2 = Text(sresult, font=ovfont, bg=textbg, fg="white", height=5, width=60, borderwidth=0)
    d2.insert(1.0, str(fdf['overview'][2]))
    d2.config(state=DISABLED)
    d2.place(x=180, y=460)
    drc2 = Frame(sresult, bg="#E57373", bd=2, relief="groove")
    drc2.place(x=180, y=610, width=550, height=60)
    director = Label(sresult, text="Director: ", font=ovfont, bg="#E57373", fg='white').place(x=190, y=620)
    director_name = Label(sresult, text=dname2, font=ovfont, bg="#E57373", fg='white').place(x=280, y=620)
    rating = Label(sresult, text="Rating: ", font=ovfont, bg="#E57373", fg='white').place(x=190, y=650)
    rate_name = Label(sresult, text=rate2, font=ovfont, bg="#E57373", fg='white').place(x=260, y=650)

    # Movie 3
    l3 = Label(sresult, text=str(fdf['title'][3]), font=titlefont, bg=bgc, fg=accent_color, cursor="hand2")
    link3 = str(fdf['homepage'][3])
    title3 = str(fdf['title'][3])
    link3 = linkcheck(link3, title3)
    l3.bind('<Button-1>', lambda x: webbrowser.open_new(link3))
    l3.place(x=800, y=50)
    ovbgc3 = Frame(sresult, bg="#D5DBDB", bd=2, relief="groove")
    ovbgc3.place(x=770, y=100, width=550, height=140)
    d3 = Text(sresult, font=ovfont, bg=textbg, fg="white", height=5, width=60, borderwidth=0)
    d3.insert(1.0, str(fdf['overview'][3]))
    d3.config(state=DISABLED)
    d3.place(x=780, y=110)
    drc3 = Frame(sresult, bg="#E57373", bd=2, relief="groove")
    drc3.place(x=780, y=260, width=550, height=60)
    director = Label(sresult, text="Director: ", font=ovfont, bg="#E57373", fg='white').place(x=790, y=270)
    director_name = Label(sresult, text=dname3, font=ovfont, bg="#E57373", fg='white').place(x=880, y=270)
    rating = Label(sresult, text="Rating: ", font=ovfont, bg="#E57373", fg='white').place(x=790, y=300)
    rate_name = Label(sresult, text=rate3, font=ovfont, bg="#E57373", fg='white').place(x=860, y=300)

    # Movie 4
    l4 = Label(sresult, text=str(fdf['title'][4]), font=titlefont, bg=bgc, fg=accent_color, cursor="hand2")
    link4 = str(fdf['homepage'][4])
    title4 = str(fdf['title'][4])
    link4 = linkcheck(link4, title4)
    l4.bind('<Button-1>', lambda x: webbrowser.open_new(link4))
    l4.place(x=800, y=400)
    ovbgc4 = Frame(sresult, bg="#D5DBDB", bd=2, relief="groove")
    ovbgc4.place(x=770, y=450, width=550, height=140)
    d4 = Text(sresult, font=ovfont, bg=textbg, fg="white", height=5, width=60, borderwidth=0)
    d4.insert(1.0, str(fdf['overview'][4]))
    d4.config(state=DISABLED)
    d4.place(x=780, y=460)
    drc4 = Frame(sresult, bg="#E57373", bd=2, relief="groove")
    drc4.place(x=780, y=610, width=550, height=60)
    director = Label(sresult, text="Director: ", font=ovfont, bg="#E57373", fg='white').place(x=790, y=620)
    director_name = Label(sresult, text=dname4, font=ovfont, bg="#E57373", fg='white').place(x=880, y=620)
    rating = Label(sresult, text="Rating: ", font=ovfont, bg="#E57373", fg='white').place(x=790, y=650)
    rate_name = Label(sresult, text=rate4, font=ovfont, bg="#E57373", fg='white').place(x=860, y=650)

    # Back button
    back_button = Button(sresult, text="Back", font=("Calibri", 16), bg="#E74C3C", fg="white", borderwidth=0, command=quitter, activebackground="#C0392B", activeforeground="white")
    back_button.place(relx=0.5, rely=0.9, anchor=CENTER, width=120, height=50)

# Initialize the first search window
create_search_window()
search.mainloop()