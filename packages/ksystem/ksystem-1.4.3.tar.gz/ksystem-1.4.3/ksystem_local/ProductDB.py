#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# 类 ProductDB
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2019-04-29 | Zou Mingzhe   | Ver0.3  | 1.增加 dict(self)
#            |               |         | 2.增加 check(self, stock = False)
# 2019-04-28 | Zou Mingzhe   | Ver0.2  | 变更类名
# 2019-04-21 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
import ztools.Xls
import ksystem_local.Process
# ----------------------------------------------------------------------------------------------------
class ProductDB(ztools.Xls, ksystem_local.Process):
    """
    ProductDB类，构建商品数据库。
    """
    def __init__(self, path):
        self.__version = "0.3"
        self.__path = path
        self.__info = None
        self.__dict = None
# ----------------------------------------------------------------------------------------------------
    def Version(self, isShow = False):
        """
        返回（屏幕上打印，可选）版本号。
        """
        if(isShow):
            print("[ksystem]-[ProductDB]-[vesion:%s]" % self.__version)
        return self.__version
# ----------------------------------------------------------------------------------------------------
    def dict(self):
        """
        构建字典。
        """
        # 读取字典数据
        dict_ibook = self.ReadInfo(self.__path['dict'])
        size_isheet = self.ReadObj(self.__path['dict'], dict_ibook.index('size'))
        class_isheet = self.ReadObj(self.__path['dict'], dict_ibook.index('class'))
        # 建立字典
        info = {}
        # 建立尺寸字典
        size = {}
        for i in range(len(size_isheet)):
            size[size_isheet[i][0]] = size_isheet[i][1]
        # 建立分类字典
        code = {}
        class1 = {}
        class2 = {}
        supplier = {}
        for i in range(len(class_isheet)):
            code[class_isheet[i][0]] = class_isheet[i][1]
            class2[class_isheet[i][0]] = class_isheet[i][2]
            class1[class_isheet[i][0]] = class_isheet[i][3]
            supplier[class_isheet[i][0]] = class_isheet[i][4]
        # 合并字典
        self.__dict = {}
        self.__dict['size'] = size
        self.__dict['code'] = code
        self.__dict['class1'] = class1
        self.__dict['class2'] = class2
        self.__dict['supplier'] = supplier
        return self.__dict
# ----------------------------------------------------------------------------------------------------
    def build(self):
        """
        构建商品数据库。
        """
        # 读取字典数据
        data_ibook = self.ReadInfo(self.__path['dats'])
        data_isheet = self.ReadObj(self.__path['dats'], 0)
        # 建立商品数据库
        #print('商品数据库建立中...')
        for i in range(len(data_isheet)):
            data_isheet[i] = tuple(data_isheet[i])
        self.__info = tuple(data_isheet)
        #print('商品数据库建立完毕！')
        return self.__info
# ----------------------------------------------------------------------------------------------------
    def search(self, key, value):
        """
        搜索商品数据库。
        """
        index = self.__info[0].index(key)
        # 搜索商品数据库
        for i in range(1, len(self.__info)):
            if self.__info[i][index] == value:
                return self.__info[i]
# ----------------------------------------------------------------------------------------------------
    def check(self, stock = False):
        """
        在数据库中检查是否有重复录入。
        """
        # 字典解析
        size = self.__dict['size']
        code = self.__dict['code']
        class1 = self.__dict['class1']
        class2 = self.__dict['class2']
        supplier = self.__dict['supplier']
        # 数据处理
        self.copy(self.__path['idat'], self.__path['temp'])
        input_ibook = self.ReadInfo(self.__path['idat'])
        input_isheet = self.ReadObj(self.__path['idat'], 0)
        # 错误报告
        different = []
        change = []
        nofind = []
        # 商品数据查重
        for i in range(1, len(input_isheet)):
            if input_isheet[i][1] != '':
                bcmd = False
                cmd = "N"
                for j in range(len(size)):
                    # 尺码 库存
                    i_size = input_isheet[0][6 + j]
                    i_number = input_isheet[i][6 + j]
                    # 信息组合：名称 分类 条码 库存 进货价 销售价 批发价 会员价 积分商品 会员折扣 库存上限 库存下限 供货商 拼音码 颜色 尺码 商品状态 商品描述
                    encode_info = self.encode(input_isheet[i], i_size, i_number, size, code, class2, supplier)
                    i_code = encode_info[2]
                    # 查重
                    if i_number != '':
                        res = self.search('条码', i_code)
                        if res != None:
                            # 列表化
                            res = list(res)
                            res = self.decode_database(res)
                            # print(encode_info)
                            # print(res)
                            # 商品比对
                            num1 = int(float(encode_info.pop(3)))
                            num2 = int(float(res.pop(3)))
                            # 商品比对
                            if encode_info != res:
                                different.append(encode_info)
                                different.append(res)
                                different.append([])
                            if encode_info != res and bcmd == False:
                                print('录入商品信息冲突（第一行：库存信息，第二行：录入信息）：')
                                print(res)
                                print(encode_info)
                                bcmd = True
                                if stock == False:
                                    cmd = input("使用录入信息且合并库存数据(Y)？")
                                # else:
                                #     print('已用录入信息替换原信息！')
                            if (encode_info == res or cmd == "Y") and stock == False:
                                input_isheet[i][4] = '补'
                                input_isheet[i][5] = str(int(float(input_isheet[i][5])) + num2)
                                input_isheet[i][6 + j] = str(num1 + num2)
                                print('录入商品库存变更：', encode_info[0], encode_info[13], encode_info[14], '：', num1, '->', num1 + num2)
                                change.append(input_isheet[i])
                        elif stock == True:
                            # print('未找到库存：')
                            # print(encode_info)
                            nofind.append(encode_info)
        # 数据输出
        self.WriteObjMulti(self.__path['temp'], ['check', '冲突', '变更', '未找到库存'], [input_isheet, different, change, nofind])
        return input_isheet
# ----------------------------------------------------------------------------------------------------
