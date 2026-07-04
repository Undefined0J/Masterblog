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


@app.route('/delete/<int:post_id>')
def delete(post_id: int):
    """
    Handle the deletion of a specific blog post.

    Extracts the post_id from the URL, removes it from the data store,
    and redirects back to the index page.

    :param post_id: The unique ID of the blog post to be deleted.
    :return: A redirection to the index route.
    """
    # Trigger the deletion logic in data handler
    data_handler.delete_post(post_id)

    # Redirect back to the home page to reflect changes
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int):
    """
    Handle the retrieval and modification of a specific blog post.

    GET request: Renders the edit form pre-populated with current post data.
    POST request: Extracts updated form entries, saves them, and redirects home.

    :param post_id: The unique ID of the blog post to update.
    :return: HTML response or a redirection to the index route.
    """
    # Fetch the specific post from the JSON database
    post = data_handler.get_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Extract and sanitize the updated inputs
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        # Simple validation before triggering backend storage update
        if author and title and content:
            data_handler.update_post(post_id, author, title, content)
            return redirect(url_for('index'))

    # Render form pre-populated with data
    return render_template('update.html', post=post)

if __name__ == '__main__':
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000, debug=True)
