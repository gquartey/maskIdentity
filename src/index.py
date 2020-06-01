import flask
from flask import request, jsonify, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
from scripts import videoTransform as vd
from os import path


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/' + 'data/upload'
app.config['DOWNLOAD_FOLDER'] = os.getcwd() + '/' + 'data/return-files'


@app.route('/', methods = ['GET'])
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      secure_file = secure_filename(f.filename)
      input_path = app.config['UPLOAD_FOLDER'] + '/' + secure_file
      output_path = app.config['DOWNLOAD_FOLDER'] + '/' + secure_file
      out_path = 'data/return-files/' + secure_file
      f.save(input_path)

      # create and save transformed video
      vd.serverVideoTransform(input_path,output_path)

      # return file to user 
      try:
         print("Check if a file exists : ",path.exists(output_path))
         return send_file(
            output_path,
            attachment_filename='blurred.mp4',
            mimetype='video/mp4',
            as_attachment=True)
         # return 'file processed successfully'
      except Exception as e:
         return str(e)
      # return 'file uploaded successfully'
    


if __name__ == '__main__':
   app.run(debug = True)