from previsaoligas import app
from flask import Flask, render_template, request
import config  # Import the configuration file
import stripe

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
app.config.from_object('config')

stripe.api_key = app.config['STRIPE_SECRET_KEY']