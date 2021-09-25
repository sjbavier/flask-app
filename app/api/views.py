from .. import db
from . import api
from ..models.bookmark import BookmarkSchema, CategorySchema
from app.models.bookmark import Bookmark, Category
from flask import jsonify
from app import jwt_required, request
from app.auth.decorators import permission_required, debug
from app.models.user import Permission

bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


# ///////////////////
# Create Bookmarks
# ///////////////////

@api.route('/bookmarks', methods=['POST'])
@jwt_required()
@permission_required(Permission.WRITE)
def create_bookmark():
    link = request.json['link']
    test_bookmark = Bookmark.query.filter_by(link=link).first()
    if test_bookmark:
        return jsonify(msg='Bookmark url already exists'), 409
    else:
        title = request.json['title']
        category = request.json['category']
        bookmark = Bookmark(title=title,link=link)
        if category and isinstance(category, list):
            for c in category:
                test_category = Category.query.filter_by(name=c).first()
                if test_category:
                    bookmark.categories_collection.append(test_category)
                else:
                    add_c = Category(name=c)
                    bookmark.categories_collection.append(add_c)
                db.session.add(bookmark)
                db.session.commit()
            return jsonify(msg=f'Bookmark added {title}')
        else:
            return jsonify(msg=f'Bookmark {title} has improper category field'), 409


# ///////////////////
# Read Bookmarks
# ///////////////////

@api.route('/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks_list = Bookmark.query.all()
    result = bookmarks_schema.dump(bookmarks_list)
    return jsonify(result)


# ///////////////////
# Update Bookmarks
# ///////////////////

@api.route('/bookmarks/', methods=['PUT'])
@jwt_required()
@permission_required(Permission.WRITE)
def delete_bookmark():
    link = request.json['link']
    test_bookmark = Bookmark.query.filter_by(link=link).first()
    if test_bookmark:
        title = request.json['title']
        category = request.json['category']
        test_bookmark.title = title
        test_bookmark.link = link
        if category and isinstance(category, list):
            for c in category:
                test_category = Category.query.filter_by(name=c).first()
                if test_category:
                    test_bookmark.categories_collection.append(test_category)
                else:
                    add_c = Category(name=c)
                    test_bookmark.categories_collection.append(add_c)
                db.session.commit()
            return jsonify(msg=f'Bookmark updated {title}')
        else:
            return jsonify(msg=f'Bookmark {title} has improper category field'), 409
    else:
        return jsonify(msg='Bookmark url already exists'), 409


# ///////////////////
# Delete Bookmarks
# ///////////////////

@api.route('/bookmarks/<int:bookmark_id>', methods=['DELETE'])
@jwt_required()
@permission_required(Permission.EXECUTE)
def delete_bookmark(bookmark_id: int):
    bookmark = Bookmark.query.filter_by(bookmark_id=bookmark_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify(message='deleted a bookmark'), 202
    else:
        return jsonify(message='bookmark does not exist'), 404


# ///////////////////
# Read Categories
# ///////////////////

@api.route('/categories', methods=['GET'])
def categories():
    categories_list = Category.query.all()
    results = categories_schema.dump(categories_list)
    return jsonify(results)


