from flask import render_template
from flask import current_app as app
from flask import request


@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='Graph MSXV Telemetry Data',
        description='Fetches telemetry data and graphs it',
        template='home-template',
        body="This is a homepage served with Flask."
    )


@app.route('/test', methods=['POST'])
def test():
    """Landing page."""
    text = request.form['text']
    return text