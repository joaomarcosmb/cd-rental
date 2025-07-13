from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.config.database import db


class BaseController:
    def __init__(self, model_class):
        self.model_class = model_class

    def get_all(self):
        try:
            records = self.model_class.query.all()
            return [record.to_dict() for record in records]
        except SQLAlchemyError as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def get_by_id(self, record_id):
        try:
            record = self.model_class.query.get(record_id)
            if not record:
                return {"error": "Record not found"}, 404
            return record.to_dict()
        except SQLAlchemyError as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def create(self):
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Create new instance
            record = self.model_class(**data)

            # Add to database
            db.session.add(record)
            db.session.commit()

            return record.to_dict(), 201
        except IntegrityError as e:
            db.session.rollback()
            return {"error": "Data integrity error", "details": str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500
        except Exception as e:
            db.session.rollback()
            return {"error": "Invalid data provided", "details": str(e)}, 400

    def update(self, record_id):
        try:
            record = self.model_class.query.get(record_id)
            if not record:
                return {"error": "Record not found"}, 404

            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Update record attributes
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db.session.commit()
            return record.to_dict(), 200
        except IntegrityError as e:
            db.session.rollback()
            return {"error": "Data integrity error", "details": str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500
        except Exception as e:
            db.session.rollback()
            return {"error": "Invalid data provided", "details": str(e)}, 400

    def delete(self, record_id):
        try:
            record = self.model_class.query.get(record_id)
            if not record:
                return {"error": "Record not found"}, 404

            db.session.delete(record)
            db.session.commit()

            return {"message": "Record deleted successfully"}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {
                "error": "Cannot delete record due to foreign key constraints",
                "details": str(e),
            }, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500

    # Overridable methods
    def _apply_filters(self, query, filters):
        return query

    def _validate_create_data(self, data):
        return {"valid": True, "errors": []}

    def _validate_update_data(self, data, item):
        return {"valid": True, "errors": []}

    def _create_instance(self, data):
        return self.model_class(**data)

    def _update_instance(self, item, data):
        for key, value in data.items():
            if hasattr(item, key):
                setattr(item, key, value)

    def _can_delete(self, item):
        return {"can_delete": True, "message": ""}
