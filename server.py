from flask import Flask, render_template, jsonify
from scraping import scrape_twitter_trends

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    # Run the Selenium script
    result = scrape_twitter_trends()
    response=jsonify(result)
    print("HEllo")
    return response

if __name__ == '__main__':
    app.run(debug=True)
