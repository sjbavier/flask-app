from .. import db
from . import api
from ..models.bookmark import BookmarkSchema, CategorySchema
from app.models.bookmark import Bookmark, Category
from flask import jsonify


bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@api.route('/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks_list = Bookmark.query.all()
    result = bookmarks_schema.dump(bookmarks_list)
    return jsonify(result)


@api.route('/categories', methods=['GET'])
def categories():
    categories_list = Category.query.all()
    results = categories_schema.dump(categories_list)
    return jsonify(results)