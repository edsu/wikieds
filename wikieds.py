#!/usr/bin/env python

"""
Print a summary of Wikipedia editors for a given article as markdown.
"""

import sys
import json

from urllib.request import urlopen, quote

# some bots have edited millions of articles, we don't want to count them all :)

MAX_ARTICLES = 1000


def get_articles_edited(user):
    user = quote(user)
    url = 'https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser=%s&uclimit=200&ucnamespace=0&format=json' % user
    cursor = None
    articles = set()
    while True:
        u = url
        if cursor:
            u += "&uccontinue=" + cursor
        results = json.load(urlopen(u))
        for edit in results['query']['usercontribs']:
            articles.add(edit['title'])
        if len(articles) > MAX_ARTICLES:
            break
        elif 'continue' in results:
            cursor = results['continue']['uccontinue']
        else:
            break
    return articles


def get_editors(title):
    """
    Give this function a wikipedia article title and it will walk through 
    the edits to see who the editors were.
    """
    title = quote(title)
    url = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=%s&rvlimit=500&rvprop=timestamp|user|comment|size&continue=&format=json' % title
    stats = {"users": {}, "count": 0, "creator": None, "created": None}
    cursor = None
    user = None
    while True:
        u = url
        if cursor:
            u += "&rvcontinue=" + cursor
        results = json.load(urlopen(u))
        page_id = list(results['query']['pages'].keys())[0]
        for rev in results['query']['pages'][page_id]['revisions']:
            if 'user' not in rev:
                continue
            stats['count'] = stats.get('count', 0) + 1
            user = rev['user']
            date = rev['timestamp']
            stats['users'][user] = stats['users'].get(user, 0) + 1
        if 'continue' in results:
            cursor = results['continue']['rvcontinue']
        else:
            break
    stats['creator'] = user
    stats['created'] = date
    return stats


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: wikistats [article title]")

    title = ' '.join(sys.argv[1:])
    editors = get_editors(title)

    print("### Wikipedia Editor Statistics for %s" % title)
    print() 
    print("The Wikipedia article %s was created by %s at %s and has been edited %s times by %s users." % (title, editors['creator'], editors['created'], editors['count'], len(editors['users'].keys())))
    print()

    users = list(editors['users'].keys())
    users = sorted(users, key=lambda a: editors['users'][a], reverse=True) 

    print("| User                                     | Edits      | Articles   |")
    print("| ---------------------------------------- | ----------:| ----------:|")
    for user in users:
        articles_edited = len(get_articles_edited(user))
        if articles_edited >= MAX_ARTICLES:
            articles_edited = '+%i' % MAX_ARTICLES
        else:
            articles_edited = str(articles_edited)

        print("| %40s | %10s | %10s |" % (user, editors['users'][user], articles_edited))

if __name__ == "__main__":
    main()
