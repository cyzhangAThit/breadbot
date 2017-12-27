#!/usr/bin/env python3
import os
import re
import sys
import yaml
from pymongo import MongoClient

from breadbot.core import misc


class insertData(object):

    def __init__(self, dataPath=None):
        self.splitSignal = ' '
        self.db = self.create_db('breadDB')
        if not dataPath:
            dataPath = misc.cfg().get('data_path')
        if not dataPath:
            print('[Error] data path not found')
            sys.exit(1)
        changedDataList = self.get_changed_data_list(dataPath)
        self.clean_old_db_data(changedDataList)
        self.insert_db_data(changedDataList)
        print('\n All Complete!')

    def create_db(self, dbName):
        client = MongoClient('localhost', 27017)
        db = client[dbName]
        return db

    def _get_data_log_path(self):
        dataLogPath = os.path.join(misc.cfg().get('log_path'), 'data.log')
        return dataLogPath

    def _get_path_name(self, filePath):
        dirList = ['dia', 'klg', 'sec']
        pathList = filePath.split(r'/')
        num = 0
        for i in range(len(pathList)):
            if pathList[i] in dirList:
                num = i
                break
        path = '_'.join(pathList[i:])
        path = path.replace('.', '_')
        return path

    def _read_data_file(self, dataPath):
        f = open(dataPath, 'r')
        readStr = f.read()
        readStr = re.sub(r'\n +\n', '\n\n', readStr)
        f.close()
        return readStr

    def _save_data_list(self, dataList):
        dataLogPath = self._get_data_log_path()
        log = open(dataLogPath, 'w')
        for dataPathInfo in dataList:
            log.write(dataPathInfo + '\n')
        log.close()

    def _get_data_list(self, root, files):
        dataList = []
        for file in files:
            if not re.match(r'^.*\.yml$', file):
                continue
            filePath = os.path.join(root, file)
            editTime = os.stat(filePath).st_mtime
            info = ' '.join([filePath, str(editTime)])
            dataList.append(info)
        return dataList

    def _get_cur_data_list(self, dataPath):
        curDataList = []
        for root, dirs, files in os.walk(dataPath):
            dataList = self._get_data_list(root, files)
            curDataList += dataList
        try:
            secPath = os.path.join(dataPath, 'sec')
            secPath = os.readlink(secPath)
            for root, dirs, files in os.walk(secPath):
                dataList = self._get_data_list(root, files)
                curDataList += dataList
        except Exception:
            print('[Warning] No sec found')
        return curDataList

    def _get_old_data_list(self):
        dataLogPath = self._get_data_log_path()
        if os.path.exists(dataLogPath):
            log = open(dataLogPath, 'r')
            oldDataList = log.readlines()
            for i in range(len(oldDataList)):
                oldDataList[i] = oldDataList[i].replace('\n', '')
            log.close()
            return oldDataList
        else:
            log = open(dataLogPath, 'w')
            log.close()
            return []

    def get_changed_data_list(self, dataPath):
        curDataList = self._get_cur_data_list(dataPath)
        oldDataList = self._get_old_data_list()
        changedDataList = []
        for dataPath in curDataList:
            if dataPath not in oldDataList:
                dataPath = dataPath.split(self.splitSignal)[0]
                changedDataList.append(dataPath)
        for dataPath in oldDataList:
            if dataPath not in curDataList:
                dataPath = dataPath.split(self.splitSignal)[0]
                changedDataList.append(dataPath)
        self._save_data_list(curDataList)
        return changedDataList

    def clean_old_db_data(self, changedDataList):
        for dataPath in changedDataList:
            pathName = self._get_path_name(dataPath)
            print('clean %s...' % pathName)
            self.db[pathName].drop()
        for dataPath in changedDataList:
            path = dataPath.split(self.splitSignal)[0]
            if not os.path.exists(path):
                changedDataList.remove(dataPath)

    def insert_db_data(self, changedDataList):
        for dataPath in changedDataList:
            pathName = self._get_path_name(dataPath)
            print('insert %s...' % pathName)
            coll = self.db[pathName]
            readStr = self._read_data_file(dataPath)
            data = yaml.load(readStr)
            coll.insert(data)
            coll.create_index('tag')
            coll.create_index('que')
