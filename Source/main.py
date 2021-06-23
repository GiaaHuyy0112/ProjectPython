from flask import Flask, render_template, send_from_directory, Response, request
import predict
import cv2
import os


app = Flask(__name__)

@app.route('/<page>')
def hello_world(page=None):
    grenade = len(os.listdir('static/data/train/Grenade/'))
    knives = len(os.listdir('static/data/train/Knives/'))
    machineguns = len(os.listdir('static/data/train/Machine Guns/'))
    pistol = len(os.listdir('static/data/train/Pistol Hand Guns/'))
    arr = {"Grenade":grenade, "Knives":knives, "Machine Guns": machineguns, "Pistol Hand Guns": pistol}
    return render_template('template.html', page=page, arr=arr)

@app.errorhandler(404)
def page_not_found(error):
   return render_template('template.html', page = '404'), 404



@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return render_template("template.html", uploaded_image=image.filename, page="main")
    return render_template("template.html", page="main")


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


if __name__ == '__main__':
    app.run(debug=True)