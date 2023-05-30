Ryan's Reading List App
This is a simple web application built using Flask, PostgreSQL, and Google Books API. It allows users to maintain a list of books they've read, search for books, add them to their reading list, update details of the books, and delete books from the list.

Features
List of books a user has read, displaying title, author, rating, and review.
Search functionality using the Google Books API, allowing users to search for books and view basic information about the search results.
Option to add searched books to the user's reading list.
Update the rating and review of the books in the reading list.
Delete a book from the reading list.
Uses a PostgreSQL database for data storage.

Prerequisites
Python 3
Flask
PostgreSQL

Installation
Clone the repository:
git clone https://github.com/your-username/ryans-reading-list.git

Change to the project directory:
cd ryans-reading-list

Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate

Install the required packages:
pip install -r requirements.txt
Set up your PostgreSQL database and update the DATABASE_URL in the config.py file with your database details.

Set up your Google Books API key by following the instructions here. Add your API key to the config.py file.

Set up the environment variables:

export FLASK_APP=app.py
export FLASK_ENV=development

Create the database tables:
flask db upgrade

Run the application:
flask run
The application should now be accessible at http://localhost:5000.

Usage
Visit the application at http://localhost:5000.
Click the "Search Books" button to search for books using the Google Books API.
Click "Add to reading list" to add a book to your reading list.
On the main page, you can view your reading list, update the rating and review of a book, or delete a book from the list.
