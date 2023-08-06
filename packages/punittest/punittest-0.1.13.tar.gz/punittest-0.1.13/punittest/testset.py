#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .settings import Settings
from .utils.parse_excel import ExcelParser
from .utils.logger import logger
from importlib import import_module
import unittest
import re
import os
import platform


class TestSet:
    def __init__(self, test_prefix):
        self.test_set = []
        self.case_prefix = test_prefix
        self.test_suite = unittest.TestSuite()

    @staticmethod
    def _convert_params(params):
        """将测试用例中的ParamsData由字符串转换成python数据结构"""
        if params is None:
            return None
        elif isinstance(params, bool):
            return [params]
        else:
            param_list = params.split('\n')
            try:
                param_list = [eval(x.strip()) for x in param_list]
            except NameError:
                param_list = [x.strip() for x in param_list]
            return param_list

    @staticmethod
    def _convert_asserts(asserts):
        """将测试用例中的AssertResult由字符串转换成python数据结构"""
        if asserts is None:
            return None
        elif isinstance(asserts, bool):
            return [asserts]
        else:
            asserts_list = asserts.split('\n')
            try:
                asserts_list = [eval(x.strip()) for x in asserts_list]
            except NameError:
                asserts_list = [x.strip() for x in asserts_list]
            return asserts_list

    @staticmethod
    def _convert_tags(tags):
        """将测试用例中的Tag解析成列表"""
        # 将字符串移除换行符，并利用逗号分隔
        tag_list = ['ALL']
        if tags is not None:
            tags = [t.strip() for t in tags.replace('\n', '').split(',')]
            if len(tags) > 0:
                tag_list.extend(tags)
        return tag_list

    def filter_test_case(self, **titles):
        """
        根据表格中的title过滤测试用例
        :param titles: 关键字参数，每个参数名对应表格中的title
        :return: 测试用例组成的列表
        """
        if titles:
            for title, value in titles.items():
                self.test_set = list(filter(lambda d: title in d.keys(), self.test_set))
                self.test_set = list(filter(lambda d: d[title] == value, self.test_set))
        return self.test_set


class CodeTestSet(TestSet):
    """从本地代码处获取测试集"""
    def __init__(self, test_prefix=Settings.TEST_PREFIX):
        super(CodeTestSet, self).__init__(test_prefix)
        self.test_set = None

    def make_test_suite(self):
        """
        遍历测试用例目录下的所有文件，类和方法，加载符合条件的测试方法（测试用例）
        :param: case_prefix 测试类和测试用例函数前缀
        :return: unittest.TestSuite 对象
        """
        for root, dir_, files in os.walk(Settings.TEST_SUITE_DIR):
            for file in files:
                if os.path.splitext(file)[-1] == '.py' and file != '__init__.py':
                    root_dir_name = os.path.split(Settings.PROJECT_ROOT)[-1]
                    if platform.system() == 'Windows':
                        path_list = root.split('\\')
                    else:
                        path_list = root.split('/')
                    path_list = path_list[path_list.index(root_dir_name) + 1:]
                    path_list.append(os.path.splitext(file)[0])
                    import_list = '.'.join(path_list)
                    package = import_module(import_list)
                    for cls_name in package.__dict__:
                        if cls_name.lower().startswith(self.case_prefix):
                            cls = getattr(package, cls_name)
                            for name, func in list(cls.__dict__.items()):
                                _name = re.sub(r'_#[\d]*', '', name)
                                _name = re.sub(self.case_prefix + r'_\d{5}', self.case_prefix, _name)
                                if _name.startswith(self.case_prefix):
                                    case = cls(name)
                                    self.test_suite.addTest(case)
        return self.test_suite


class ExcelTestSet(TestSet):
    """从Excel中读取测试集"""
    def __init__(self, test_prefix=Settings.TEST_PREFIX):
        super(ExcelTestSet, self).__init__(test_prefix)
        try:
            self._excel = ExcelParser(Settings.TEST_EXCEL_PATH, 'TestCases')
        except FileNotFoundError:
            raise FileNotFoundError("Cannot found testcase file: {}".format(Settings.TEST_EXCEL_PATH))
        self.test_set = self.make_test_set()

    def make_test_set(self):
        """
        一次性读取所有测试用例
        :return: [dict(case), dict(case)...]形式的suite
        """
        test_set = list()
        titles = [x for x in self._excel.get_row_values(1)]
        for row in range(2, self._excel.max_row + 1):
            test_case = dict()
            row_hidden = self._excel.worksheet.row_dimensions[row].hidden   # 获取该行是否被隐藏
            # 过滤被隐藏的行
            if row_hidden is False:
                values = [x for x in self._excel.get_row_values(row)]
                # 将行数据按照表头个数补齐None
                if len(values) < len(titles):
                    for i in range(len(titles) - len(values)):
                        values.append(None)
                for title, value in zip(titles, values):
                    if title == 'ParamsData':
                        params = self._convert_params(value)
                        test_case[title] = params
                    elif title == 'AssertResult':
                        asserts = self._convert_asserts(value)
                        test_case[title] = asserts
                    elif title == 'Tags':
                        tags = self._convert_tags(value)
                        test_case[title] = tags
                    else:
                        test_case[title] = value
                test_set.append(test_case)
        return test_set

    def make_test_suite(self):
        """
        将excel表格中读取的测试用例生成 PUnittest 能识别的 TestSuite 对象，或者获取本地的所有测试文件
        :param: case_prefix 测试类和测试用例函数前缀
        :return: unittest.TestSuite 对象
        """
        if len(self.test_set) > 0:
            for test_case in self.test_set:
                _dir_name = test_case['TestDir'] if 'TestDir' in test_case else None
                _file_name = test_case['TestFile'] if 'TestFile' in test_case else None
                _cls_name = test_case['TestClass'] if 'TestClass' in test_case else None
                _case_name = test_case['TestCase'] if 'TestCase' in test_case else None
                try:
                    package = import_module('{0}.{1}'.format(_dir_name, _file_name))
                    cls = getattr(package, _cls_name)
                    for name, func in list(cls.__dict__.items()):
                        # 将装饰过的测试用例尾部序号移除
                        _name = re.sub(r'_#[\d]*', '', name)
                        # 将装饰过的测试用例首部还原
                        _name = re.sub(self.case_prefix + r'_\d{5}', self.case_prefix, _name)
                        if _name == _case_name:
                            case = cls(name)
                            self.test_suite.addTest(case)
                except Exception as e:
                    logger.error('Fail to load test case <{0}><{1}>: {2}'.format(_cls_name, _case_name, e))
        else:
            logger.error('Fail to load any test case, please check')
            raise RuntimeError('Fail to load any test case, please check')
        return self.test_suite


class ApiTestSet(TestSet):
    """从Http接口获取测试集"""
    def __init__(self, data, test_prefix=Settings.TEST_PREFIX):
        super(ApiTestSet, self).__init__(test_prefix)
        self.api_data = data
        self.test_set = self.make_test_set()

    def make_test_set(self):
        test_set = list()
        for item in self.api_data:
            test_case = dict()
            for k, v in item.items():
                if k == 'ParamsData':
                    params = self._convert_params(v)
                    test_case[k] = params
                elif k == 'AssertResult':
                    asserts = self._convert_asserts(v)
                    test_case[k] = asserts
                elif k == 'Tags':
                    tags = self._convert_tags(v)
                    test_case[k] = tags
                else:
                    test_case[k] = v
            test_set.append(test_case)
        return test_set
