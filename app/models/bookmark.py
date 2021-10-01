from .. import db
from .. import ma
from marshmallow import fields
from sqlalchemy import event


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    bookmark_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    link = db.Column(db.String(128), unique=True, nullable=False)
    categories_collection = db.relationship('Category', secondary='bookmark_category',
                                            back_populates='bookmarks_collection', lazy='dynamic',
                                            join_depth=1)

    def __repr__(self):
        return '<Bookmark %r>' % self.title


class BookmarkSchema(ma.Schema):
    bookmark_id = fields.Integer()
    title = fields.String()
    link = fields.String()
    categories_collection = fields.Nested(lambda: CategorySchema(only=('category_id', 'name',)), many=True)


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    bookmarks_collection = db.relationship('Bookmark', secondary='bookmark_category',
                                           back_populates='categories_collection', lazy='dynamic',
                                           join_depth=1)

    def __repr__(self):
        return '<Category %r>' % self.name


class CategorySchema(ma.Schema):
    category_id = fields.Integer()
    name = fields.String()
    bookmarks_collection = fields.Nested(lambda: BookmarkSchema(only=('bookmark_id', 'title', 'link')), many=True)


class BookmarkCategory(db.Model):
    __tablename__ = 'bookmark_category'

    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id', ondelete='CASCADE'), primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.bookmark_id', ondelete='CASCADE'), primary_key=True)


@event.listens_for(db.Session, 'after_flush')
def delete_category_orphans(session, ctx):
    session.query(Category)\
        .filter(~Category.bookmarks_collection.any())\
        .delete(synchronize_session=False)