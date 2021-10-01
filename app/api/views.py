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
    bookmark_exists = Bookmark.query.filter_by(link=link).first()
    if bookmark_exists:
        return jsonify(msg='Bookmark url already exists'), 409
    else:
        title = request.json['title']
        category = request.json['category']
        created_bookmark = Bookmark.create(title, link, category)
        if created_bookmark:
            return jsonify(msg=f'Bookmark added {title}')
        else:
            return jsonify(msg=f'Bookmark {title} has not been added'), 409
        # bookmark = Bookmark(title=title,link=link)
        # if category and isinstance(category, list):
        #     for c in category:
        #         category_exists = Category.query.filter_by(name=c).first()
        #         if category_exists:
        #             bookmark.categories_collection.append(category_exists)
        #         else:
        #             add_c = Category(name=c)
        #             bookmark.categories_collection.append(add_c)
        #         db.session.add(bookmark)
        #         db.session.commit()
        #     return jsonify(msg=f'Bookmark added {title}')
        # else:
        #     return jsonify(msg=f'Bookmark {title} has improper category field'), 409


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

@api.route('/bookmarks/<int:bookmark_id>', methods=['PUT'])
# @jwt_required()
# @permission_required(Permission.WRITE)
def update_bookmark(bookmark_id: int):
    link = request.json['link']
    bookmark_exists = Bookmark.query.filter_by(bookmark_id=bookmark_id).first()
    if bookmark_exists:
        title = request.json['title']
        category = request.json['category']
        existing_categories = bookmark_exists.categories_collection.all()
        print(existing_categories)
        if category and isinstance(category, list):
            for c in category:
                category_exists = Category.query.filter_by(name=c).first()
                if category_exists:
                    bookmark_exists.categories_collection.append(category_exists)
                else:
                    add_c = Category(name=c)
                    bookmark_exists.categories_collection.append(add_c)
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
    bookmark_exists = Bookmark.query.filter_by(bookmark_id=bookmark_id).first()
    if bookmark_exists:
        db.session.delete(bookmark_exists)
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


