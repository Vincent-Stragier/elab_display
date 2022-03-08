"""
    This module aims to provide a way to scrap posts on a Facebook page,
    to remove or add emoji and to get the number of likes on a page.

    Requirement:
    python3 -m pip install pillow facebook_scraper, demoji, emoji
"""
import re
import requests

# https://pypi.org/project/demoji/
import demoji

import emoji

# https://pypi.org/project/facebook-scraper/
from facebook_scraper import get_posts  # , set_user_agent


def get_likes_count(page_name: str) -> int:
    """Get the number of likes on the Facebook page"""
    URL = f"https://fr-fr.facebook.com/pg/{page_name}"

    response = requests.get(URL)
    regex = ('<meta name="description"[^/>0-9]+'
             '([0-9]+)[\s]+J&#x2019;aime[^/>]+')
    count = re.findall(regex, response.text)[0]
    return int(count) if str(int(count)) == count else -1


def remove_emoji(data: str) -> str:
    """Remove the emoji from the 'data' string."""
    return demoji.replace(data)


def add_emoji(emoji_name: str) -> str:
    """Return the UTF-8 encoded emoji value."""
    return emoji.emojize(emoji_name)


def get_matching_post(
        page_name: str, key: str, enable_emoji: bool = True) -> str:
    """Get the first post on the 'page_name' FB page containing the 'key'."""
    # set_user_agent()
    for post in get_posts(page_name):
        # Looking for the 'key' emoji
        if key in post['text'][:]:
            if enable_emoji:
                return post['text'][:]
            else:
                return remove_emoji(post['text'][:])
    return None


def main() -> None:
    # PAGE_NAME = "electroLAB.FPMs"
    # PAGE_NAME = "codobot.be"
    # PAGE_NAME = "tamu"
    PAGE_NAME = "UniversiteMons"
    print(f"Test: {PAGE_NAME = }")
    print(get_likes_count(page_name=PAGE_NAME))
    print("This Python script is a module which can be used"
          " to scrap information from a Facebook page.")


if __name__ == "__main__":
    main()
