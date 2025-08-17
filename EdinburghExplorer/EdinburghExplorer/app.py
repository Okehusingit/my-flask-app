from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import re
import json
import os

# Flask Tourism Web App
# Acknowledgements:
# - W3Schools tutorials were used for reference on:
#   • Python regex (email validation) -> https://www.w3schools.com/python/python_regex.asp
#   • Flask basics (routes, templates) -> https://www.w3schools.com/python/python_flask_getstarted.asp
# All other logic and file handling were implemented by the author.

app = Flask(__name__)

# Secret key for flash messages and sessions
# In production, always set SECRET_KEY as an environment variable
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

def get_current_year():
    return datetime.now().year

# Paths for data and messages
DATA_DIR = os.path.join(app.root_path, "data")
MESSAGES_FILE = os.path.join(app.root_path, "messages.txt")
ATTRACTIONS_FILE = os.path.join(DATA_DIR, "attractions_data.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure attractions JSON exists
if not os.path.exists(ATTRACTIONS_FILE):
    with open(ATTRACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route("/")
def index():
    return render_template("index.html", current_year=get_current_year())

@app.route("/about")
def about():
    return render_template("about.html", current_year=get_current_year())

@app.route("/attractions")
def attractions():
    try:
        with open(ATTRACTIONS_FILE, "r", encoding="utf-8") as f:
            attractions_data = json.load(f)
    except json.JSONDecodeError:
        attractions_data = []
        flash("Error reading attractions data. File reset.", "warning")
        with open(ATTRACTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(attractions_data, f)

    return render_template("attractions.html", attractions=attractions_data, current_year=get_current_year())

@app.route("/blogs")
def blogs():
    return render_template("blogs.html", current_year=get_current_year())

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Basic form validation (reference: W3Schools regex and validation examples)
        if not name or not email or not message:
            flash("All fields are required.", "danger")
            return redirect(url_for("contact"))

        # Email validation regex (adapted from W3Schools regex tutorial)
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("contact"))

        # Save message to file
        with open(MESSAGES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{name} | {email} | {message}\n")

        flash("✅ Thank you for your message! We'll get back to you soon.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", current_year=get_current_year())

@app.route("/events")
def events():
    return render_template("events.html", current_year=get_current_year())

@app.route("/itinerary")
def itinerary():
    return render_template("itinerary.html", current_year=get_current_year())

if __name__ == "__main__":
    app.run(debug=True)
