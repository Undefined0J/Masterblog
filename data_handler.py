"""
Data access layer for the Masterblog application.
"""

import json
import os
from typing import List, Dict, Any, Optional

DATA_FILE = "posts.json"


def load_posts() -> List[Dict[str, Any]]:
    """
    Load all blog posts from the JSON data file.

    If the file does not exist or contains invalid JSON,
    it returns an empty list.

    :return: A list of dictionaries representing blog posts.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        # Fallback if file is corrupted or unreadable
        return []


def save_posts(posts: List[Dict[str, Any]]) -> bool:
    """
    Save the list of blog posts to the JSON data file.

    :param posts: The complete list of blog posts to persist.
    :return: True if saving was successful, False otherwise.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4, ensure_ascii=False)
            return True
    except IOError:
        return False


def add_post(author: str, title: str, content: str) -> None:
    """
    Create a new blog post with a unique ID and append it to the data store.

    :param author: The author of the blog post.
    :param title: The title of the blog post.
    :param content: The main body text of the blog post.
    """
    posts = load_posts()

    # Generate unique ID based on the maximum existing ID
    new_id = max((post["id"] for post in posts), default=0) + 1

    new_post = {
        "id": new_id,
        "author": author,
        "title": title,
        "content": content
    }

    posts.append(new_post)
    save_posts(posts)


def delete_post(post_id: int) -> bool:
    """
    Delete a blog post by its unique ID from the JSON data file.

    :param post_id: The unique identifier of the post to delete.
    :return: True if the post was found and deleted, False otherwise.
    """
    posts = load_posts()
    initial_count = len(posts)

    # Filter out the post with the matching ID
    posts = [post for post in posts if post["id"] != post_id]

    # If the count didn't change, the ID was not found
    if len(posts) == initial_count:
        return False

    return save_posts(posts)


def get_post_by_id(post_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single blog post by its unique ID.

    :param post_id: The unique identifier of the post.
    :return: The post dictionary if found, None otherwise.
    """
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


def update_post(post_id: int, author: str, title: str, content: str) -> bool:
    """
    Update the core details of an existing blog post.

    :param post_id: The unique identifier of the post to modify.
    :param author: The updated name of the author.
    :param title: The updated title of the post.
    :param content: The updated content body.
    :return: True if the post was found and updated, False otherwise.
    """
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["author"] = author
            post["title"] = title
            post["content"] = content
            return save_posts(posts)
    return False
