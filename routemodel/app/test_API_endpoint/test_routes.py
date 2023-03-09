from flask import Flask, request, render_template
import csv

csv_dir = "../sample_route_step4.csv"

app = Flask(__name__)

@app.route('/')
def hello_name():
    return render_template('test_template.html')


@app.route('/csv', methods=['GET'])
def get_csv():
    csv_file = open(csv_dir)

    return csv_file


if __name__ == '__main__':
    app.run(port=8000, debug=True)