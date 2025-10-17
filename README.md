# booklogger
A web app for tracking your reading.

- Users can sign up for a personal account.
- Users can add reviews for books they've read. Review can include a score.
- Users are able to leave comments on other peoples' reviews.
- Users can search for reviews by book titles or author names.
- User pages show how many books the user has read, average review score, and a list of their book reviews.
- Users have statistics pages that show how many books they've read each year, average book page count for each year etc.

## Testing

Make sure that flask is installed.
```
pip install flask
```

create and initialize the database with
```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

run the app with
```
flask run
```



Cover placeholder image from https://commons.wikimedia.org/wiki/File:Wikisource-books-missing-scan.png