#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# 类 MemberDB
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-04-12 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
import ztools.Xls
import ksystem_local.Process
# ----------------------------------------------------------------------------------------------------
class MemberDB(ztools.Xls):
    """
    MemberDB类，构建会员数据库。
    """
    def __init__(self, path):
        self.__version = "0.1"
        self.__path = path
        self.__info = None
        self.__dict = None
# ----------------------------------------------------------------------------------------------------
    def Version(self, isShow = False):
        """
        返回（屏幕上打印，可选）版本号。
        """
        if(isShow):
            print("[ksystem]-[MemberDB]-[vesion:%s]" % self.__version)
        return self.__version
# ----------------------------------------------------------------------------------------------------
    def build(self):
        """
        构建会员数据库。
        """
        # 读取字典数据
        data_ibook = self.ReadInfo(self.__path['mdat'])
        data_isheet = self.ReadObj(self.__path['mdat'], 0)
        # 建立会员数据库
        #print('会员数据库建立中...')
        for i in range(len(data_isheet)):
            data_isheet[i] = tuple(data_isheet[i])
        self.__info = tuple(data_isheet)
        #print('会员数据库建立完毕！')
        return self.__info
# ----------------------------------------------------------------------------------------------------
    def search(self, key, value):
        """
        搜索会员数据库。
        """
        index = self.__info[0].index(key)
        # 搜索会员数据库
        for i in range(1, len(self.__info)):
            if self.__info[i][index] == value:
                return self.__info[i]
# ----------------------------------------------------------------------------------------------------
    def check(self):
        """
        在数据库中检查是否有重复录入。
        """
        # 数据处理
        input_ibook = self.ReadInfo(self.__path['mnew'])
        input_isheet = self.ReadObj(self.__path['mnew'], 0)
        # 错误报告
        add = []
        old = []
        # 会员数据查重
        add.append([\
            '编号（必填）',\
            '姓名（必填）',\
            '积分（必填）',\
            '折扣（必填）',\
            '余额（必填）',\
            '会员分类（必填）',\
            '联系电话（必填）',\
            '密码',\
            '加入日期',\
            '到期日期',\
            '生日',\
            '电子邮箱',\
            'QQ',\
            '地址',\
            '备注',\
            '允许赊账',\
            '状态'])
        for i in range(1, len(input_isheet)):
            if input_isheet[i][2] != '':
                phone_num = str(int(input_isheet[i][2]))
                res = self.search('联系电话（必填）', phone_num)
                item = [\
                    phone_num,\
                    phone_num,\
                    '0',\
                    '90',\
                    '0',\
                    '贵宾卡',\
                    phone_num]
                if res != None:
                    old.append(item)
                else:
                    add.append(item)
        # 数据输出
        self.WriteObjMulti(self.__path['mtmp'], ['新增', '已有'], [add, old])
        self.WriteObjMulti(self.__path['mout'], ['member'], [add])
        return input_isheet
# ----------------------------------------------------------------------------------------------------
