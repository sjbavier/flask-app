from .. import db
from .. import ma


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    bookmark_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    link = db.Column(db.String(128), unique=True, nullable=False)
    categories_collection = db.relationship('Category', secondary='bookmark_category', back_populates='bookmarks_collection', lazy='joined', join_depth=1)

    def __repr__(self):
        return '<Bookmark %r>' % self.title


class BookmarkSchema(ma.Schema):
    # categories_collection = ma.Nested(categories_schema, many=True)
    class Meta:
        fields = ('bookmark_id', 'title', 'link')


bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    bookmarks_collection = db.relationship('Bookmark', secondary='bookmark_category', back_populates='categories_collection', lazy='joined', join_depth=1)

    def __repr__(self):
        return '%r' % self.name


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('category_id', 'name')


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class BookmarkCategory(db.Model):
    __tablename__ = 'bookmark_category'

    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.bookmark_id'), primary_key=True)
