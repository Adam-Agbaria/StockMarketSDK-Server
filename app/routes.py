from flask import request, jsonify
from flask_restful import Resource
from app.database import firebase_db
from datetime import datetime

class StockAPI(Resource):
    def get(self):
        """
        Handle GET requests to retrieve cryptocurrency data.
        Query parameters:
        - crypto: Cryptocurrency symbol (e.g., BTC, ETH, BNB) (required).
        - timeframe: Timeframe for data (daily, weekly, monthly) (required).
        - start_date: Start date for range (optional, format YYYY-MM-DD).
        - end_date: End date for range (optional, format YYYY-MM-DD).
        """
        # Get query parameters
        crypto = request.args.get("crypto")
        timeframe = request.args.get("timeframe")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # Validate required parameters
        if not crypto or not timeframe:
            return {"error": "Both 'crypto' and 'timeframe' parameters are required."}, 400

        # Reference the database node for the specified cryptocurrency and timeframe
        data_ref = firebase_db.child("cryptocurrencies").child(crypto).child(timeframe)
        data = data_ref.get()

        if not data:
            return {"error": f"No data found for {crypto} in {timeframe} timeframe."}, 404

        # Filter data by date range
        filtered_data = {}
        if start_date or end_date:
            for date, values in data.items():
                if start_date and date < start_date:
                    continue
                if end_date and date > end_date:
                    continue
                filtered_data[date] = values
        else:
            filtered_data = data

        return jsonify(filtered_data)


def initialize_routes(api):
    api.add_resource(StockAPI, '/stocks')
