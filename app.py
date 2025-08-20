from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# In-memory users and books for demonstration
users = {
    "alice": "wonderland",
    "bob": "builder",
}

books = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "price": 9.99,
        "image": "https://covers.openlibrary.org/b/isbn/0451524934-L.jpg",
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "price": 12.99,
        "image": "https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg",
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "price": 10.50,
        "image": "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg",
    },
]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users.get(username) == password:
            session["username"] = username
            session.setdefault("cart", [])
            return redirect(url_for("list_books"))
        error = "Invalid credentials"
    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/books")
@login_required
def list_books():
    return render_template("books.html", books=books)


@app.post("/add/<int:book_id>")
@login_required
def add_to_cart(book_id):
    cart = session.setdefault("cart", [])
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        cart.append(book)
        session["cart"] = cart
    return redirect(url_for("list_books"))


@app.route("/cart", methods=["GET", "POST"])
@login_required
def view_cart():
    cart = session.setdefault("cart", [])
    if request.method == "POST":
        session["cart"] = []
        return render_template("cart.html", cart=[], total=0, message="Order placed successfully!")
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total, message=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
