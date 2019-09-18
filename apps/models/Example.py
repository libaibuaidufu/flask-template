# -*- coding: utf-8 -*-
from settings.dataBase import CRUDMixin, db


class Example(db.Model, CRUDMixin):
    __tablename__ = "example"
    __table_args__ = ({'comment': '案例表'})

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), comment="名称")
    title = db.Column(db.String(100), comment="标题")
    is_albums = db.Column(db.SMALLINT, comment="是否相册")
    is_attach = db.Column(db.SMALLINT, comment="是否附件")
    is_spec = db.Column(db.SMALLINT, comment="是否")
    sort_id = db.Column(db.SMALLINT, comment="排序")

    def __str__(self):
        return self.name
