from .. import db


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), unique=True, nullable=False)
    link = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.String(128))

    def __repr__(self):
        return '<Bookmark %r>' % self.name