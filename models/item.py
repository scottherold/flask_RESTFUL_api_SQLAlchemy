import sqlite3

from db import db


class ItemModel(db.Model):
    """ A model for an Item object. Extends SQLAlchemy Model object

    Attributes:
        name (str): The name of the ItemModel instance.
        price (decimal): The cost of an ItemModel instance.
        store_id (int): The id number of the store the instance of the ItemModel is related to in
            the DB

    Class Methods:
        find_by_name: Takes the arguement 'name' and performs a GET query on the DB to determine
            if the ItemModel is present.

    Methods:
        json: Returns the ItemModel attributes in JSON format
        save_to_db: upserts data (ItemModel) into the DB.
        delete_from_db: deletes data (ItemModel) from DB.
    """
    # DB ORM fields
    __tablename__ = 'items'

    # Attributes MUST match the DB model properties, except for id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Many to one relationship (Store --> Items)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    @classmethod
    def find_by_name(cls, name):
        # refactored SQLAlchemy ORM
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # refactored SQLAlchemy ORM to upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # refactored SQLAlchemy ORM
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'name': self.name, 'price': self.price}