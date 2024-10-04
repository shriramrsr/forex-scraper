# api/main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models import get_average_rate, get_closing_rate
from config import CURRENCY_PAIRS

app = Flask(__name__)
CORS(app)

@app.route('/api/average_rate', methods=['POST'])
def average_rate():
    data = request.json
    base_currency = data.get('base_currency')
    quote_currency = data.get('quote_currency')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()

    # if (base_currency, quote_currency) not in CURRENCY_PAIRS:
    #     return jsonify({"error": "Invalid currency pair"}), 400
    
    avg_rate = get_average_rate(
        base_currency,
        quote_currency,
        start_date,
        end_date
    )
    
    if avg_rate is None:
        return jsonify({"note": "No data found for the specified period"}), 201
    
    return jsonify({"average_rate": avg_rate}), 200

@app.route('/api/closing_rate', methods=['POST'])
def closing_rate():
    data = request.json
    base_currency = data.get('base_currency')
    quote_currency = data.get('quote_currency')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()

    # if (base_currency, quote_currency) not in CURRENCY_PAIRS:
    #     return jsonify({"error": "Invalid currency pair"}), 400
    
    close_rate = get_closing_rate(
        base_currency,
        quote_currency,
        date
    )
    
    if close_rate is None:
        return jsonify({"error": "No data found for the specified date"}), 404
    
    return jsonify({"closing_rate": close_rate})

# This function will be called from main.py to create the Flask app
def create_app():
    return app