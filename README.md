# Movie Recommendation System 🚀

A Python desktop app built with Tkinter that recommends **4 movies** based on a movie you search for. It uses TF-IDF vectorization and cosine similarity on movie metadata to find similar movies.

---

## Features

- Search a movie by name.
- Get **4** recommended movies based on your input.
- Movie details include title, overview, director, and ratings.
- Click movie titles to open their homepage or Google search page if homepage is missing.
- The app launches in **fullscreen** mode by default.
- Background image for a better user experience.

---

## Technologies Used

- Python 3.x
- Tkinter (GUI)
- pandas, numpy
- scikit-learn (TF-IDF, cosine similarity)
- difflib (movie title matching)
- Pillow (image handling)

---

## How to Run

1. Install Python 3.x if not installed.

2. Install required packages:

```bash
pip install pandas numpy scikit-learn pillow
