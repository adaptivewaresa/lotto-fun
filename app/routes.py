from flask import Blueprint, jsonify
from app.services import generate_pen_lotto_numbers
from app.fun_facts import get_random_fun_fact

api_bp = Blueprint('api', __name__)


@api_bp.route('/', methods=['GET'])
def home():
    """Base route returning fun facts about the app."""
    return jsonify({
        "title": "Lottoscope - Like Horoscope",
        "description": "A lotto number generator based on pseudo-random algorithms and frequency analysis.",
        "fun_fact": get_random_fun_fact(),
        "disclaimer": "Gambling is addictive. This is just a fun project created out of boredom. Values generated here are likely to lose you money!"
    })


@api_bp.route('/generate', methods=['GET'])
def generate():
    """Endpoint to generate lotto numbers."""
    result = generate_pen_lotto_numbers()
    return jsonify(result)
