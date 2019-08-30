from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os as os
from werkzeug import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = '/home/pi/web_server/files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
	
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    app.logger.info(os.getcwd())
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    hists = os.listdir("/files")
    hists = ['files/' + file for file in hists]
    return render_template('gallery.html')


if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0')