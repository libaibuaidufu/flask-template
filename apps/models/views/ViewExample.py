# -*- coding: utf-8 -*-
from settings.dataBase import CRUDMixin, db


class ViewExample(db.Model, CRUDMixin):
    __tablename__ = "view_example"
    __table_args__ = {"info": dict(is_view=True)}  # 不会被创建成表
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    is_albums = db.Column(db.Integer)
    is_attach = db.Column(db.Integer)
    is_spec = db.Column(db.Integer)
    sort_id = db.Column(db.Integer)

    def __str__(self):
        return 'id : %s' % self.id
