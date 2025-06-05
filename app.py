from flask import Flask, request, redirect, url_for, render_template_string
import os
from git import Repo
import shutil

UPLOAD_FOLDER = 'uploads'
GIT_REPO_FOLDER = 'repo'
GITHUB_REPO_URL = 'https://github.com/Vchieu004/flask.git'  # Thay bằng repo của bạn

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tạo thư mục nếu chưa có
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GIT_REPO_FOLDER, exist_ok=True)

# Clone repo nếu chưa clone
if not os.path.exists(os.path.join(GIT_REPO_FOLDER, '.git')):
    Repo.clone_from(GITHUB_REPO_URL, GIT_REPO_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return 'No selected file'

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(filepath)

        # Copy file vào repo
        dest_path = os.path.join(GIT_REPO_FOLDER, uploaded_file.filename)
        shutil.copy(filepath, dest_path)

        # Push file lên GitHub
        repo = Repo(GIT_REPO_FOLDER)
        repo.git.add(uploaded_file.filename)
        repo.index.commit(f"Upload {uploaded_file.filename}")
        origin = repo.remote(name='origin')
        origin.push()

        return f'File {uploaded_file.filename} uploaded and pushed to GitHub!'
    
    # Giao diện đơn giản
    return render_template_string("""
        <!doctype html>
        <title>Upload File to GitHub</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
