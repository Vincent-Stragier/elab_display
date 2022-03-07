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
# from contextlib import redirect_stdout
# import io

import emoji

# https://pypi.org/project/facebook-scraper/
from facebook_scraper import get_posts  # , set_user_agent


# Get the number of likes on the Facebook page (using the name of the page)
def getLikeCount(page_name):
    URL = f"https://fr-fr.facebook.com/pg/{page_name}"

    response = requests.get(URL)
    description = re.findall("<meta name=\"description\".+/>", response.text)
    count = re.findall("([0-9]+)[\s]+J&#x2019;aime", description[0])[0]
    return count if count else -1

# Remove the emoji from the 'data' string
def remove_emoji(data):
    return demoji.replace(data)


# Return the UTF-8 encoded emoji value
def add_emoji(emoji_name):
    return emoji.emojize(emoji_name)


# Get the first post on the 'page_name' Facebook Page containing the 'key'
def getPost(page_name, key, enable_emoji=True):
    # set_user_agent("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
    for post in get_posts(page_name):
        if key in post['text'][:]:  # Looking for the clock emoji
            if enable_emoji:
                return post['text'][:]
            else:
                return remove_emoji(post['text'][:])
    return None


def main():
    # PAGE_NAME = "electroLAB.FPMs"
    # PAGE_NAME = "codobot.be"
    # PAGE_NAME = "tamu"
    # PAGE_NAME = "UniversiteMons"
    # print(getLikeCount(page_name=PAGE_NAME))
    print("This Python script is a module which can be used"
          " to scrap information from a Facebook page.")


if __name__ == "__main__":
    main()
