from flask import jsonify


async def handle_429(error):
    return jsonify({"message": "Too Many Requests", "status_code": 429}), 429


async def handle_404(error):
    return jsonify({"message": "Endpoint not found", "status_code": 404}), 404


async def handle_415(error):
    return jsonify({"message": "Unsupported Media Type", "status_code": 415}), 415


async def handle_400(error):
    return jsonify({"message": "Bad Request", "status_code": 400}), 400
