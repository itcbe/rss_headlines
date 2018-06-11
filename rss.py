import json

from bottle import route, run, template, static_file, request, response, get
import feedparser

RSS_FEEDS = {
    "1": {
        "title": "The Jerusalem Post",
        "rss_link": "https://www.jpost.com/Rss/RssFeedsHeadlines.aspx"
    },
    "2": {
        "title": "Daily Mail",
        "rss_link": "http://www.dailymail.co.uk/articles.rss"
    },
    "3": {
        "title": "Wired Magazine",
        "rss_link": "http://feeds.wired.com/wired/index"
    },
}


@route('/', method="GET")
def index():
    return template("rss.html")


@route("/api/feeds", method="GET")
def get_feeds():
    """
    Available RSS feeds
    """
    return json.dumps(RSS_FEEDS)


@route("/api/headlines", method="GET")
def update_headlines():
    # Handle explicit feed selection using the "feed" query string parameter.
    # For example: http://localhost:7000/api/headlines?feed=3 will select the "Wired Magazine" RSS feed.
    desired_rss_feed = request.query.get("feed", "1")
    if desired_rss_feed not in RSS_FEEDS:
        desired_rss_feed = "1"

    # Fetch the feed
    feed = feedparser.parse(RSS_FEEDS[desired_rss_feed]["rss_link"])

    # Format a response for the client using list comprehension. Every element in the list is a dictionary
    # providing details on a single headline (it's title and a link to the full story).
    headlines = [
                    {"title": entry["title"], "link": entry["link"]}
                    for entry in feed["entries"]
                ]

    return json.dumps({"headlines": headlines})


####
# Static files function handlers
####


@route('/static/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='static/css')


@route('/static/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='static/images')


def main():
    run(host='localhost', port=7000, debug=True)


if __name__ == '__main__':
    main()
