# -*- coding: utf-8 -*-

Code_Str = "code"
Info_Str = "info"
Message_Str = "message"

errorCode: dict = {
    "param_error": "参数错误",
    "fail": "服务器异常!",
    "json_error": "json格式错误",
    "update_fail": "更新失败!查看参数是否正确!",
    "insert_fail": "插入失败!查看参数是否正确!",
    "commit_fail": "提交失败!查看参数是否正确!",
    "query_fail": "查询失败!查看参数是否正确!",
    "delete_fail": "删除失败!查看参数是否正确!",
    "permission_denied": "权限不对",
}


# 请求报错
def returnErrorMsg(CodeStr=None):
    if CodeStr:
        resultDict = {Message_Str: {"code": -1, "msg": CodeStr}}
    else:
        resultDict = {Message_Str: {"code": -1, "msg": "服务器异常!"}}
    return resultDict


# 请求成功，有数据
def returnMsg(dataDict: dict = {}):
    resultDict = {Info_Str: dataDict, Message_Str: {Code_Str: 1, "msg": ""}}
    return resultDict
