from flask import Flask , jsonify, render_template
import requests
import re

app = Flask(__name__)

#get the x_guest_token for twitter
def get_token():
    try:
        linkToGetToken = requests.get('https://twitter.com')
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error_message": str(e)})
    text = linkToGetToken.text
    tok = re.search('gt=([0-9]+)', text)
    if tok:
        return tok.group(1)
    else:
        print("Error: failed to generate guest token")
        return -1


@app.route("/<int:id>")
def get_post(id):
    if not id:
        return "<p>the URL must contain the Post_ID</p>"
    x_guest_token = get_token()
    auth = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    if x_guest_token == -1:
        return '<p>Error: failed to generate guest token</p>'
    headers_dict = {"authorization": auth
                    ,"x-guest-token": x_guest_token
                    }

    try:
        req = requests.get('https://twitter.com/i/api/2/timeline/conversation/'+str(id)+'.json', headers=headers_dict)
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error_message": str(e)})

    j = req.json()
    twitter_det = j["globalObjects"]['tweets'][str(id)]
    media = []
    if twitter_det['entities']:
        all_media = twitter_det['entities']['media']
        for i in range(len(all_media)):
            media.append(all_media[i]['media_url'])
    return render_template('postDetail.html', likes=str(twitter_det['favorite_count']), postText=str(twitter_det['text'])
                           , tweetCount=str(twitter_det['retweet_count']), media=media, created=twitter_det['created_at'])




