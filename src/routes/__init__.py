from .customer_routes import customer_ns
from .album_routes import album_ns
from .attendant_routes import attendant_ns
from .address_routes import address_ns
from .store_routes import store_ns
from .inventory_item_routes import inventory_item_ns
from .rental_routes import rental_ns
from .payment_routes import payment_ns


def register_namespaces(api_instance):
    api_instance.add_namespace(customer_ns, path="/customers")
    api_instance.add_namespace(album_ns, path="/albums")
    api_instance.add_namespace(attendant_ns, path="/attendants")
    api_instance.add_namespace(address_ns, path="/addresses")
    api_instance.add_namespace(store_ns, path="/stores")
    api_instance.add_namespace(inventory_item_ns, path="/inventory-items")
    api_instance.add_namespace(rental_ns, path="/rentals")
    api_instance.add_namespace(payment_ns, path="/payments")
