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

    @staticmethod
    def create(title: str, link: str, categories: list):
        """
        static method: accepts title str, link str and categories list
        returns True or False if creation was successful
        """
        bookmark_exists = Bookmark.query.filter_by(link=link).first()
        if bookmark_exists:
            return False
        else:
            bookmark = Bookmark(title=title,link=link)
            if categories and isinstance(categories, list):
                for category in categories:
                    Category.create(category, bookmark)
                return True
            else:
                return False

    def flush_categories(self):
        """
        removes the categories_collection items
        """
        for category in self.categories_collection:
            # this removes the category from the collection
            # but relies on delete_category_orphans for clean-up
            self.categories_collection.remove(category)

    @staticmethod
    def update(bookmark_id: int, title: str, link: str, categories: list):
        """
        static method: accepts bookmark_id int, title str, link str and categories list
        checks for existing bookmark to update and flushes the existing categories
        """
        bookmark_exists = Bookmark.query.filter_by(bookmark_id=bookmark_id).first()
        if bookmark_exists:
            bookmark_exists.title = title
            bookmark_exists.link = link
            bookmark_exists.flush_categories()
            if categories and isinstance(categories, list):
                for category in categories:
                    Category.create(category, bookmark_exists)
                return True
            else:
                return False
        else:
            return False


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

    @staticmethod
    def create(category: str, bookmark):
        """
        static method: accepts a single category and bookmark object.
        checks for existing category and appends the collection.
        """
        category_exists = Category.query.filter_by(name=category).first()
        if category_exists:
            bookmark.categories_collection.append(category_exists)
        else:
            add_category = Category(name=category)
            bookmark.categories_collection.append(add_category)
        db.session.add(bookmark)
        db.session.commit()


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
