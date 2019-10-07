from flask import Blueprint, render_template, request, redirect,jsonify
import base64
import re
import sys
import os
import tensorflow as tf
import face_recognition
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from werkzeug import secure_filename 

# from IPython import display

modelpage = Blueprint('modelpage', __name__)

model = tf.keras.models.load_model("static/models/vgg16.h5")


DOT = 'dot'
COSINE = 'cosine'

songs = pd.read_pickle('./static/data/data.pkl')
genre_cols = ['Hip-Hop', 'Jazz', 'Soul','Blues', 'Rock',
                         'Dance', 'Electronic', 'Pop', 'Country']
music_embedding = songs[['pos','neu','neg']]

def compute_scores(query_embedding, item_embeddings, measure=DOT):
    """Computes the scores of the candidates given a query.
    Args:
        query_embedding: a vector of shape [k], representing the query embedding.
        item_embeddings: a matrix of shape [N, k], such that row i is the embedding
          of item i.
        measure: a string specifying the similarity measure to be used. Can be
          either DOT or COSINE.
    Returns:
        scores: a vector of shape [N], such that scores[i] is the score of item i.
    """
    u = query_embedding
    V = item_embeddings
    if measure == COSINE:
        V = V / np.linalg.norm(V, axis=1, keepdims=True)
        u = u / np.linalg.norm(u)
    else:
        u = np.array(u)
        
    scores = u.dot(V.T)
    return scores

def user_recommendations(user_id,user_embedding, music_embedding, measure='dot', exclude_rated=True, k=6):
    scores = compute_scores(
        user_embedding[user_id], music_embedding, measure)
    score_key = measure + ' score'
    df = pd.DataFrame({
        score_key: list(scores),
        'titles': songs['title'],
        'artist': songs['artist'],
        'videoId': songs['videoId'],
        'all_genres': songs['all_genres']
    })

    return df.sort_values([score_key], ascending=False).head(k)  


@modelpage.route('/model')
def home():
    
    return render_template('model.html')


@modelpage.route("/upload/", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        # retrieve the image from the ajax request
        file = request.files['file']
        # firstname = request.form['firstname']

        # names = firstname.split('-')
        # print(firstname, file=sys.stdout)

        # security stuff
        filename = secure_filename(file.filename)
        # get the full file path
        upload_file_path = os.path.join('UPLOAD_FOLDER', filename)
        # save the image to our uploads folder
        file.save(upload_file_path)

        # Load test image to find faces in
        test_image = face_recognition.load_image_file(upload_file_path)

        # Find faces in test image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # Convert to PIL format
        pil_image = Image.fromarray(test_image)

        # Create a ImageDraw instance
        draw = ImageDraw.Draw(pil_image)
        j = 0
        i = 0

        def takeleft(elem):
            return elem[-1]

        face_locations.sort(key=takeleft)

        # Loop through faces in test image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            
            face_image = test_image[top:bottom, left:right]
            pil_image1 = Image.fromarray(face_image)
            
            name = 'Unknown'
            
            # if j < len(names):
            #     name = names[j]
            #     name = name.strip('')
            #     j+=1
            

            # If match
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            
            pil_image1.save('new_image' + str(i)+'.jpg')

            img = tf.io.read_file('new_image' + str(i)+'.jpg')
            img = tf.image.decode_jpeg(img, channels=3)
            img = tf.image.resize(img, [100,100])
            img = img / 255.0
            img = 2*img - 1
            probabilites = model.predict(tf.expand_dims(img,0))
            prediction = np.argmax(probabilites, axis=1)[0]
            # class = {0: 'Happy', 1: 'Emotionless',2:'Unhappy'}

            indices = {0: 'Happy', 1: 'Emotionless',2:'Unhappy'}
            label = indices[prediction]
            print(label)
            # Draw box
            draw.rectangle(((left-10, top), (right+10
            , bottom)), outline=(255,255,0))
            # Draw label
            draw_label = name + ' is ' + label
            print(draw_label)
            text_width, text_height = draw.textsize(draw_label)
            draw.rectangle(((left-10,bottom - text_height - 10), (right+10, bottom)), fill=(255,255,0), outline=(255,255,0))
            draw.text((left-7, bottom - text_height - 5), draw_label, fill=(0,0,0))

            # pil_image1.show()
            i += 1

        for w in range(0,i):
            os.remove('new_image' + str(w)+'.jpg')

        del draw

        # Save image
        pil_image.save('identify.jpg')

        with open("identify.jpg", "rb") as img_file:
            my_string = base64.b64encode(img_file.read()).decode('UTF-8')

        # print(probabilites)
        rs = user_recommendations(0,probabilites, music_embedding, measure='cosine', k=10).reset_index()
        # print(rs)
        rs = rs[['index','titles','artist','videoId','all_genres']].as_matrix().tolist()


        return (jsonify({'img': my_string, 'videoId': rs[0][3],'song':rs,'label':label}))