
# -*- coding: utf-8 -*-
from models import db,CRUDMixin


class Example(db.Model,CRUDMixin):
    __tablename__ = "example"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    is_albums = db.Column(db.Integer)
    is_attach = db.Column(db.Integer)
    is_spec = db.Column(db.Integer)
    sort_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_info(self):
        info_dict = {
            "id":self.id,
            "name":self.name,
            "title":self.title,
            "isAlbums":self.is_albums,
            "isAttach":self.is_attach,
            "isSpec":self.is_spec,
            "sortId":self.sort_id,
        }
        return info_dict
    
    def __repr__(self):
        return 'id : %s' % self.id


    tableChangeDict = {
    "id":"id",
    "name":"name",
    "title":"title",
    "isAlbums":"is_albums",
    "isAttach":"is_attach",
    "isSpec":"is_spec",
    "sortId":"sort_id"
    }
    
    intList = ['id','isAlbums','isAttach','isSpec','sortId']

# db.create_all()
