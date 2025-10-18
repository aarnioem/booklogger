# booklogger
A web app for tracking your reading.

- Users can sign up for a personal account.
- Users can add reviews for books they've read. Review can include a score.
- Users are able to leave comments on other peoples' reviews.
- Users can search for reviews by book titles.
- User pages show how many books the user has read, which categories their logged books are in, signup date, how many comments they have left, and a list of their book reviews.

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

### Large database test

The app has been tested with a database that was seeded with `seed.py`. Without the index that is in `schema.sql` the profile pages were very slow (10-15 seconds) due to the complex query that is performed for the user stats. Search can be a bit slow if there's a lot of results, but I couldn't come up with a very good solution to this. All other pages seemed to be lightning fast, so I have not added other indices.


Cover placeholder image from https://commons.wikimedia.org/wiki/File:Wikisource-books-missing-scan.png