#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 13:46
# @File    : hump_db.py
# @author  : dfkai
# @Software: PyCharm

from sqlalchemy import text

from settings.config import db
from settings.dataBase import Common
from settings.log import logger


# Not id
class CRUDMixinNotId(Common):
    __table_args__ = {'extend_existing': True}

    @classmethod
    def insert(cls, *args, **kwargs: dict):
        """
        先把驼峰结构转换为 小写加下划线 | isDelete -> is_delete
        :param args: list 按照顺序 进行填充值 跳过主键
        :param kwargs: dict
        :return:
        """
        tableDict = dict()
        if args:
            index = 0
            for c in cls.__table__.columns:
                if c.primary_key:
                    continue
                if len(args) < index + 1:
                    break
                tableDict[c.name] = args[index]
                index += 1
        if kwargs:
            for key, value in kwargs.items():
                key = cls.check_Up_key_in_str(key)  # 非驼峰可以注释
                tableDict[key] = value
        instance = cls(**tableDict)
        return instance.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False

    def update(self, **kwargs: dict):
        try:
            for key, value in kwargs.items():
                key = self.check_Up_key_in_str(key)  # 解决驼峰单词 不是模型命名单词 # # 非驼峰可以注释
                setattr(self, key, value)
            return self.save()
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False

    @classmethod
    def get_ins_by_id(cls, id):
        if any((isinstance(id, str) and id.isdigit(),
                isinstance(id, (int, float))), ):
            return cls.query.get(int(id))
        return False

    def get_dict(self, re_list: list = [], not_list=[], is_lower: bool = False):
        """
        通过 实例__dict__直接获取 字典格式，但是里面有一个不需要的 _sa_instance_state 直接pop掉
        但是不是驼峰结构 可以在转换一下
        改用 to_dict
        :return:
        """
        dataDict = self.to_dict()
        infoDict = self.up_first_key(dataDict)
        if is_lower:
            _kv = {v: k for k, v in self.tableChangeDict.items()}
            not_list = [_kv[key] if _kv.get(key, "") else key for key in not_list]
            re_list = [_kv[key] if _kv.get(key, "") else key for key in re_list]
        if not_list:
            for key in not_list:
                if key in infoDict:
                    infoDict.pop(key)
            return infoDict
        elif re_list:
            re_dict = dict()
            for key in re_list:
                if key:
                    re_dict[key] = infoDict.get(key, "")
            return re_dict
        return infoDict

    def to_dict_table(self, re_list: list = [], is_in_use: bool = False, is_not_in_use: bool = False):
        """
        通过模型来获取值
        :param re_list:
        :param is_in_use:
        :param is_not_in_use:
        :return:
        """
        infoDict = dict()
        if is_in_use or is_not_in_use:
            re_list = list(map(lambda x: x.__str__().rsplit(".", 1)[-1], re_list))
        for c in self.__table__.columns:
            if c.name in re_list and is_in_use:
                infoDict[c.name] = getattr(self, c.name, None)
            if c.name not in re_list and is_not_in_use:
                infoDict[c.name] = getattr(self, c.name, None)
        infoDict = self.up_first_key(infoDict)
        return infoDict

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


# 驼峰结构 版本
class CRUDMixin(CRUDMixinNotId):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)

    @classmethod
    def get_ins_by_ids(cls, ids):
        if isinstance(ids, (list, tuple)):
            return cls.query.filter(cls.id.in_(ids)).all()
        return False


