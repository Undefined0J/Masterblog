"""
Masterblog Application.

This module serves as the main entry point for the Flask web application,
handling the routing for the blog interface.
"""

from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the home page displaying all dynamic blog posts.

    :return: The rendered HTML template for the index page.
    """
    blog_posts = data_handler.load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the creation of a new blog post.

    GET request: Renders the form to create a post.
    POST request: Extracts form data, saves the post, and redirects to home.

    :return: HTML response or a redirection to the index route.
    """
    if request.method == 'POST':
        # Retrieve data from the HTML form fields
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        # Simple validation before saving
        if author and title and content:
            data_handler.add_post(author, title, content)
            return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000, debug=True)
