# Movie Suggester Application

## Project Overview

This project is a Python-based desktop application that suggests top-rated movies to watch based on the genre selected by the user. The app fetches movie data dynamically by scraping IMDb's website and also caches the results locally in a CSV file for faster subsequent lookups. Additionally, the app randomly recommends one movie at the top of the list to help users decide what to watch today.

The application features a simple graphical user interface (GUI) built with Tkinter, allowing easy genre selection and displaying the movie list along with ratings.

---

## Features

- Scrapes top 20 highly rated movies for a selected genre from IMDb.
- Caches movie data locally in a CSV file (`movies.csv`) to avoid repeated web scraping.
- Displays the movie list with their IMDb ratings.
- Randomly highlights one movie recommendation from the list.
- User-friendly GUI for seamless interaction.

---

## Technologies and Libraries Used

- **Python 3.x** — programming language used for the application.
- **Requests** — for making HTTP requests to IMDb.
- **BeautifulSoup4** — for parsing HTML content and extracting movie details.
- **Pandas** — for handling CSV file operations and data manipulation.
- **Tkinter** — Python's standard GUI library for building the desktop interface.
- **Random (standard library)** — to select a random movie recommendation.
- **OS (standard library)** — for handling file system operations.

---

## Installation and Setup

1. **Clone or download the repository to your local machine.**

2. **Install required Python packages:**

   Make sure you have Python 3 installed. Then install the dependencies using pip:

   ```bash
   pip install requests beautifulsoup4 pandas

Run the application:

## Run the application

```bash
python movie_suggester_final.py

## Usage

- Launch the application; a window will open with a dropdown menu listing available genres.  
- Select a genre from the dropdown (e.g., Action, Comedy, Drama).  
- Click the **"Get Movies"** button.  
- The application will either load cached movie data from the CSV or scrape fresh data from IMDb if not available.  
- A random movie recommendation will be displayed at the top followed by the top 20 movies in the selected genre with their IMDb ratings.  

## Code Structure

- **MovieSuggester Class:**  
  Handles scraping IMDb, loading and saving movie data to CSV, and managing the cache.

- **MovieSuggesterApp Class:**  
  Implements the GUI using Tkinter, handles user input, and displays movie recommendations.

- **Main Execution:**  
  Initializes the Tkinter root window and launches the app.

## Notes

- The app requires an active internet connection for initial data scraping.  
- Cached data reduces load times on subsequent queries for the same genre.  
- The CSV file `movies.csv` is stored in the same directory as the script.

## Author

This project was developed by Pavithra.
