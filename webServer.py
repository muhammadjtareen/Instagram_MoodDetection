from flask import Flask, render_template, redirect, url_for, request, make_response
from itertools import islice
from math import ceil
import base64
import shutil
from instaloader import Instaloader, Profile
import os

import io



import cv2


app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # return "HELLO"
        user=request.form['username']

        #the reason this is important is to remove any repeated entries. 
        file_path = os.getcwd() + f'/static/{user}'

        if os.path.exists(file_path) and os.path.isdir(file_path):
            shutil.rmtree(file_path)
        os.mkdir(file_path)
        
        #import haar-cascades
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        L = Instaloader(dirname_pattern=f'static/{user}')
        X_percentage = 5    # percentage of posts that should be downloaded


        total=[]
        profile = Profile.from_username(L.context, user)
        posts_sorted_by_likes = sorted(profile.get_posts(),
                               key=lambda p: p.likes + p.comments,
                               reverse=True)
        

        for post in islice(posts_sorted_by_likes, ceil(profile.mediacount * X_percentage / 100)):
            # return post
            total.append(f"https://www.instagram.com/p/{post.shortcode}")
            L.download_post(post, user)
        
        directory= f'static/{user}'
        files=[]
        for filename in os.listdir(directory): 
            f = os.path.join(directory, filename)
            if os.path.isfile(f) and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                #load file:
                img = cv2.imread(f)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.35, 5)
                for (x,y,w,h) in faces: 
                    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0,0), 5)
                    roi_gray=gray[y:y+h, x:x+w]
                    roi_color=img[y:y+h, x:x+w]

                    eyes = eye_cascade.detectMultiScale(roi_gray, 1.35, 5)

                    for (ex, ey, ew, eh) in eyes: 
                        cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 5)
                
                cv2.imwrite(f, img)

                
                files.append(f)

        print(files)
        print("HELLO")
        # return "HELLO"

        return render_template('test.html', posts=total, images=files, user=user)
        for post in profile.get_posts():
            return post.url

        return f"<h1>{user}</h1>"
    else: 
        return render_template('index.html')



if __name__== "__main__": 
    app.run(debug=True)