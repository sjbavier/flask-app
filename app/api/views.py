from .. import db
from . import api
from ..models.bookmark import Bookmark, bookmark_schema, bookmarks_schema, Category, categories_schema
from flask import jsonify


@api.route('/api/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks_list = Bookmark.query.all()
    result = bookmarks_schema.dump(bookmarks_list)
    return jsonify(result)


@api.route('/api/categories', methods=['GET'])
def categories():
    categories_list = Category.query.all()
    results = categories_schema.dump(categories_list)
    return jsonify(results)