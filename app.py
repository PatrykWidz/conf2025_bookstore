from functools import wraps
import time
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
    {
        "id": 4,
        "title": "Observability Engineering",
        "author": "Charity Majors, Liz Fong-Jones, George Miranda",
        "price": 44.99,
        "image": "https://covers.openlibrary.org/b/isbn/9781492076643-L.jpg",
    },
    {
        "id": 5,
        "title": "Practical Monitoring",
        "author": "Mike Julian",
        "price": 34.99,
        "image": "https://covers.openlibrary.org/b/isbn/9781491957356-L.jpg",
    },
    {
        "id": 6,
        "title": "Logging and Log Management",
        "author": "Anton Chuvakin",
        "price": 49.99,
        "image": "https://covers.openlibrary.org/b/isbn/9780123749888-L.jpg",
    },
    {
        "id": 7,
        "title": "Security Engineering",
        "author": "Ross Anderson",
        "price": 59.99,
        "image": "https://covers.openlibrary.org/b/isbn/9781119642787-L.jpg",
    },
    {
        "id": 8,
        "title": "Kubernetes Security",
        "author": "Liz Rice",
        "price": 39.99,
        "image": "https://covers.openlibrary.org/b/isbn/9781492081777-L.jpg",
    },
    {
        "id": 9,
        "title": "Building Secure and Reliable Systems",
        "author": "Heather Adkins, Betsy Beyer, Paul Blankinship, et al.",
        "price": 54.99,
        "image": "https://covers.openlibrary.org/b/isbn/9781492083122-L.jpg",
    },
    {
        "id": 10,
        "title": "Web Application Security",
        "author": "Andrew Hoffman",
        "price": 45.00,
        "image": "https://covers.openlibrary.org/b/isbn/9781492053118-L.jpg",
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
        item = next((i for i in cart if i["id"] == book_id), None)
        if item:
            item["quantity"] += 1
        else:
            cart.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "price": book["price"],
                "quantity": 1,
            })
        session["cart"] = cart
    return redirect(url_for("list_books"))


@app.post("/cart/update/<int:book_id>/<action>")
@login_required
def update_cart(book_id, action):
    cart = session.setdefault("cart", [])
    item = next((i for i in cart if i["id"] == book_id), None)
    if not item:
        return redirect(url_for("view_cart"))
    if action == "increase":
        item["quantity"] += 1
    elif action == "decrease":
        item["quantity"] -= 1
        if item["quantity"] <= 0:
            cart.remove(item)
    elif action == "remove":
        cart.remove(item)
    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/cart", methods=["GET", "POST"])
@login_required
def view_cart():
    cart = session.setdefault("cart", [])
    if request.method == "POST":
        if any(item["title"] == "Observability Engineering" for item in cart):
            time.sleep(10)
            total = sum(item["price"] * item["quantity"] for item in cart)
            return render_template(
                "cart.html",
                cart=cart,
                total=total,
                message=None,
                error="Ups, something went wrong",
            )
        session["cart"] = []
        return render_template(
            "cart.html", cart=[], total=0, message="Order placed successfully!", error=None
        )
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total=total, message=None, error=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
