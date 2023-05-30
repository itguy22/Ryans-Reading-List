from dotenv import load_dotenv
import os
from flask import render_template, request, redirect, url_for, flash
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Load the .env file to get the environment variables. If you do not have a .env file, you can create one and add the environment variables there.
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@db/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = os.urandom(24)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Book {self.title}>'

    def __init__(self, title, authors, rating, review):
        self.title = title
        self.rating = rating
        self.review = review
        self.authors = authors


@app.route('/', methods=['GET', 'POST'])
def index():
    books = Book.query.all()  # Retrieve all books from database
    order = request.args.get('order', default='id')
    direction = request.args.get('direction', default='asc')

    if order == 'rating':
        if direction == 'desc':
            books = Book.query.order_by(Book.rating.desc()).all()
        else:
            books = Book.query.order_by(Book.id).all()
        if request.method == 'POST':
            title = request.form['title']
            rating = request.form['rating']
            review = request.form['review']
            book = Book(title, rating, review)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('index', order=order, direction=direction))

    return render_template('index.html', books=books, order=order, direction=direction)


@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    authors = request.form['authors']
    rating = request.form['rating']
    review = request.form['review']

    new_book = Book(title=title, authors=authors, rating=rating, review=review)
    db.session.add(new_book)
    db.session.commit()

    flash('Book added to the reading list.', 'success')
    return redirect(url_for('index'))


@app.route('/add_searched_book', methods=['POST'])
def add_searched_book():
    title = request.form['title']
    authors = request.form['authors']
    # Use a default value if not provided
    rating = request.form.get('rating', 0)
    # Use a default value if not provided
    review = request.form.get('review', '')

    new_book = Book(title=title, authors=authors, rating=rating, review=review)
    db.session.add(new_book)
    db.session.commit()

    flash('Book added to the reading list.', 'success')
    return redirect(url_for('index'))


@app.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)

    book.rating = request.form['rating']
    book.review = request.form['review']
    db.session.commit()

    flash('Book updated successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/update_page/<int:book_id>', methods=['GET'])
def update_page(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('update.html', book=book)


@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    flash('Book removed from the reading list.', 'success')
    return redirect(url_for('index'))


def search_books(query):
    # Google API key moved to environment variable.
    api_key = os.getenv('GOOGLE_API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    books = []
    if "items" in data:
        for item in data["items"]:
            book_info = item["volumeInfo"]
            books.append({
                "title": book_info.get("title", "Unknown Title"),
                "authors": book_info.get("authors", ["Unknown Author"]),
                "thumbnail": book_info.get("imageLinks", {}).get("thumbnail", "")
            })
    return books


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        books = search_books(query)
        return render_template('search.html', books=books)
    return render_template('search.html')

# Add this below all route decorators to create the database tables.


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
