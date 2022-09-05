import json
import os

import click
from flask_migrate import Migrate

from app import create_app, db
from app.models.bookmark import Bookmark, Category
from app.models.reference import Reference, ReferenceStructure
from app.models.user import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Bookmark=Bookmark, Category=Category, Reference=Reference)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('database dropped')


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('database created')


@app.cli.command('db_reference_seed')
def db_reference_seed():
    ref_path = 'app/Reference'
    reference_structure = ReferenceStructure.create_directory_structure(ref_path)
    ref_struct = ReferenceStructure(path=ref_path, structure=json.dumps(reference_structure))
    ref_struct.add_hash(json.dumps(reference_structure))
    db.session.add(ref_struct)
    db.session.commit()

    Reference.create_markdown_entries(ref_path)
    

@app.cli.command('db_seed')
def db_seed():
    with open('bookmarksJson.json', 'r') as bookmarks_file:
        bookmarks = json.load(bookmarks_file)
        for b in bookmarks:
            bq = db.session.query(Bookmark.bookmark_id).filter(Bookmark.link == b['link'])
            if not db.session.query(bq.exists()).scalar():
                add_b = Bookmark(title=b['title'], link=b['link'])
                # check for existence of key category and type list
                if 'category' in b and isinstance(b['category'], list):
                    for c in b['category']:
                        # test for existence of category entry
                        q = db.session.query(Category.category_id).filter(Category.name == c)
                        # get the boolean of whether q exists
                        if db.session.query(q.exists()).scalar():
                            cq = Category.query.filter_by(name=c).first()
                            # add existing category to the bookmark
                            add_b.categories_collection.append(cq)
                        # if q doesn't exist
                        else:
                            # create Category object
                            add_c = Category(name=c)
                            # add c to b
                            add_b.categories_collection.append(add_c)
                        # add bookmark and commit changes
                        db.session.add(add_b)
                        db.session.commit()
    print('bookmarks added\ncategories added')
    Role.insert_roles()
    print('inserted roles')
    print('database_seeded')
