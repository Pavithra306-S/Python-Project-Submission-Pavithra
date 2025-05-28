import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class MovieSuggester:
    def __init__(self, csv_file='movies.csv'):
        self.base_url = "https://www.imdb.com/search/title/"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        self.csv_file = csv_file

    def load_movies_from_csv(self, genre):
        if not os.path.exists(self.csv_file):
            return None
        try:
            if os.path.getsize(self.csv_file) == 0:
                # Empty file, treat as no data
                return None
            
            df = pd.read_csv(self.csv_file)
            if df.empty or 'Genre' not in df.columns:
                return None
            
            genre_filtered = df[df['Genre'].str.lower() == genre.lower()]
            if not genre_filtered.empty:
                return genre_filtered[['Title', 'Rating']].to_dict(orient='records')
            else:
                return None
        except pd.errors.EmptyDataError:
            print("CSV file is empty or has no columns.")
            return None
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None

    def save_movies_to_csv(self, movies, genre):
        for movie in movies:
            movie['Genre'] = genre

        try:
            if not os.path.exists(self.csv_file) or os.path.getsize(self.csv_file) == 0:
                # File doesn't exist or is empty, create fresh with headers
                df_new = pd.DataFrame(movies)
                df_new.to_csv(self.csv_file, index=False)
            else:
                df_existing = pd.read_csv(self.csv_file)
                df_new = pd.DataFrame(movies)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.drop_duplicates(subset=['Title', 'Genre'], inplace=True)
                df_combined.to_csv(self.csv_file, index=False)
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def scrape_movies_by_genre(self, genre):
        movies = self.load_movies_from_csv(genre)
        if movies is not None:
            print(f"Loaded {len(movies)} movies for genre '{genre}' from CSV.")
            return movies

        try:
            url = (
                f"{self.base_url}?genres={genre.lower()}"
                f"&sort=user_rating,desc&title_type=feature&num_votes=10000,&count=20"
            )
            print(f"Fetching URL: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find movie title divs
            title_divs = soup.find_all('div', class_=lambda c: c and 'dli-title' in c)
            print(f"Found {len(title_divs)} movie title divs.")

            movies = []
            for title_div in title_divs:
                h3_tag = title_div.find('h3', class_='ipc-title__text')
                title = h3_tag.text.strip() if h3_tag else 'N/A'

                rating = 'N/A'
                parent = title_div.parent
                if parent:
                    rating_div = parent.find('div', class_=lambda c: c and 'dli-ratings-container' in c)
                    if rating_div:
                        rating_span = rating_div.find('span', class_='ipc-rating-star--rating')
                        if rating_span and rating_span.text.strip():
                            rating = rating_span.text.strip()

                if title != 'N/A':
                    movies.append({'Title': title, 'Rating': rating})

            if movies:
                self.save_movies_to_csv(movies, genre)

            return movies

        except requests.RequestException as e:
            print(f"Network error during scraping: {e}")
            return None
        except Exception as e:
            print(f"Error during scraping: {e}")
            return None


class MovieSuggesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Suggester")
        self.suggester = MovieSuggester()

        self.genres = [
            'action', 'comedy', 'drama', 'horror', 'thriller', 'sci-fi', 'romance', 'animation', 'adventure'
        ]

        # Dropdown
        self.genre_label = ttk.Label(root, text="Select Genre:")
        self.genre_label.pack(pady=5)

        self.genre_var = tk.StringVar(value=self.genres[0])
        self.genre_dropdown = ttk.Combobox(root, textvariable=self.genre_var, values=self.genres, state='readonly')
        self.genre_dropdown.pack(pady=5)

        # Button
        self.search_button = ttk.Button(root, text="Get Movies", command=self.get_movies)
        self.search_button.pack(pady=5)

        # Results box
        self.result_box = scrolledtext.ScrolledText(root, width=60, height=20)
        self.result_box.pack(pady=10)

    def get_movies(self):
        genre = self.genre_var.get()
        self.result_box.delete('1.0', tk.END)
        self.result_box.insert(tk.END, f"Fetching movies for genre: {genre}...\n")
        self.root.update()

        movies = self.suggester.scrape_movies_by_genre(genre)
        if movies:
            random_movie = random.choice(movies)
            self.result_box.delete('1.0', tk.END)
            self.result_box.insert(
                tk.END, 
                f"You can watch this movie today: {random_movie['Title']} (Rating: {random_movie['Rating']})\n\n"
            )
            self.result_box.insert(tk.END, f"Top {len(movies)} {genre.capitalize()} Movies:\n\n")
            for i, movie in enumerate(movies, 1):
                self.result_box.insert(tk.END, f"{i}. {movie['Title']} (Rating: {movie['Rating']})\n")
        else:
            messagebox.showerror("Error", "No movies found or an error occurred.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieSuggesterApp(root)
    root.mainloop()
