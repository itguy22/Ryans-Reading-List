Ryan's Reading List App

This is a simple web application built using Flask, PostgreSQL, and Google Books API. It allows users to maintain a list of books they've read, search for books, add them to their reading list, update details of the books, and delete books from the list.

Features

List of books a user has read, displaying title, author, rating, review, and thumbnail image.
Search functionality using the Google Books API, allowing users to search for books and view basic information about the search results.
Option to add searched books to the user's reading list.
Update the rating, review, and thumbnail image of the books in the reading list.
Delete a book from the reading list.
Uses a PostgreSQL database for data storage.
Prerequisites

Docker
Docker Compose

Installation

Clone the repository
bash
git clone https://github.com/your-username/ryans-reading-list.git

Change to the project directory

cd ryans-reading-list

Build and run Docker containers
docker-compose up -d --build

The application should now be accessible at http://localhost:5001.

The Docker Compose file will create two Docker containers - one for the PostgreSQL database and one for the Flask app. It will also install all the Python dependencies from the requirements.txt file.

The db container will create a PostgreSQL database using the environment variables from the .env file.

The web container will run the Flask application.

Create database tables
To create the database tables, you'll need to run the database upgrade command in the web container.

First, get the id of the web container with this command:
docker ps

Then, run the database upgrade command:

docker exec -it <container-id> flask db upgrade
Remember to replace <container-id> with your container's id.

Set up the Google Books API
Set up your Google Books API key by following the instructions here.

After you get your API key, add it as an environment variable to the Docker Compose file.

Usage
Visit the application at http://localhost:5001.
Click the "Search Books" button to search for books using the Google Books API.
Click "Add to reading list" to add a book to your reading list.
On the main page, you can view your reading list, update the rating and review of a book, or delete a book from the list.
