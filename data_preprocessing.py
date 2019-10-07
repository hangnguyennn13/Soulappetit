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
    face_extract('static/img/sad_raw','static/img/sad')