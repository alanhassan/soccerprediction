from previsaoligas import app
import os
import stripe
from dotenv import load_dotenv
import os


load_dotenv()

stripe.api_key = os.getenv('stripe_api_key')

if __name__ == '__main__':
    app.run(debug=True)


