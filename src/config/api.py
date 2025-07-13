from flask_restx import Api

api = Api(
    version="1.0",
    title="BD Loja API",
    description="A comprehensive API for managing a music store with albums, customers, rentals, and more",
    doc="/docs/", 
    prefix="/api"
)
