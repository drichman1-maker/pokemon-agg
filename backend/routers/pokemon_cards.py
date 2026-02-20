"""
Pokemon Cards Category Router.
Blueprint for /products endpoints serving seeded product data.
"""

from flask import Blueprint, jsonify
from seed_data import get_all_products, get_product_by_id, get_products_by_category

pokemon_cards_bp = Blueprint('pokemon_cards', __name__, url_prefix='/products')


@pokemon_cards_bp.route('/', methods=['GET'])
def list_products():
    """Return all seeded products."""
    products = get_all_products()
    return jsonify({
        "products": products,
        "total": len(products),
        "category": "pokemon_cards"
    })


@pokemon_cards_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Return a single product by ID."""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": f"Product '{product_id}' not found"}), 404
    return jsonify({"product": product})


@pokemon_cards_bp.route('/category/<category>', methods=['GET'])
def list_by_category(category):
    """Return products filtered by category (e.g., graded, raw, sealed)."""
    products = get_products_by_category(category)
    return jsonify({
        "products": products,
        "total": len(products),
        "category": category
    })
