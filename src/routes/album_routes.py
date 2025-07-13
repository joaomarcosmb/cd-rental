from flask import Blueprint, request
from src.controllers.album_controller import AlbumController

album_bp = Blueprint("album", __name__)
album_controller = AlbumController()


@album_bp.route("", methods=["GET"])
def get_all_albums():
    """Get all albums."""
    return album_controller.get_all()


@album_bp.route("/<uuid:album_id>", methods=["GET"])
def get_album_by_id(album_id):
    """Get album by ID."""
    return album_controller.get_by_id(album_id)


@album_bp.route("", methods=["POST"])
def create_album():
    """Create a new album."""
    return album_controller.create()


@album_bp.route("/<uuid:album_id>", methods=["PUT"])
def update_album(album_id):
    """Update album by ID."""
    return album_controller.update(album_id)


@album_bp.route("/<uuid:album_id>", methods=["DELETE"])
def delete_album(album_id):
    """Delete album by ID."""
    return album_controller.delete(album_id)


@album_bp.route("/search", methods=["GET"])
def search_albums():
    """Search albums by title, artist, or genre."""
    try:
        title = request.args.get("title")
        artist = request.args.get("artist")
        genre = request.args.get("genre")

        albums = album_controller.search_albums(title=title, artist=artist, genre=genre)
        return {"albums": [album.to_dict() for album in albums]}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@album_bp.route("/artist/<string:artist>", methods=["GET"])
def get_albums_by_artist(artist):
    """Get albums by artist."""
    try:
        albums = album_controller.get_albums_by_artist(artist)
        return {"albums": [album.to_dict() for album in albums]}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@album_bp.route("/genre/<string:genre>", methods=["GET"])
def get_albums_by_genre(genre):
    """Get albums by genre."""
    try:
        albums = album_controller.get_albums_by_genre(genre)
        return {"albums": [album.to_dict() for album in albums]}, 200
    except Exception as e:
        return {"error": str(e)}, 500
