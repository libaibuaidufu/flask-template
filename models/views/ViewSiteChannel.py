#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/31 11:54
# @File    : ExampleModelApi.py
# @author  : dfkai
# @Software: PyCharm
from models import db, CRUDMixin


class ViewSiteChannel(db.Model, CRUDMixin):
    __tablename__ = "view_site_channel"
    # site_id = db.Column(db.Integer, comment='站点ID')
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='自增ID')
    name = db.Column(db.String(50), comment='频道名称')
    title = db.Column(db.String(100), comment='频道标题')
    is_albums = db.Column(db.SmallInteger, default=0, comment='是否开启相册功能')
    is_attach = db.Column(db.SmallInteger, default=0, comment='是否开启附件功能')
    is_spec = db.Column(db.SmallInteger, default=0, comment='是否开启规格')
    sort_id = db.Column(db.Integer, default=99, comment='排序数字')
    autoload = True
    is_view = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_info(self):
        info_dict = {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "isAlbums": self.is_albums,
            "isAttach": self.is_attach,
            "isSpec": self.is_spec,
            "sortId": self.sort_id,
        }
        return info_dict


    tableChangeDict = {
        "id": "id",
        "name": "name",
        "title": "title",
        "isAlbums": "is_albums",
        "isAttach": "is_attach",
        "isSpec": "is_spec",
        "sortId": "sort_id"
    }
    intList = ['id', 'isAlbums', 'isAttach', 'isSpec', 'sortId']
