from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['portfolio_db']
contact_collection = db['contacts']

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('contact'))

        # Save to MongoDB
        contact_collection.insert_one({
            "name": name,
            "email": email,
            "message": message
        })

        flash('Thank you for contacting me! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# -------------------- RUN APP --------------------

if __name__ == '__main__':
    app.run(debug=True)
