# Conference 2025 Bookstore

This is a very simple Flask-based bookstore demo. Users can log in, browse a list of books, add them to a cart and checkout. The application is designed for demonstration purposes only and uses in-memory data structures instead of a database.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then visit [http://localhost:5000](http://localhost:5000) in your browser and log in using one of the predefined users (e.g. `alice`/`wonderland`).

## Docker

Build the image and run the container:

```bash
docker build -t bookstore .
docker run -p 5000:5000 bookstore
```
