# coding:utf-8
import os

data = """
# -*- coding: utf-8 -*-
from settings.dataBase import CRUDMixin, db


class {model_Name}(db.Model,CRUDMixin):
    __tablename__ = "{table_name}"

{all_fields}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_info(self):
        info_dict = [
{info_dict}
        ]
        return info_dict
    
    def __str__(self):
        return {returnMsg}


    tableChangeDict = [
{changeFields}
    ]
    
    intList = \a{intLists}\b


"""


class Models(object):
    def __init__(self, db, dbname):
        self.db = db
        self.dbname = dbname
        self.string = ["varchar", "char"]
        self.integer = ["int", "bigint", "smallint"]
        self.datatime = ["date", "datetime"]
        self.smallInteger = ["tinyint"]
        self.decimal = ["decimal"]
        self.text = ["text", "longtext"]
        self.blob = ["longblob"]
        self.intList = []

    # 查询所有字段
    def list_col(self, table_name):
        fieldsList = self.db.engine.execute(
            "select column_name,data_type,character_maximum_length,numeric_scale,numeric_precision from information_schema.columns where  table_schema='{}' and table_name='{}'".format(
                self.dbname, table_name))
        col_name_dict = {}
        col_name_list = []
        col_name_num = {}
        col_name_decl = {}
        for tuple in fieldsList:
            col_name_list.append(tuple[0])
            col_name_dict[tuple[0]] = tuple[1]
            col_name_num[tuple[0]] = tuple[2]
            col_name_decl[tuple[0]] = {"numeric_scale": tuple[3], "numeric_precision": tuple[4]}
        return col_name_dict, col_name_num, col_name_list, col_name_decl

    # 列出所有的表
    def list_table(self):
        tableList = self.db.engine.execute(
            "select TABLE_NAME,row_format from information_schema.tables where (TABLE_TYPE ='BASE TABLE' or TABLE_TYPE ='VIEW') and table_schema='{}'".format(
                self.dbname))
        table_list = []
        for tuple in tableList:
            table_list.append(tuple[0])
        return table_list

    def normalize(self, name):
        return name.capitalize()

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
        self.intList: list = []
        dirpath = os.getcwd()
        tablename = table
        modelName = self.getName(tablename)
        file = "{}.py".format(modelName)
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

    def datafl(self):
        all_fields = []
        init_fields = []
        db_column = []
        info_dict_list=[]
        listfields = []
        fileds = ",".join(self.col_name_list)
        for x in self.col_name_list:
            # init
            init_fields.append("        self.{}={}".format(x, x))
            # changeDict
            list_k = x.split('_')
            try:
                z = map(self.normalize, list_k[1:])
                z = ''.join(z)
            except:
                z = ''
            z = ''.join([list_k[0], z])
            listfields.append("'{}'".format(z))
            all_fields.append('    "{}":"{}"'.format(z, x))
            info_dict_list.append('            "{}":self.{},'.format(z,x))
            # db.column
            if 'id' == x:
                db_column.append(
                    "    {} = db.Column(db.Integer, primary_key=True, nullable=False)".format(x))
                # self.intList.append(z)
                self.intList.append("'{}'".format(z))
            elif x == self.col_name_list[0]:
                db_column.append(
                    "    {} = db.Column(db.Integer, primary_key=True, nullable=False)".format(x))
                # self.intList.append(z)
                self.intList.append("'{}'".format(z))
            elif self.col_name_dict[x] in self.string:
                db_column.append("    {} = db.Column(db.String({}))".format(x, self.col_name_num[x]))
            elif self.col_name_dict[x] in self.integer:
                db_column.append("    {} = db.Column(db.Integer)".format(x))
                # self.intList.append(z)
                self.intList.append("'{}'".format(z))
            elif self.col_name_dict[x] in self.datatime:
                db_column.append("    {} = db.Column(db.DateTime)".format(x))
            elif self.col_name_dict[x] in self.smallInteger:
                db_column.append("    {} = db.Column(db.SmallInteger)".format(x))
                self.intList.append("'{}'".format(z))
            elif self.col_name_dict[x] in self.text:
                db_column.append("    {} = db.Column(db.Text)".format(x))
            elif self.col_name_dict[x] in self.blob:
                db_column.append("    {} = db.Column(db.BLOB)".format(x))
            elif self.col_name_dict[x] in self.decimal:
                db_column.append(
                    "    {} = db.Column(db.Numeric({},{}))".format(x, self.col_name_decl[x]["numeric_precision"],
                                                                   self.col_name_decl[x]["numeric_scale"]))
            else:
                db_column.append("    {} = db.Column(db.String({}))".format(x, self.col_name_num[x]))
        all_fields = ",\n".join(all_fields)
        init_fields = "\n".join(init_fields)
        db_column = "\n".join(db_column)
        listfields = ",".join(listfields)
        info_dict_list = "\n".join(info_dict_list)
        self.intList_str = ",".join(self.intList)
        return all_fields, init_fields, db_column, fileds, listfields,info_dict_list

    def main(self, tablename=[], dataType="data_"):
        table_list = self.list_table()
        self.dataType = dataType
        # print table_list
        if tablename != []:
            for table in tablename:
                if table in table_list:
                    models = data
                    self.col_name_dict, self.col_name_num, self.col_name_list, self.col_name_decl = self.list_col(table)
                    try:
                        all_fields, init_fields, db_column, fileds, listfields,info_dict_list = self.datafl()
                        tablename = table
                        modelName = self.getName(tablename)
                        returnMsg = "'{} : %s' % self.{}".format(self.col_name_list[0], self.col_name_list[0])
                        tableChangeDic = "{}ChangeDic".format(modelName)
                        models = models.format(tableChangeDic=tableChangeDic, model_Name=modelName,
                                               table_name=tablename, all_fields=db_column,
                                               fileds=fileds, intListname=modelName + "IntList",info_dict=info_dict_list,
                                               initfields=init_fields, returnMsg=returnMsg, listfields=listfields,
                                               changeFields=all_fields, intLists=self.intList_str).replace("[",
                                                                                                           "{").replace(
                            "]", "}").replace("\a", "[").replace("\b", "]")
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
                self.col_name_dict, self.col_name_num, self.col_name_list, self.col_name_decl = self.list_col(table)
                try:
                    all_fields, init_fields, db_column, fileds, listfields,info_dict_list = self.datafl()
                    tablename = table
                    modelName = self.getName(tablename)
                    returnMsg = "'{} : %s' % self.{}".format(self.col_name_list[0], self.col_name_list[0])
                    tableChangeDic = "{}ChangeDic".format(modelName)
                    models = models.format(tableChangeDic=tableChangeDic, model_Name=modelName, table_name=tablename,
                                           all_fields=db_column,info_dict=info_dict_list,
                                           fileds=fileds, intListname=modelName + "IntList",
                                           initfields=init_fields, returnMsg=returnMsg, listfields=listfields,
                                           changeFields=all_fields, intLists=self.intList_str).replace("[",
                                                                                                       "{").replace("]",
                                                                                                                    "}").replace("\a", "[").replace("\b", "]")
                    self.intList = []
                    if self.creatModel(table, models):
                        print("success", table)
                    else:
                        print("fail", table)

                except Exception as e:
                    print(e)
                    print(table)
