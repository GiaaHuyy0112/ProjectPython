from flask import Flask, render_template, send_file, Response
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




if __name__ == '__main__':
    app.run()