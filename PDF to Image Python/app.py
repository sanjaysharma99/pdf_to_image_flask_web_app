from flask import *
from distutils.log import debug
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from os.path import basename
import fitz
from zipfile import ZipFile

app=Flask(__name__,static_folder='static')

app.config["UPLOAD_FOLDER"] = "upload/"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/convert', methods = ['POST'])  
def convert():  
    if request.method == 'POST':  
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)  

        file=fitz.open('upload/'+filename)
        global zipname
        zipname,ftype=filename.split('.')
        zipObj=ZipFile(f'static/zipfile/{zipname}.zip', 'w')
        i=0
        for page in file:
            img=page.get_pixmap()
            img.save(f'static/images/image_{i}.png')
            zipObj.write(f'static/images/image_{i}.png')
            i+=1

        return render_template('download.html')

@app.route('/download',methods=['POST'])
def download():
     return send_file(f'static/zipfile/{zipname}.zip', as_attachment=True)


app.run()