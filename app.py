from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', name="Võ Công Hiếu", mssv="22dh111085", message="Chào mừng đến với Lab 3")

if __name__ == '__main__':
    app.run(debug=True)
