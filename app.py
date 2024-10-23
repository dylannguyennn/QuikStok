from flask import Flask, render_template, request
from posts import search_ticker

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    ticker = request.form.get('ticker', '').strip().upper()
    print(ticker)
    return(search_ticker(ticker))
    