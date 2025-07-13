from src.models.inventory_item import InventoryItem
from src.models.album import Album
from src.models.store import Store
from src.validators import InventoryItemValidator
from .base_controller import BaseController
from src.config.database import db


class InventoryItemController(BaseController):
    def __init__(self):
        super().__init__(InventoryItem)

    def create_inventory_item(self, barcode, album_id, store_id, status="available"):
        try:
            # Verify album and store exist
            album = Album.query.get(album_id)
            if not album:
                raise ValueError(f"Album with ID {album_id} not found")

            store = Store.query.get(store_id)
            if not store:
                raise ValueError(f"Store with ID {store_id} not found")

            inventory_item = InventoryItem(
                barcode=barcode, album_id=album_id, store_id=store_id, status=status
            )
            db.session.add(inventory_item)
            db.session.commit()
            return inventory_item
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating inventory item: {str(e)}")

    def get_inventory_item_by_id(self, item_id):
        try:
            item = InventoryItem.query.get(item_id)
            if not item:
                raise ValueError(f"Inventory item with ID {item_id} not found")
            return item
        except Exception as e:
            raise Exception(f"Error retrieving inventory item: {str(e)}")

    def get_inventory_item_by_barcode(self, barcode):
        try:
            item = InventoryItem.query.filter(InventoryItem.barcode == barcode).first()
            if not item:
                raise ValueError(f"Inventory item with barcode {barcode} not found")
            return item
        except Exception as e:
            raise Exception(f"Error retrieving inventory item: {str(e)}")

    def get_all_inventory_items(self):
        try:
            return InventoryItem.query.all()
        except Exception as e:
            raise Exception(f"Error retrieving inventory items: {str(e)}")

    def get_inventory_items_by_store(self, store_id):
        try:
            return InventoryItem.query.filter(InventoryItem.store_id == store_id).all()
        except Exception as e:
            raise Exception(f"Error retrieving inventory items by store: {str(e)}")

    def get_inventory_items_by_album(self, album_id):
        try:
            return InventoryItem.query.filter(InventoryItem.album_id == album_id).all()
        except Exception as e:
            raise Exception(f"Error retrieving inventory items by album: {str(e)}")

    def get_inventory_items_by_status(self, status):
        try:
            return InventoryItem.query.filter(InventoryItem.status == status).all()
        except Exception as e:
            raise Exception(f"Error retrieving inventory items by status: {str(e)}")

    def get_available_items(self, album_id=None, store_id=None):
        try:
            query = InventoryItem.query.filter(InventoryItem.status == "available")

            if album_id:
                query = query.filter(InventoryItem.album_id == album_id)
            if store_id:
                query = query.filter(InventoryItem.store_id == store_id)

            return query.all()
        except Exception as e:
            raise Exception(f"Error retrieving available items: {str(e)}")

    def update_inventory_item_status(self, item_id, status):
        try:
            item = self.get_inventory_item_by_id(item_id)

            # Validate status
            validated_status = InventoryItemValidator.validate_status(status)
            item.status = validated_status

            db.session.commit()
            return item
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating inventory item status: {str(e)}")

    def update_inventory_item(
        self, item_id, barcode=None, album_id=None, store_id=None, status=None
    ):
        try:
            item = self.get_inventory_item_by_id(item_id)

            # Validate and update fields if provided
            if barcode is not None:
                item.barcode = InventoryItemValidator.validate_barcode(barcode)
            if album_id is not None:
                # Verify album exists
                album = Album.query.get(album_id)
                if not album:
                    raise ValueError(f"Album with ID {album_id} not found")
                item.album_id = InventoryItemValidator.validate_album_id(album_id)
            if store_id is not None:
                # Verify store exists
                store = Store.query.get(store_id)
                if not store:
                    raise ValueError(f"Store with ID {store_id} not found")
                item.store_id = InventoryItemValidator.validate_store_id(store_id)
            if status is not None:
                item.status = InventoryItemValidator.validate_status(status)

            db.session.commit()
            return item
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating inventory item: {str(e)}")

    def delete_inventory_item(self, item_id):
        try:
            item = self.get_inventory_item_by_id(item_id)

            # Check if item has active rentals
            if item.rentals.filter_by(return_date=None).count() > 0:
                raise ValueError("Cannot delete inventory item with active rentals")

            db.session.delete(item)
            db.session.commit()
            return True
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting inventory item: {str(e)}")

    def rent_item(self, item_id):       
        try:
            item = self.get_inventory_item_by_id(item_id)

            if item.status != "available":
                raise ValueError(
                    f"Item is not available for rental (current status: {item.status})"
                )

            item.status = "rented"
            db.session.commit()
            return item
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error renting item: {str(e)}")

    def return_item(self, item_id): 
        try:
            item = self.get_inventory_item_by_id(item_id)

            if item.status != "rented":
                raise ValueError(
                    f"Item is not currently rented (current status: {item.status})"
                )

            item.status = "available"
            db.session.commit()
            return item
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error returning item: {str(e)}")
