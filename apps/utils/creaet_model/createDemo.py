# coding:utf-8
import os

data = """# -*- coding: utf-8 -*-

from flask import request, json, jsonify

from apps.example import example_api
from utils.ReturnMessage import returnMsg, errorCode, returnErrorMsg
from models.{ModelName} import {ModelName}
from settings.dataBase import TransactionClass, serachView


# select list view
@example_api.route("/findView{ModelName}ByCondition", methods=["POST"])
def findView{ModelName}ByCondition():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    groupBy = "group by id"
    orderByStr = " order by sort_id desc "
    otherCondition = " id != 99 "
    resultList = serachView(dataDict, {ModelName}, groupBy=groupBy, orderByStr=orderByStr,
                            otherCondition=otherCondition)
    infoList = []
    if resultList:
        for result in resultList.items:
            data = result.get_info_by_dict()
            infoList.append(data)
        infoDict = dict(data=infoList, total=resultList.total)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify((resultDict))


# select list 
@example_api.route("/find{ModelName}ByCondition", methods=["POST"])
def find{ModelName}ByCondition():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    resultList = serachView(dataDict, {ModelName})
    infoList = []
    if resultList:
        for result in resultList.items:
            data = result.get_info_by_dict()
            infoList.append(data)
        infoDict = dict(data=infoList, total=resultList.total)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify((resultDict))


# add info 
@example_api.route("/add{ModelName}", methods=["POST"])
def add{ModelName}():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    table = {ModelName}.create(**dataDict)
    if table:
        resultDict = returnMsg(table.to_dict())
    else:
        resultDict = returnErrorMsg(errorCode["insert_fail"])
    return jsonify(resultDict)


# update info 
@example_api.route("/update{ModelName}", methods=["POST"])
def update{ModelName}():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    id: int = dataDict.get("id", 0)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify((resultDict))
    table = {ModelName}.get_into_by_id(id)
    if table.update(**dataDict):
        resultDict = returnMsg(table.to_dict())
    else:
        resultDict = returnErrorMsg(errorCode["update_fail"])
    return jsonify(resultDict)


# delete info 
@example_api.route("/delete{ModelName}", methods=["POST"])
def delete{ModelName}():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    idList: list = dataDict.get("idList", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify((resultDict))
    trans = TransactionClass()
    tableList = {ModelName}.query.filter({ModelName}.id.in_(idList)).all()
    if not trans.deleteList(tableList):
        resultDict = returnErrorMsg(errorCode["delete_fail"])
        return jsonify(resultDict)
    if trans.commit():
        resultDict = returnMsg()
    else:
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify((resultDict))


# get info 
@example_api.route("/get{ModelName}Info", methods=["POST"])
def get{ModelName}Info():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    id: int = dataDict.get("id", None)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = {ModelName}.get_into_by_id(id)
    if table:
        infoDict = table.to_dict()
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
    return jsonify(resultDict)


# trans test
@example_api.route("/testTrans", methods=["POST"])
def testTrans():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    trans = TransactionClass()
    table = {ModelName}.insert(dataDict)
    table = trans.save(table)
    print(table.to_dict())
    try:
        # trans.commit()
        raise ValueError
    except:
        trans.rollback()
    return jsonify(returnMsg())
"""


class CreateApi:
    def __init__(self, db, dbname):
        self.db = db
        self.dbname = dbname

    # 列出所有的表
    def list_table(self):
        " SELECT  *  FROM  information_schema.views"
        "information_schema.tables"
        tableList = self.db.engine.execute(
            "select TABLE_NAME,row_format from information_schema.tables where (TABLE_TYPE='BASE TABLE' or TABLE_TYPE='VIEW') and table_schema='{}'".format(
                self.dbname))
        table_list = []
        for tuple in tableList:
            table_list.append(tuple[0])
        return table_list

    # 大写
    def normalize(self, name):
        return name.capitalize()

    # 大写模型名
    def getName(self, tablename):
        if self.dataType in tablename:
            modelName = tablename.replace(self.dataType, "")
            list_k = modelName.split('_')
            try:
                z = map(self.normalize, list_k)
                modelName = ''.join(z)
                # modelName = ''.join([list_k[0], z])
            except:
                modelName = ''
        elif "_" in tablename:
            list_k = tablename.split('_')
            try:
                # z = map(self.normalize, list_k[1:])
                z = map(self.normalize, list_k)
                modelName = ''.join(z)
                # modelName = ''.join([list_k[0], z])
            except:
                modelName = ''
        else:
            modelName = self.normalize(tablename)
        return modelName

    def creatModel(self, table, models):
        self.intList = []
        self.first = True
        dirpath = os.getcwd()
        tablename = table
        modelName = self.getName(tablename)
        file = "{}Api.py".format(modelName)
        doc_path = os.path.join(dirpath, "wtempmodel")
        if not os.path.exists(doc_path):
            os.mkdir(doc_path)
        filepath = os.path.join(doc_path, file)
        try:
            with open(filepath, "w+") as f:
                f.write(models)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False

    def main(self, tablename=[], dataType="data_"):
        table_list = self.list_table()
        self.dataType = dataType
        if tablename:
            for table in tablename:
                if table in table_list:
                    models = data
                    try:
                        tablename = table
                        ModelName = self.getName(tablename)
                        models = models.format(ModelName=ModelName).replace("\b", "{").replace("\a", "}")
                        if self.creatModel(table, models):
                            print("success", table)
                        else:
                            print("fail", table)
                    except Exception as e:
                        print(e)
                        print(table)
        else:
            for table in table_list:
                models = data
                try:
                    tablename = table
                    ModelName = self.getName(tablename)
                    models = models.format(ModelName=ModelName).replace("\b", "{").replace("\a", "}")
                    if self.creatModel(table, models):
                        print("success", table)
                    else:
                        print("fail", table)
                except Exception as e:
                    print(e)
                    print(table)
