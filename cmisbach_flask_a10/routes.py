#!/usr/bin/env python

# import necessities
from flask import Flask, render_template
import time

app = Flask(__name__)

# global variables used in base.html for the pages of the website
pages = {"Home" : "index", "About" : "about", "Links" : "links"}

# main landing page, the home page
@app.route("/")
def index():
    entries = []
    try:
        with open("entries.txt", "r") as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    timestamp = parts[0]
                    title = parts[1]
                    content = parts[2]

                    # Convert timestamp to readable date
                    date = time.ctime(int(timestamp))

                    entries.append({'date': date, 'title': title, 'content': content})
    except IOError:
        print("Error: File entries.txt does not appear to exist.")
               


    return render_template("home.html", pages=pages, entries=entries)

# creates about route
@app.route("/about")
def about():
    return render_template("about.html", pages=pages)

# creates links route
@app.route("/links")
def links():
    links = []
    with open("links.txt", "r") as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 2:
                links.append({'text': parts[0], 'url': parts[1]})

    return render_template("links.html", pages=pages, links=links)


# Set up the 404 not found handler.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Set up the 500 internal server error handler.
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Run flask server with my custom port (userid)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=17996)
