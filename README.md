# Soulappetit
 Using deep neural network to predict the facial expression then the app will recommend some songs that fit the user emotion the most

## Project goal
* Build model to classify whether the emotion of people face base on the provided image. Moreover the model has to reach more than 80% accuracy score
* Build a Flask app to identify facial area and tag each person face in side the picture with a given name and predicted expression
* After the expression is detected then the app will recommend some songs that fit the user emotion.


## Link to the flask app
* https://github.com/hangnguyennn13/Soulappetit

## Main Task:
1. Recognizing Emotion
2. Recommending Music
3. Build Flask App
4. Deploy on gcloud

## Recognizing Emotion


### Understanding the facial experssion dataset
* Label: 0 - positive, 1 - neutral, 2 - negative
* Image_path: Path to a image


### Tasks needed to be done
#### Create VM on GCE with Deep learning platform: https://hackmd.io/SEVZeQMJRa2JJMxd9y8PnQ
#### Build Model:
1. Collect data
    * The guide for download images from google can be found [here](https://hackmd.io/8McWB9l9S-K58OxSiLM65A)
    * Using the above technic to download needed image: happy - emotionless - unhappy face

2. Preprocess data:
    * Using face_recognition library to select only the face from the raw image downloaded from google
    * Saved it in another folder
    * ```python=
        import face_recognition
        from PIL import Image, ImageDraw
        import glob
        import os
        import pathlib

        def face_extract(raw_folder,save_folder):

            data_root = pathlib.Path(raw_folder)
            img = data_root.glob('*')

            j = 1


            for i in img:

                image = face_recognition.load_image_file(i)
                face_locations = face_recognition.face_locations(image)

                for face_location in face_locations:
                    top, right, bottom, left = face_location

                    face_image = image[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    # pil_image.show()

                    # path to save file
                    s = save_folder + '/sad_'+str(j)
                    pil_image.save(f'{s}.jpg')

                    j += 1



        if __name__ == "__main__":
            face_extract('static/img/sad_raw','static/img/sad')```



3. Save the image path + label in python dataframe

4. Check whether we have a balanced dataset or not using seaborn countplot on the label columns. If not then consider to choose between applying undersamplying or oversampling technique. However, we have a nearly balanced dataset (937- happy, 500 - emotionless, 700 - unhappy) so we can skip this part 

5. **CNN architecture**:
    * **Input Layer:** It represent input image data. It will reshape image into single diminsion array. Example your image is 64x64 = 4096, it will convert to (4096,1) array.

    * **Conv Layer:** This layer will extract features from image.

    * **Pooling Layer:** This layerreduce the spatial volume of input image after convolution.

    * **Fully Connected Layer:** It connect the network from a layer to another layer

    * **Output Layer:** It is the predicted values layer.

    * **Loss:**- To make our model better we either minimize loss or maximize accuracy. NN always minimize loss. To measure it we can use different formulas like 'categorical_crossentropy' or 'binary_crossentropy'. Here I have used binary_crossentropy

    * **Optimizer :**- If you know a lil bit about mathematics of machine learning you might be familier with local minima or global minima or cost function. To minimize cost function we use different methods For ex :- like gradient descent, stochastic gradient descent. So these are call optimizers. We are using a default one here which is adam

    * **Metrics :**- This is to denote the measure of your model. Can be accuracy or some other metric.

6. Define a Sequential model

7. Fine Tune
    * **Early Stopping:**
    * **Reduce Learning rate:**

## Recommending Music
### 1. Get  data
1. Use last.fm api to scrape top 100 famous artist
2. Use genius api to get the artist songs and image and lyrics
3. Use last.fm api to get famous tags of each songs
4. Use youtube api to get youtube video id for embedding purpose
### 2. Preprocessing data
#### a. Song tags
1. Preprocessing tags to take only the genre of the songs
2. Some song that doesn't have any tag so we take the common genre in the artist's list songs. Finally, assign that to tag to the song that missed the tag. If no song in the artist's list have tags then delete the list
#### b. Song lyrics
1. Turn to dtype to string
2. Remove punctuation (list of common punctuation: string.punctuation)
3. Remove words in the square bracket
4. Remove stopwords
5. Label sentimental using 



#### Build Flask App:
1. Visual Code as our environment to build flask app

2. Create a folder to store your work

3. Create a virtual and activate environment:
    * virtualen env
    * For ios: source env/bin/activate
    * For windows: cd env/Scripts then activate

5. Install libraries inside the virtual environment
    * pip -r requirement.txt

6. Activate debug mode:
    ```python=
        if __name__ == "__main__":
            app.run(debug = True)
    ```

7. Template:
![](https://i.imgur.com/NMdKaGm.png)

    * home.html: 
        * navigation bar
        * banner
        * project goal
        * footer
        * sign-in button
    * predict.html: predict the expression
        * take a picture from camera
        * upload a picture
        * type the feeling
        * correct button to correct the emotion if the model predict wrong. 
        * return the result to the recommendation page
    * recommend.html:
        * music section:
            * Use youtube api embed code
            
