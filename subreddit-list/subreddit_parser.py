# Usage: go to http://www.reddit.com/reddits/mine/.json?limit=100
# where limit is set to a number greater than the number of subreddits
# you are subscribed to.

import json


def subreddit_parser(json_text):
    json_data = json.loads(json_text)
    subreddit_data = json_data[u'data'][u'children']
    out = open("sr_parser_output.html", "w")
    out.write("<!doctype html><html><title>subreddits</title><body>")
    out.write("<table><thead><th>#</th><th>subreddit</th><th>subscribers"
              "</th></thead><tbody>")
    for num, subreddit in enumerate(subreddit_data):
        template = '<tr><td>%d</td><td><a href="http://www.reddit.com%s">%s</a></td><td>%d</tr>\n'
        out.write(template % (num + 1,
                              subreddit[u'data'][u'url'],
                              subreddit[u'data'][u'display_name'],
                              subreddit[u'data'][u'subscribers']))
    out.write("</tbody></table></body></html>")

if __name__ == "__main__":
    subreddit_parser(open("json").read())