# 分页 驼峰 搜索
def serachView(dataDict: dict, tableName: db.Model, groupBy: str = "", orderByStr: str = "", otherCondition: str = ""):
    """
    reqeusts args:
    {
        "condition":[
            {"field":"id","op":"equal","value":1},
            {"field":"id","op":"notequal","value":2},
            {"field":"id","op":"notin","value":"(2)"},
            {"field":"id","op":"in","value":"(1,2)"},
            {"field":"id","op":"less","value":3},
            {"field":"id","op":"greater","value":0},
            {"field":"id","op":"llike","value":1},
            {"field":"id","op":"rlike","value":1},
            {"field":"id","op":"like","value":1}
        ],
        "page":{"pageIndex":1,"pageSize":30},
        "multiSort":{"id":"desc"}
    }
    # example:
        groupBy = " group by id "
        orderByStr = " order by sort_id desc "
        otherCondition = " id != 99 "
        resultList = serachView(dataDict, tablename, groupBy=groupBy, orderByStr=orderByStr,otherCondition=otherCondition)
    # id =  1  and id !=  2  and id not in  (2)  and id in  (1,2)  and id <  3  and id >  0  and id like  '%1'  and id like  '1%'  and id like  '%1%'  order by id desc limit 0,30
    :param dataDict:
    :param tableName:
    :param sqlStr:
    :param groupBy:
    :param orderByStr:
    :param deptIdConditonStr:
    :return:
    """
    opDic = {"in": "in", "notin": "not in", "equal": "=", "notequal": "!=", "less": "<", "greater": ">", "is": "is",
             "llike": "like", "rlike": "like", "like": "like", "contains": "like"}

    # 排序编辑
    multiSort: dict = dataDict.get("multiSort", {})
    if multiSort:
        orderList = []
        for key, value in multiSort.items():
            orderStr = f"{tableName.tableChangeDict[key]} {value}"
            orderList.append(orderStr)
        if orderByStr and orderList:
            orderByStr += ","
        orderByStr += " , ".join(orderList)

    # 条件编辑
    condition: list = dataDict.get("condition", [])
    sqlStr: str = ""
    if condition:
        conditionList: list = []
        for cond in condition:
            field, op, value = cond["field"], cond["op"], cond["value"]
            if op == "llike":
                sql_condition = f"{tableName.tableChangeDict[field]} {opDic[op]}  '%{str(value)}'"
            elif op == "rlike":
                sql_condition = f"{tableName.tableChangeDict[field]} {opDic[op]}  '{str(value)}%'"
            elif op in ["like", "contains"]:
                sql_condition = f"{tableName.tableChangeDict[field]} {opDic[op]}  '%{str(value)}%'"
            elif op in ["in", "not in", "is"]:
                sql_condition = f"{tableName.tableChangeDict[field]} {opDic[op]}  {str(value)}"
            else:
                sql_condition = f"{tableName.tableChangeDict[field]} {opDic[op]}  '{str(value)}'"
            conditionList.append(sql_condition)
        sqlStr = " and ".join(conditionList)
    if sqlStr.strip():
        if otherCondition:
            sqlStr = sqlStr + " and " + otherCondition
        else:
            sqlStr = sqlStr
    else:
        sqlStr = otherCondition
    # 分页编辑
    pageDic: dict = dataDict.get("page", {})
    pageIndex: int = pageDic.get("pageIndex", 1)
    pageSize: int = pageDic.get("pageSize", 20)
    if pageIndex <= 0: pageIndex = 1
    if pageSize > 1000: pageSize = 50
    try:
        sqlStrquery = text(sqlStr)
        orderByStr = text(orderByStr.strip())
        groupBy = text(groupBy.strip())
        if sqlStr.strip():
            tableList = tableName.query.filter(sqlStrquery).group_by(groupBy).order_by(orderByStr)
        else:
            tableList = tableName.query.group_by(groupBy).order_by(orderByStr)
        # 这样返回可以使用更多分页的特性
        return tableList.paginate(pageIndex, per_page=pageSize, error_out=False)
    except Exception as  e:
        logger.error(e)
        return []


# 事务
class TransactionClass(Common):
    """
    事务处理
    """

    def __init__(self):
        self._session = db.session
        self._engine = db.engine

    def insert(self, table, **kwargs):
        """
        先把驼峰结构转换为 小写加下划线 | isDelete -> is_delete
        :param kwargs: dict
        :return:
        """
        tableDict = dict()
        for key, value in kwargs.items():
            key = table.check_Up_key_in_str(key)
            tableDict[key] = value
        instance = table(**tableDict)
        return self.save(instance)

    def save(self, ins):
        """
        模型 新增 保存
        :param ins:
        :return:
        """
        try:
            self._session.add(ins)
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return ins

    def update(self, ins, dataDict, is_hump=True):
        """
        模型更新
        :param ins: object
        :param dataDict: 更新信息
        :param is_hump: 是否是驼峰 默认 false
        :return:
        """
        try:
            for key, value in dataDict.items():
                if is_hump:
                    key = self.check_Up_key_in_str(key)
                setattr(ins, key, value)
            self._session.add(ins)
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return ins

    def deleteList(self, inss: list):
        """
        模型 批量删除
        :param inss:
        :return:
        """
        try:
            for ins in inss:
                self._session.delete(ins)
                self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return True

    def delete(self, ins):
        """
        模型 删除
        :param ins:
        :return:
        """
        try:
            self._session.delete(ins)
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return True

    def commit(self):
        """
        提交
        :return:
        """
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return True

    def rollback(self):
        """
        手动回滚
        :return:
        """
        try:
            self._session.rollback()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def select_sql(self, sql):
        """
        查询sql
        :param sql:
        :return:
        """
        try:
            result = self._session.execute(sql).fetchall()
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return result

    def delete_sql(self, sql):
        """
        删除sql
        :param sql:
        :return:
        """
        try:
            self._session.execute(sql)
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return True

    def insert_sql(self, sql):
        """
        sql 插入
        如 获取 新增后的数据 ,单个 可使用 get_cls_by_id,多个 执行sql
        :param sql:
        :param table_name:
        :param only_key:
        :return:
        """
        try:
            self._session.execute(sql)
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return True

    def update_sql(self, sql):
        """
        sql 更新
        如 获取 更新后的数据 ,单个 可使用 get_cls_by_id,多个 执行sql
        :param sql:
        :return:
        """

        try:
            self._session.execute(sql)
            self._session.flush()
        except Exception as e:
            self._session.rollback()
            logger.error(e)
            return False
        return True
