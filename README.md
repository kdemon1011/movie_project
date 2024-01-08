# Prerequisites

- Python3

- Create and activate virtual env

  ```bash
  sudo apt-get install python-virtualenv
  python3 -m venv env
  source env/bin/activate
  ```

- Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

# Fetch Movies

- Run the following command to fetch top 250 movies from the IMDB website. The data will be stored into **utils/disha_movies.csv** file

  ```bash
  python fetch_movies.py
  ```
