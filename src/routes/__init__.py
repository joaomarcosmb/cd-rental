from .person_routes import person_bp
from .customer_routes import customer_bp
from .attendant_routes import attendant_bp
from .address_routes import address_bp
from .store_routes import store_bp
from .album_routes import album_bp
from .inventory_item_routes import inventory_item_bp
from .rental_routes import rental_bp
from .payment_routes import payment_bp


def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(person_bp, url_prefix="/api/persons")
    app.register_blueprint(customer_bp, url_prefix="/api/customers")
    app.register_blueprint(attendant_bp, url_prefix="/api/attendants")
    app.register_blueprint(address_bp, url_prefix="/api/addresses")
    app.register_blueprint(store_bp, url_prefix="/api/stores")
    app.register_blueprint(album_bp, url_prefix="/api/albums")
    app.register_blueprint(inventory_item_bp, url_prefix="/api/inventory-items")
    app.register_blueprint(rental_bp, url_prefix="/api/rentals")
    app.register_blueprint(payment_bp, url_prefix="/api/payments")
