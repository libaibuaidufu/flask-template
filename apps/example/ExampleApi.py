# -*- coding: utf-8 -*-

from flask import request, json, jsonify

from apps.example import example_api
from models import Example
from models.views import ViewExample
from settings.db import TransactionClass, serachView
from utils.ReturnMessage import returnMsg, errorCode, returnErrorMsg


# select list view
@example_api.route("/findViewExampleByCondition", methods=["POST"])
def findViewExampleByCondition():
    jsonData: str = request.get_data()
    dataDict: dict = json.loads(jsonData)
    groupBy = " id"
    orderByStr = " sort_id desc "
    otherCondition = " id != 99 "
    resultList = serachView(dataDict, ViewExample, groupBy=groupBy, orderByStr=orderByStr,
                            otherCondition=otherCondition)
    infoList = []
    if resultList:
        for result in resultList.items:
            data = result.get_dict()
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
            data = result.get_dict()
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
    table = Example.insert(**dataDict)
    if table:
        resultDict = returnMsg(table.get_dict())
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
    table = Example.get_ins_by_id(id)
    if table.update(**dataDict):
        resultDict = returnMsg(table.get_dict())
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
    table = Example.get_ins_by_id(id)
    if table:
        # 三种获取值得方式
        re_list = ["name"]
        infoDict = table.get_dict(re_list=re_list)
        print(infoDict)
        # {'name': 'dfk'}

        pop_list = ["name"]
        infoDict = table.get_dict(pop_list=pop_list)
        print(infoDict)
        # {'id': 1, 'title': 'dfk2', 'is_albums': 0, 'is_attach': 0, 'is_spec': 0, 'sort_id': 99}

        re_list = [Example.name]
        infoDict = table.get_dict(re_list=re_list, is_model=True)
        print(infoDict)
        # {'name': 'dfk'}

        pop_list = [Example.name]
        infoDict = table.get_dict(pop_list=pop_list, is_model=True)
        print(infoDict)
        # {'id': 1, 'title': 'dfk2', 'is_albums': 0, 'is_attach': 0, 'is_spec': 0, 'sort_id': 99}

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
    table = Example.insert(**dataDict)
    table = trans.save(table)
    print(table.get_dict())
    try:
        # trans.commit()
        raise ValueError
    except:
        trans.rollback()
    return jsonify(returnMsg())


@example_api.route("/testSelectForUpdate")
def testSelectForUpdate():
    example = Example.query.filter(Example.id == 1).with_for_update()
    print(example)
    print(example.one().name)
    import time
    time.sleep(20)
    dataDict = dict(name="libai")
    example.update(dataDict)
    return jsonify(dict(code=1))
