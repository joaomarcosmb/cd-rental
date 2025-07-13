from src.models.album import Album
from src.validators import AlbumValidator
from .base_controller import BaseController
from src.config.database import db


class AlbumController(BaseController):
    def __init__(self):
        super().__init__(Album)

    def create_album(self, title, rental_price, artist, genre):
        try:
            album = Album(
                title=title, rental_price=rental_price, artist=artist, genre=genre
            )
            db.session.add(album)
            db.session.commit()
            return album
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating album: {str(e)}")

    def get_album_by_id(self, album_id):
        try:
            album = Album.query.get(album_id)
            if not album:
                raise ValueError(f"Album with ID {album_id} not found")
            return album
        except Exception as e:
            raise Exception(f"Error retrieving album: {str(e)}")

    def get_all_albums(self):
        try:
            return Album.query.all()
        except Exception as e:
            raise Exception(f"Error retrieving albums: {str(e)}")

    def update_album(
        self, album_id, title=None, rental_price=None, artist=None, genre=None
    ):
        try:
            album = self.get_album_by_id(album_id)

            # Validate and update fields if provided
            if title is not None:
                album.title = AlbumValidator.validate_title(title)
            if rental_price is not None:
                album.rental_price = AlbumValidator.validate_rental_price(rental_price)
            if artist is not None:
                album.artist = AlbumValidator.validate_artist(artist)
            if genre is not None:
                album.genre = AlbumValidator.validate_genre(genre)

            db.session.commit()
            return album
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating album: {str(e)}")

    def delete_album(self, album_id):
        try:
            album = self.get_album_by_id(album_id)

            # Check if album has inventory items
            if album.inventory_items.count() > 0:
                raise ValueError("Cannot delete album with existing inventory items")

            db.session.delete(album)
            db.session.commit()
            return True
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting album: {str(e)}")

    def search_albums(self, title=None, artist=None, genre=None):
        try:
            query = Album.query

            if title:
                query = query.filter(Album.title.ilike(f"%{title}%"))
            if artist:
                query = query.filter(Album.artist.ilike(f"%{artist}%"))
            if genre:
                query = query.filter(Album.genre.ilike(f"%{genre}%"))

            return query.all()
        except Exception as e:
            raise Exception(f"Error searching albums: {str(e)}")

    def get_albums_by_artist(self, artist):
        try:
            return Album.query.filter(Album.artist.ilike(f"%{artist}%")).all()
        except Exception as e:
            raise Exception(f"Error retrieving albums by artist: {str(e)}")

    def get_albums_by_genre(self, genre):
        try:
            return Album.query.filter(Album.genre.ilike(f"%{genre}%")).all()
        except Exception as e:
            raise Exception(f"Error retrieving albums by genre: {str(e)}")
