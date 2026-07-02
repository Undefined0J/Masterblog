"""
Data access layer for the Masterblog application.
"""

import json
import os
from typing import List, Dict, Any

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
