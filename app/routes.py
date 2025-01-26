from flask import request, jsonify
from flask_restful import Resource
from app.database import firebase_db

class StockAPI(Resource):
    def get(self):
        """
        Handle GET requests to retrieve stock data.
        Query parameters:
        - symbol: Filter by stock symbol (optional)
        - date: Filter by stock date (optional)
        """
        symbol = request.args.get("symbol")
        date = request.args.get("date")

        # Fetch all stock data
        stocks = firebase_db.child("stocks").get()

        if not stocks:
            return jsonify([])

        # Filter stocks based on query parameters
        results = [
            stock for stock in stocks.values()
            if (not symbol or stock.get("symbol") == symbol) and
               (not date or stock.get("date") == date)
        ]

        return jsonify(results)
    
    def post(self):
        """
        Handle POST requests to add stock data.
        Payload example:
        {
            "symbol": "AAPL",
            "date": "2023-12-31",
            "open_price": 150,
            "high": 155,
            "low": 149,
            "close": 154
        }
        """
        data = request.json

        # Push the stock data into the database
        firebase_db.child("stocks").push(data)
        return {"message": "Stock data added successfully!"}, 201

def initialize_routes(api):
    # Register the StockAPI resource
    api.add_resource(StockAPI, '/stocks')
