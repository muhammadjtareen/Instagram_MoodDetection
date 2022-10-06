from flask import Flask, render_template, redirect, url_for, request
from itertools import islice
from math import ceil
import base64
from instaloader import Instaloader, Profile


app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # return "HELLO"
        user=request.form['username']

        L = Instaloader()
        X_percentage = 10    # percentage of posts that should be downloaded


        total=[]
        profile = Profile.from_username(L.context, user)
        posts_sorted_by_likes = sorted(profile.get_posts(),
                               key=lambda p: p.likes + p.comments,
                               reverse=True)
        i=0
        for post in islice(posts_sorted_by_likes, ceil(profile.mediacount * X_percentage / 100)):
            # return post
            total.append(f"https://www.instagram.com/p/{post.shortcode}")
        return render_template('posts.html', posts=total)
        # for post in profile.get_posts():
        #     return post.url

        return f"<h1>{user}</h1>"
    else: 
        return render_template('index.html')



if __name__== "__main__": 
    app.run(debug=True)