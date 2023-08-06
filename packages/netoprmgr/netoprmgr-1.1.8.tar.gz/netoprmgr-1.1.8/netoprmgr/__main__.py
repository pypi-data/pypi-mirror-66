import os
import pkg_resources
from flask import Flask, render_template

import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = pkg_resources.resource_filename('netoprmgr', '')
os.chdir(BASE_DIR)
CAPT_DIR = os.path.join(BASE_DIR,'capture')

ALLOWED_EXTENSIONS = set(['txt', 'log',])

app.secret_key = "!qw3ezxc7gsj4nn1j23kkf9"
app.config['UPLOAD_FOLDER'] = CAPT_DIR

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/log/upload")
def log_upload_page():
    return render_template('log_upload_page.html')
    #return (os.path.join(os.getcwd(),'capture'))

@app.route('/log/upload', methods=['POST'])
def log_upload():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('Logs successfully uploaded')
		return redirect('/log/upload')

@app.route('/report/generate')
def report_generate_page():
	return render_template('report_generate.html')

@app.route('/report/result')
def report_generate():
	from main_cli import MainCli
	MainCli.createReport()
	return render_template('report_download.html')

@app.route('/env/generate')
def env_generate_page():
	return render_template('env_generate.html')

@app.route('/env/result')
def env_generate():
	from main_cli import MainCli
	MainCli.showEnvironment()
	return render_template('env_download.html')

@app.route('/log')
def log_delete_page():
	return render_template('log_delete.html')

@app.route('/log/delete')
def log_delete():
	from main_cli import MainCli
	MainCli.deleteCapture()
	return redirect('/log/upload')

if __name__ == "__main__":
    app.run(debug=True)