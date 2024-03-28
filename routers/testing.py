from flask import Blueprint, jsonify, request

testing_router = Blueprint("api testing", __name__)


@testing_router.get("/coba")
async def home_coba():
    return jsonify({"version": "1.0.0"}), 200


@testing_router.get("/coba1/<string:oke>")
async def home_coba1(oke):
    return jsonify({"version": oke}), 200


@testing_router.get("/coba2/<string:oke>")
async def home_coba2(oke):
    data = request.json
    username = data.get("username")
    return jsonify({"version": [oke, username]}), 200
