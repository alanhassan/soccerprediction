from previsaoligas import app
import os
import stripe

stripe.api_key = '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'

if __name__ == '__main__':
    app.run(debug=True)


