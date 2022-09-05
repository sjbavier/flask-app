import hashlib
import json
import os

from marshmallow import fields

from .. import db
from .. import ma


class ReferenceStructure(db.Model):
    __tablename__ = 'reference_structure'

    reference_structure_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hash = db.Column(db.String(), nullable=False)
    path = db.Column(db.String(), nullable=False)
    structure = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<ReferenceStructure %r>' % self.reference_structure_guid

    def verify_directory_structure(self, directory_structure):
        """
        verify if directory structures match
        """

        return True if self.hash == json.dumps(directory_structure) else False

    def add_hash(self, input_string: str):
        self.hash = hashlib.md5(input_string.encode("utf-8")).hexdigest()

    @staticmethod
    def create_directory_structure(path):
        """
        create the json representation of the directory tree
        copy-pasta: https://stackoverflow.com/questions/25226208/represent-directory-tree-as-json
        """

        d = {'name': os.path.basename(path), 'path': path}
        if os.path.isdir(path):
            d['type'] = 'directory'
            d['children'] = [ReferenceStructure.create_directory_structure(os.path.join(path, x)) for x in
                             os.listdir(path)]
        else:
            d['type'] = 'file'
        return d

    def add_reference_structure(self):
        """
        Static method: build/rebuild the database off of markdown files, requires path set
        """
        cwd = os.getcwd()
        ref_dir = os.path.relpath(os.path.join(cwd, self.path))
        self.structure = ReferenceStructure.create_directory_structure(ref_dir)
        with open('reference.json', 'w') as file:
            file.write(json.dumps(self.structure))


class Reference(db.Model):
    __tablename__ = 'reference'
    reference_id = db.Column(db.Integer, primary_key=True, nullable=False)
    path = db.Column(db.String, nullable=False)
    content = db.Column(db.String(), nullable=True)
    hash = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return '<Reference %r>' % self.title

    def add_hash(self):
        """
        generate md5 hash based on file content
        """
        md5 = hashlib.md5()
        with open(self.path, 'r') as f:
            while chunk := f.read(4096):
                md5.update(chunk)

        self.hash = md5.hexdigest()

    def verify_hash(self):
        """
        verify file hash with database record
        """
        md5 = hashlib.md5()
        with open(self.path, 'r') as f:
            while chunk := f.read(4096):
                md5.update(chunk)

        return True if self.hash == md5.hexdigest() else False

    def file_to_content(self):
        """
        convert file contents to string
        """
        content = ''
        with open(self.path, 'r') as f:
            self.content = f.read()

    @staticmethod
    def create_markdown_entries(path):
        """
        create markdown entries
        """
        if os.path.isdir(path):
            [Reference.create_markdown_entries(os.path.join(path, x)) for x in os.listdir(path)]
        else:
            if path.endswith('.md'):
                content = ''
                with open(path, 'rb') as f:
                    content = f.read()
                    hashed_file = hashlib.md5(content).hexdigest()
                    ref = Reference(path=path, hash=hashed_file, content=content)
                    db.session.add(ref)
                    db.session.commit()


class ReferenceStructureSchema(ma.Schema):
    reference_structure_id = fields.Integer()
    hash = fields.String()
    path = fields.String()
    structure = fields.String()


class ReferenceSchema(ma.Schema):
    reference_id = fields.Integer()
    path = fields.String()
    content = fields.String()
    hash = fields.String()
