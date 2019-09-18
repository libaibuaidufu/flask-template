#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 16:06
# @File    : db.py
# @author  : dfkai
# @Software: PyCharm
from datetime import datetime

from sqlalchemy import text

from settings.config import db
from settings.log import logger

now = datetime.now()
now_date = datetime.now().date()


class Common(object):
    @classmethod
    def check_data_dict_has_must_key(cls, dataDict: dict, checkList: list) -> bool:
        """
        检查 是否含有必有的字段
        :param dataDict:
        :param checkList:
        :return:
        """
        for checkValue in checkList:
            if not dataDict.get(checkValue, None):
                return False
        return True

    @classmethod
    def pop_data_dict_no_update_key(cls, dataDict: dict, popList: list) -> dict:
        """
        去掉拒绝更新的字段
        :param dataDict:
        :param popList:
        :return:
        """
        for checkValue in popList:
            if checkValue in dataDict.keys():
                dataDict.pop(checkValue)
        return dataDict

    @classmethod
    def check_Up_key_in_str(cls, key: str):
        """
        解决驼峰单词 不是模型命名字段
        classmethod 是为了 给insert使用
        :param key:
        :return:
        """
        if key.islower():
            return key
        newKey = ""
        for index, pk in enumerate(key):
            if pk in "ABCDEFGHIJKLMNOPQRSTUVWXZY":
                newKey += f"_{pk.lower()}"
            else:
                newKey += pk
        return newKey

    @classmethod
    def up_first_key(cls, dataDict):
        """
        单词下划线 转换为 驼峰
        :param dataDict:
        :return:
        """
        infoDict = dict()
        for key, value in dataDict.items():
            n_key = ""
            key_list = key.split("_")
            for index, pk in enumerate(key_list):
                if index == 0:
                    n_key += pk
                else:
                    n_key += pk[:1].upper() + pk[1:].lower()
                if len(key_list) == index + 1:
                    infoDict[n_key] = value
        return infoDict


# 非驼峰结构 not Id
class CRUDMixinNotId(Common):
    """
    基础版本 没有使用驼峰转换
    """
    __table_args__ = {'extend_existing': True}

    # __abstract__ = True

    @classmethod
    def insert(cls, *args, **kwargs: dict):
        """
        :param args: list 按照顺序 进行填充值 跳过主键
        :param kwargs: dict 小写
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
                tableDict[key] = value
        instance = cls(**tableDict)
        return instance.save()

    def save(self):
        """
        保存
        :param is_commit:
        :return:
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return 0

    def update(self, **kwargs):
        """
        更新
        :param is_commit:
        :param kwargs:
        :return:
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            return self.save()
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return 0

    def delete(self):
        """
        删除
        :param is_commit:
        :return:
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            # 加入数据库commit提交失败，必须回滚！！！
            db.session.rollback()
            logger.error(e)
            return 0

    @classmethod
    def get_ins_by_id(cls, id):
        """
        通过id获取实例
        :param id:
        :return:
        """
        if any((isinstance(id, str) and id.isdigit(),
                isinstance(id, (int, float))), ):
            return cls.query.get(int(id))
        return False

    def get_dict(self, re_list: list = [], pop_list=[], is_model=False):
        """
        通过 实例__dict__直接获取 字典格式，但是里面有一个不需要的 _sa_instance_state 直接pop掉
        改用 to_dict
        re_list and not_list　,only use one

        :return:
        """
        infoDict = self.to_dict()
        if is_model:
            pop_list = list(map(lambda x: x.__str__().rsplit(".", 1)[-1], pop_list))
            re_list = list(map(lambda x: x.__str__().rsplit(".", 1)[-1], re_list))
        if pop_list:
            for key in pop_list:
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

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


# 非驼峰结构
class CRUDMixin(CRUDMixinNotId):
    id = db.Column(db.Integer, nullable=False, primary_key=True)

    @classmethod
    def get_ins_by_ids(cls, ids):
        if isinstance(ids, (list, tuple)):
            return cls.query.filter(cls.id.in_(ids)).all()
        return False


# 非驼峰 分页基础版 搜索
def serachView(dataDict: dict, tableName: db.Model, groupBy: str = "", orderByStr: str = "",
               otherCondition: str = ""):
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
            orderStr = f"{key} {value}"
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
            if field not in tableName.__table__.columns:
                # 如果模型中没有此字段 就跳过
                continue
            if op == "llike":
                sql_condition = f"{field} {opDic[op]}  '%{str(value)}'"
            elif op == "rlike":
                sql_condition = f"{field} {opDic[op]}  '{str(value)}%'"
            elif op == "like":
                sql_condition = f"{field} {opDic[op]}  '%{str(value)}%'"
            elif op in ["in", "not in", "is"]:
                sql_condition = f"{field} {opDic[op]}  '{str(value)}'"
            else:
                sql_condition = f"{field} {opDic[op]}  {str(value)}"
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
    if pageSize > 50: pageSize = 50
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
class TransactionClass(object):
    """
    事务处理
    """

    def __init__(self):
        self._session = db.session
        self._engine = db.engine

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

    def update(self, ins, dataDict):
        """
        模型更新
        :param ins: object
        :param dataDict: 更新信息
        :return:
        """
        try:
            for key, value in dataDict.items():
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
        except Exception as e:
            logger.error(e)

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
