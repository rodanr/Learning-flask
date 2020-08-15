import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id


    def json(self):
        return {"name":self.name,"price":self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM __tablename__ WHERE name=name LIMIT 1


    def save_to_db(self):
        db.session.add(self)#self:self.name, self.price
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
