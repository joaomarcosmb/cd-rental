from flask_restx import fields
from src.config.api import api

# Base model with common fields
base_model = api.model(
    "BaseModel",
    {
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)


# Customer model
customer_model = api.model(
    "Customer",
    {
        "person_id": fields.String(description="Person UUID"),
        "id": fields.String(description="Person UUID (same as person_id)"),
        "cpf": fields.String(description="CPF"),
        "name": fields.String(description="Full name"),
        "phone": fields.String(description="Phone number"),
        "email": fields.String(description="Email address"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Customer input model
customer_input_model = api.model(
    "CustomerInput",
    {
        "cpf": fields.String(required=True, description="CPF", example="12345678900"),
        "name": fields.String(
            required=True, description="Full name", example="João Silva"
        ),
        "phone": fields.String(
            required=True, description="Phone number", example="11987654321"
        ),
        "email": fields.String(
            required=True, description="Email address", example="joao@email.com"
        ),
    },
)

# Address model
address_model = api.model(
    "Address",
    {
        "id": fields.String(description="Address UUID"),
        "street": fields.String(required=True, description="Street name"),
        "number": fields.String(required=True, description="Street number"),
        "neighborhood": fields.String(required=True, description="Neighborhood"),
        "city": fields.String(required=True, description="City"),
        "state": fields.String(required=True, description="State"),
        "zip_code": fields.String(required=True, description="ZIP code"),
        "customer_id": fields.String(description="Customer UUID"),
        "store_id": fields.String(description="Store UUID"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Address input model
address_input_model = api.model(
    "AddressInput",
    {
        "street": fields.String(required=True, description="Street name"),
        "number": fields.String(required=True, description="Street number"),
        "neighborhood": fields.String(required=True, description="Neighborhood"),
        "city": fields.String(required=True, description="City"),
        "state": fields.String(required=True, description="State"),
        "zip_code": fields.String(required=True, description="ZIP code"),
        "customer_id": fields.String(description="Customer UUID"),
        "store_id": fields.String(description="Store UUID"),
    },
)

# Album model
album_model = api.model(
    "Album",
    {
        "id": fields.String(description="Album UUID"),
        "title": fields.String(required=True, description="Album title"),
        "artist": fields.String(required=True, description="Artist name"),
        "genre": fields.String(required=True, description="Music genre"),
        "rental_price": fields.Float(required=True, description="Rental price"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Album input model
album_input_model = api.model(
    "AlbumInput",
    {
        "title": fields.String(
            required=True, description="Album title", example="Abbey Road"
        ),
        "artist": fields.String(
            required=True, description="Artist name", example="The Beatles"
        ),
        "genre": fields.String(
            required=True, description="Music genre", example="Rock"
        ),
        "rental_price": fields.Float(
            required=True, description="Rental price", example=15.99
        ),
    },
)

# Store model
store_model = api.model(
    "Store",
    {
        "id": fields.String(description="Store UUID"),
        "cnpj": fields.String(required=True, description="Store CNPJ"),
        "trade_name": fields.String(required=True, description="Store trade name"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Store input model
store_input_model = api.model(
    "StoreInput",
    {
        "cnpj": fields.String(
            required=True, description="Store CNPJ", example="12345678000195"
        ),
        "trade_name": fields.String(
            required=True, description="Store trade name", example="Music World Store"
        ),
    },
)

# Inventory Item model
inventory_item_model = api.model(
    "InventoryItem",
    {
        "id": fields.String(description="Inventory Item UUID"),
        "album_id": fields.String(required=True, description="Album UUID"),
        "store_id": fields.String(required=True, description="Store UUID"),
        "barcode": fields.String(required=True, description="Item barcode"),
        "status": fields.String(
            required=True,
            description="Item status",
            enum=["available", "rented", "maintenance", "damaged", "lost"],
        ),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Inventory Item input model
inventory_item_input_model = api.model(
    "InventoryItemInput",
    {
        "album_id": fields.String(
            required=True, description="Album UUID", example="ALBUM_ID_HERE"
        ),
        "store_id": fields.String(
            required=True, description="Store UUID", example="STORE_ID_HERE"
        ),
        "barcode": fields.String(
            required=True, description="Item barcode", example="123456789012"
        ),
        "status": fields.String(
            required=True,
            description="Item status",
            enum=["available", "rented", "maintenance", "damaged", "lost"],
            example="available",
        ),
    },
)

# Attendant model
attendant_model = api.model(
    "Attendant",
    {
        "person_id": fields.String(description="Person UUID"),
        "store_id": fields.String(description="Store UUID"),
        "id": fields.String(description="Person UUID (same as person_id)"),
        "cpf": fields.String(description="CPF"),
        "name": fields.String(description="Full name"),
        "phone": fields.String(description="Phone number"),
        "email": fields.String(description="Email address"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Attendant input model
attendant_input_model = api.model(
    "AttendantInput",
    {
        "cpf": fields.String(required=True, description="CPF", example="12345678900"),
        "name": fields.String(
            required=True, description="Full name", example="João Silva"
        ),
        "phone": fields.String(
            required=True, description="Phone number", example="11987654321"
        ),
        "email": fields.String(
            required=True, description="Email address", example="joao@email.com"
        ),
        "store_id": fields.String(required=True, description="Store UUID"),
    },
)

# Rental model
rental_model = api.model(
    "Rental",
    {
        "id": fields.String(description="Rental UUID"),
        "customer_id": fields.String(required=True, description="Customer UUID"),
        "attendant_id": fields.String(required=True, description="Attendant UUID"),
        "item_id": fields.String(required=True, description="Inventory Item UUID"),
        "rental_date": fields.DateTime(required=True, description="Rental date"),
        "return_date": fields.DateTime(description="Return date"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Rental input model
rental_input_model = api.model(
    "RentalInput",
    {
        "customer_id": fields.String(required=True, description="Customer UUID"),
        "attendant_id": fields.String(required=True, description="Attendant UUID"),
        "item_id": fields.String(required=True, description="Inventory Item UUID"),
        "rental_date": fields.DateTime(required=True, description="Rental date"),
        "return_date": fields.DateTime(description="Return date"),
    },
)

# Payment model
payment_model = api.model(
    "Payment",
    {
        "id": fields.String(description="Payment UUID"),
        "rental_id": fields.String(required=True, description="Rental UUID"),
        "amount": fields.Float(required=True, description="Payment amount"),
        "payment_method": fields.String(required=True, description="Payment method"),
        "status": fields.String(required=True, description="Payment status"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

# Payment input model
payment_input_model = api.model(
    "PaymentInput",
    {
        "rental_id": fields.String(required=True, description="Rental UUID"),
        "amount": fields.Float(required=True, description="Payment amount"),
        "payment_method": fields.String(required=True, description="Payment method"),
        "status": fields.String(required=True, description="Payment status"),
    },
)

# Error model
error_model = api.model(
    "Error",
    {
        "message": fields.String(required=True, description="Error message"),
        "code": fields.Integer(description="Error code"),
    },
)

# Success message model
success_model = api.model(
    "Success",
    {
        "message": fields.String(required=True, description="Success message"),
        "data": fields.Raw(description="Response data"),
    },
)
