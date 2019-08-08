# -*- coding: utf-8 -*-

from flask import request, json, jsonify

from apps.example import example_api
from utils.ReturnMessage import returnMsg, errorCode, returnErrorMsg
from models.Example import Example
from models.views.ViewExample import ViewExample
from settings.dataBase import TransactionClass, serachView


# select list view
@example_api.route("/findViewExampleByCondition", methods=["POST"])
def findViewExampleByCondition():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    groupBy = "group by id"
    orderByStr = " order by sort_id desc "
    otherCondition = " id != 99 "
    resultList = serachView(dataDict, ViewExample, groupBy=groupBy, orderByStr=orderByStr,
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
@example_api.route("/findExampleByCondition", methods=["POST"])
def findExampleByCondition():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    resultList = serachView(dataDict, Example)
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
@example_api.route("/addExample", methods=["POST"])
def addExample():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    table = Example.create(**dataDict)
    if table:
        resultDict = returnMsg(table.to_dict())
    else:
        resultDict = returnErrorMsg(errorCode["insert_fail"])
    return jsonify(resultDict)


# update info 
@example_api.route("/updateExample", methods=["POST"])
def updateExample():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    id: int = dataDict.get("id", 0)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify((resultDict))
    table = Example.get_into_by_id(id)
    if table.update(**dataDict):
        resultDict = returnMsg(table.to_dict())
    else:
        resultDict = returnErrorMsg(errorCode["update_fail"])
    return jsonify(resultDict)


# delete info 
@example_api.route("/deleteExample", methods=["POST"])
def deleteExample():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    idList: list = dataDict.get("idList", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify((resultDict))
    trans = TransactionClass()
    tableList = Example.query.filter(Example.id.in_(idList)).all()
    if not trans.deleteList(tableList):
        resultDict = returnErrorMsg(errorCode["delete_fail"])
        return jsonify(resultDict)
    if trans.commit():
        resultDict = returnMsg()
    else:
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify((resultDict))


# get info 
@example_api.route("/getExampleInfo", methods=["POST"])
def getExampleInfo():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    id: int = dataDict.get("id", None)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = Example.get_into_by_id(id)
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
    table = Example.insert(dataDict)
    table = trans.save(table)
    print(table.to_dict())
    try:
        # trans.commit()
        raise ValueError
    except:
        trans.rollback()
    return jsonify(returnMsg())
