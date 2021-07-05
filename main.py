from flask import Flask, render_template
from fit import get_mlp
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/predict')
def predict():
    return "HEllo Workd"
if __name__ == '__main__':
   app.run(debug=False)