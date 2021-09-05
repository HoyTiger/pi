import datetime
import os

from flask import Flask, render_template, Response, request, json

from camera.cameraVideo import *

camera_ = VideoCamera()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('creat_face.html')


@app.route('/to_creat_face')
def to_creat_face():
    return render_template('creat_face.html')


@app.route('/to_recognize')
def to_recognize():
    return render_template('recognize.html')


@app.route("/make_face")
def make_face():
    data = request.args.get('data')
    data = json.loads(data)
    name = data['username']
    path = ''
    filename = '0'
    if os.path.exists('./label.txt'):
        with open('./label.txt', 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
        if name not in load_dict:
            path = str(len(load_dict))
            load_dict[name] = str(len(load_dict))
            with open('./label.txt', 'w', encoding='utf-8') as f:
                json.dump(load_dict, f, encoding='utf-8')
        else:
            path = load_dict[name]
    else:
        path = "0"
        with open('./label.txt', 'w', encoding='utf-8') as f:
            json.dump({name: "0"}, f, encoding='utf-8')

    path = os.path.join('./static/datasets', path)
    if not os.path.exists(path):
        os.makedirs(path)
    _, img = camera_.get_face_frame()
    cv2.imwrite(os.path.join(path, datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'), img)

    return render_template('creat_face.html')


@app.route("/save_face")
def save_face():

    path = 'static/output'

    if not os.path.exists(path):
        os.makedirs(path)
    _, img = camera_.get_Recognizer_frame()
    cv2.imwrite(os.path.join(path, datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'), img)

    return render_template('recognize.html')

@app.route('/pi_camera')
def pi_camera():
    return Response(gen(camera_),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pi_camera2')
def pi_camera2():
    return Response(gen2(camera_),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print(os.getcwd())
    app.run(debug=True)
