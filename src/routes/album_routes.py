from flask_restx import Namespace, Resource
from flask import request
from flask_restx.api import HTTPStatus
from src.controllers.album_controller import AlbumController
from src.models.swagger_models import (
    album_model,
    album_input_model,
    error_model,
    success_model,
)

# Create namespace for albums
album_ns = Namespace("albums", description="Album operations")
album_controller = AlbumController()


@album_ns.route("")
class AlbumList(Resource):
    @album_ns.doc("get_all_albums")
    @album_ns.marshal_list_with(album_model)
    @album_ns.response(200, "Success", [album_model])
    @album_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all albums"""
        return album_controller.get_all()

    @album_ns.doc("create_album")
    @album_ns.expect(album_input_model)
    @album_ns.marshal_with(album_model, code=HTTPStatus.CREATED)
    @album_ns.response(201, "Album created successfully", album_model)
    @album_ns.response(400, "Invalid input", error_model)
    @album_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new album"""
        return album_controller.create()


@album_ns.route("/<uuid:album_id>")
@album_ns.param("album_id", "Album UUID")
class Album(Resource):
    @album_ns.doc("get_album_by_id")
    @album_ns.marshal_with(album_model)
    @album_ns.response(200, "Success", album_model)
    @album_ns.response(404, "Album not found", error_model)
    @album_ns.response(500, "Internal Server Error", error_model)
    def get(self, album_id):
        """Get album by ID"""
        return album_controller.get_by_id(album_id)

    @album_ns.doc("update_album")
    @album_ns.expect(album_input_model)
    @album_ns.marshal_with(album_model)
    @album_ns.response(200, "Album updated successfully", album_model)
    @album_ns.response(404, "Album not found", error_model)
    @album_ns.response(400, "Invalid input", error_model)
    @album_ns.response(500, "Internal Server Error", error_model)
    def put(self, album_id):
        """Update album by ID"""
        return album_controller.update(album_id)

    @album_ns.doc("delete_album")
    @album_ns.response(200, "Album deleted successfully", success_model)
    @album_ns.response(404, "Album not found", error_model)
    @album_ns.response(500, "Internal Server Error", error_model)
    def delete(self, album_id):
        """Delete album by ID"""
        return album_controller.delete(album_id)


@album_ns.route("/search")
class AlbumSearch(Resource):
    @album_ns.doc("search_albums")
    @album_ns.param("title", "Search by album title")
    @album_ns.param("artist", "Search by artist name")
    @album_ns.param("genre", "Search by genre")
    @album_ns.marshal_list_with(album_model)
    @album_ns.response(200, "Success", [album_model])
    @album_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Search albums by title, artist, or genre"""
        try:
            title = request.args.get("title")
            artist = request.args.get("artist")
            genre = request.args.get("genre")

            albums = album_controller.search_albums(
                title=title, artist=artist, genre=genre
            )
            return {"albums": [album.to_dict() for album in albums]}, 200
        except Exception as e:
            return {"error": str(e)}, 500


@album_ns.route("/artist/<string:artist>")
@album_ns.param("artist", "Artist name")
class AlbumsByArtist(Resource):
    @album_ns.doc("get_albums_by_artist")
    @album_ns.marshal_list_with(album_model)
    @album_ns.response(200, "Success", [album_model])
    @album_ns.response(500, "Internal Server Error", error_model)
    def get(self, artist):
        """Get albums by artist"""
        try:
            albums = album_controller.get_albums_by_artist(artist)
            return {"albums": [album.to_dict() for album in albums]}, 200
        except Exception as e:
            return {"error": str(e)}, 500


@album_ns.route("/genre/<string:genre>")
@album_ns.param("genre", "Genre name")
class AlbumsByGenre(Resource):
    @album_ns.doc("get_albums_by_genre")
    @album_ns.marshal_list_with(album_model)
    @album_ns.response(200, "Success", [album_model])
    @album_ns.response(500, "Internal Server Error", error_model)
    def get(self, genre):
        """Get albums by genre"""
        try:
            albums = album_controller.get_albums_by_genre(genre)
            return {"albums": [album.to_dict() for album in albums]}, 200
        except Exception as e:
            return {"error": str(e)}, 500
