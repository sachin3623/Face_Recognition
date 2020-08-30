from flask import Flask, request, jsonify
import face_recognition
from os import listdir
from os.path import isfile, join, dirname
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
@app.route('/test')
def hello_world():
        return 'Hello, Get'


## Create and save encodings of known faces
known_faces = []

## load images dictionary
loaded_imgs = {}


# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


## add image
@app.route('/saveimg', methods=['POST'])
def save_img():
    if request.method == 'POST':
        f = request.files['file']
        i = secure_filename(f.filename)
        f.save(join(dirname(__file__)+'/known', i))
        k = face_recognition.load_image_file('./known/'+f.filename)
        known_faces.append(face_recognition.face_encodings(k)[0])
        ##return "File saved successfully"
        return jsonify(result="file saved")

## read images from folder
def read_images():
    arr = listdir('./known/')
    
    for i in arr:
        k = "./known/"+i
        #print(i.split('.'))
        loaded_imgs[i.split('.')[0]] = face_recognition.load_image_file(k)



def create_enc():
    try:
        for i in loaded_imgs:
            known_faces.append(face_recognition.face_encodings(loaded_imgs[i])[0])
    except IndexError:
        print('Index error occurred')
        quit()


def detect_faces_in_image(file):
    unknown_face = face_recognition.load_image_file(file)
    unknown_face = face_recognition.face_encodings(unknown_face)[0]
    result = face_recognition.compare_faces(known_faces, unknown_face)
    if not True in result:
        print("Matched")
        return False
    else:
        print("Not found")
        return True


@app.route('/predict', methods=['POST'])
def predict():
    
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            return "File not found"

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            ans = detect_faces_in_image(file)
            if(ans == True):
                return jsonify( result='verified' )
            else:
                return jsonify( result='not verified' )


if __name__ == "__main__":

    ## Readinf images from known folder
    read_images()
   
    ## Loading enc in known_faces
    #create_enc()

    app.run(host='0.0.0.0', port=80, debug=True)
    
