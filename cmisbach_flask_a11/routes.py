#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# Titles of the pages of the website used in base.html
pages = {"Home" : "index", "Create": "create", "Directory of Links": "directory"}

# main landing page, home page
@app.route("/")
def index():
    return render_template("home.html", pages=pages)

@app.route("/create")
def create():
    return render_template("create.html", pages=pages)

@app.route("/directory")
def directory():
    # Read the mappings from the file
    with open('url_mappings.txt', 'r') as file:
        # Create a list of tuples from the file contents
        mappings = [line.strip().split(' ', 1) for line in file if line.strip()]

    # Now pass the mappings to the template
    return render_template("directory.html", pages=pages, mappings=mappings)

@app.route("/process", methods=['POST'])
def process():
    # Grab the URL from the form field
    url = request.form['link']
    # Shorten the URL using the specified algorithm
    shortcode = shorten_url(url)
    # Create the full shortened URL using the shortcode
    full_shortened_url = f'http://odin.unomaha.edu/go/{shortcode}'
    # Save the shortcode and URL mapping to a file
    with open('url_mappings.txt', 'a') as file:
        file.write(f'{full_shortened_url} {url}\n')
    # Redirect to the success page, passing the shortcode and URL for display
    return redirect(url_for('success', shortcode=shortcode, url=url))

def shorten_url(url):
    # Step 1 and 2: Remove all punctuation and digits, leaving only letters
    url = re.sub(r'[^\w\s]', '', url)  
    url = re.sub(r'\d', '', url)       

    # Step 3: Convert all letters to lowercase
    shortened_url = url.lower()

    # Step 5: Fold the URL while it's longer than 8 characters
    while len(shortened_url) > 8:
        new_shortened_url = ''

        for i in range(0, len(shortened_url) - 1, 2):
            # Combine consecutive pairs of characters by adding their ASCII values together
            combined_ascii = ord(shortened_url[i]) + ord(shortened_url[i+1])
            # Divide the total by 2 and calculate the integer result
            new_char = chr(combined_ascii // 2)
            # Add it to a new version of the shortened URL
            new_shortened_url += new_char
        # Re-assign the newly created shortened URL for the next iteration
        shortened_url = new_shortened_url

    return shortened_url



@app.route("/sucess/<shortcode>")
def success(shortcode):
    # Find the URL from the file or pass it directly if available
    return render_template("success.html", shortcode=shortcode, pages=pages)

@app.route("/go/<id>")
def go(id):
    # Read the file and find the URL associated with the shortcode
    with open('url_mappings.txt', 'r') as file:
        mappings = {line.split()[0]: line.split()[1] for line in file}

    if id in mappings:
        return redirect(mappings[id])
    else:
        return redirect(url_for('oops'))

# You may need to create an "oops" route and template for errors

# Set up the 404 not found handler.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Run flask server with my custom port (userid)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=17996)
