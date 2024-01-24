from nntplib import ArticleInfo
from unittest import result
from wiki import article_metadata, ask_search, ask_advanced_search
from datetime import *
import time


def keyword_to_titles(metadata):
    keyword_dictionary = {}
    for article in metadata:
        for word in article[4]:
            if word in keyword_dictionary:
                keyword_dictionary[word].append(article[0])
            else:
                keyword_dictionary[word] = [article[0]]
    return keyword_dictionary


def title_to_info(metadata):
    title_dictionary = {}
    for article in metadata:
        title_dictionary[article[0]] = {
            "author": article[1],
            "timestamp": article[2],
            "length": article[3],
        }
    return title_dictionary


def search(keyword, keyword_to_titles):
    for key_word in keyword_to_titles:
        if keyword == key_word:
            return keyword_to_titles[key_word]
    return []


def article_length(max_length, article_titles, title_to_info):
    less_than_max_length = []
    for article_title in title_to_info:
        if article_title in article_titles:
            if title_to_info[article_title]["length"] <= max_length:
                less_than_max_length.append(article_title)
    return less_than_max_length


def key_by_author(article_titles, title_to_info):
    author_dictionary = {}
    for article_title in title_to_info:
        if article_title in article_titles:
            if title_to_info[article_title]["author"] not in author_dictionary:
                author_dictionary[title_to_info[article_title]["author"]] = [
                    article_title
                ]
            else:
                author_dictionary[title_to_info[article_title]["author"]].append(
                    article_title
                )
    return author_dictionary


def filter_to_author(author, article_titles, title_to_info):
    author_articles = []
    for article_title in title_to_info:
        if article_title in article_titles:
            if title_to_info[article_title]["author"] == author:
                author_articles.append(article_title)
    return author_articles


def filter_out(keyword, article_titles, keyword_to_titles):
    does_not_contain_keyword = article_titles.copy()
    for key_word in keyword_to_titles:
        if keyword == key_word:
            for article in keyword_to_titles[key_word]:
                if article in article_titles:
                    does_not_contain_keyword.remove(article)
    return does_not_contain_keyword


def articles_from_year(year, article_titles, title_to_info):
    from_year = []
    for article_title in title_to_info:
        if article_title in article_titles:
            if year == int(
                datetime.utcfromtimestamp(
                    title_to_info[article_title]["timestamp"]
                ).strftime("%Y")
            ):
                from_year.append(article_title)
    return from_year


# Prints out articles based on searched keyword and advanced options
def display_result():
    # Preprocess all metadata to dictionaries
    keyword_to_titles_dict = keyword_to_titles(article_metadata())
    title_to_info_dict = title_to_info(article_metadata())

    # Stores list of articles returned from searching user's keyword
    articles = search(ask_search(), keyword_to_titles_dict)

    # advanced stores user's chosen advanced option (1-7)
    # value stores user's response in being asked the advanced option
    advanced, value = ask_advanced_search()

    if advanced == 1:
        # value stores max length of articles
        # Update articles to contain only ones not exceeding the maximum length
        articles = article_length(value, articles, title_to_info_dict)
    if advanced == 2:
        # Update articles to be a dictionary keyed by author
        articles = key_by_author(articles, title_to_info_dict)
    elif advanced == 3:
        # value stores author name
        # Update article metadata to only contain titles and timestamps
        articles = filter_to_author(value, articles, title_to_info_dict)
    elif advanced == 4:
        # value stores a second keyword
        # Filter articles to exclude those containing the new keyword.
        articles = filter_out(value, articles, keyword_to_titles_dict)
    elif advanced == 5:
        # value stores year as an int
        # Update article metadata to contain only articles from that year
        articles = articles_from_year(value, articles, title_to_info_dict)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))


if __name__ == "__main__":
    display_result()
