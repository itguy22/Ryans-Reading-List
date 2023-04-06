# What's wrong with my code? I'm getting an error when I try to add a book to the reading list. The error is RunTime Error: The session is unavailable because no secret key was set. Set the secret_key on the application to something unique and secret.
import os
from flask import render_template, request, redirect, url_for, flash
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5MY9ppxA3J47NB@localhost/reading_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = os.urandom(24)

# Move imports that use `db` below the `db` definition


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
    if request.method == 'POST':
        title = request.form['title']
        rating = request.form['rating']
        review = request.form['review']
        book = Book(title, rating, review)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))

    books = Book.query.all()
    return render_template('index.html', books=books)


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
    print(request.form)
    book_id = request.form.get('book_id')
    title = request.form['title']
    authors = request.form['authors']
    rating = request.form['rating']
    review = request.form['review']
    # Fetch book details and save it to your database or storage
    # ...
    return redirect(url_for('reading_list'))


@app.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)

    book.title = request.form['title']
    book.authors = request.form['authors']
    book.rating = request.form['rating']
    book.review = request.form['review']

    db.session.commit()

    flash('Book updated successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    flash('Book removed from the reading list.', 'success')
    return redirect(url_for('index'))


def search_books(query):
    # Replace with your actual Google Books API key
    api_key = "AIzaSyDu0fKNRA-mMeZ2OBZH3n-JjiYPQTQKnUA"
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


if __name__ == '__main__':
    app.run(debug=True)
