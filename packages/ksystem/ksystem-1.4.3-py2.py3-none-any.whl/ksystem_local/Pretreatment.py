#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# 类 Pretreatment
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-04-12 | Zou Mingzhe   | Ver0.3  | 支付方式名称变更
# 2019-04-28 | Zou Mingzhe   | Ver0.2  | 变更类名
# 2019-04-21 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
import ztools.Xls
import ksystem_local.Process
# ----------------------------------------------------------------------------------------------------
class Pretreatment(ztools.Xls, ksystem_local.Process):
    """
    Pretreatment类，对数据进行预处理。
    """
    def __init__(self):
        self.__version = "0.3"
        self.__info = None
# ----------------------------------------------------------------------------------------------------
    def Version(self, isShow = False):
        """
        返回（屏幕上打印，可选）版本号。
        """
        if(isShow):
            print("[ksystem]-[Pretreatment]-[vesion:%s]" % self.__version)
        return self.__version
# ----------------------------------------------------------------------------------------------------
    def Entry(self, path, dictionary, output):
        """
        录入数据预处理。
        """
        # 路径解析
        output_path = path['odat']
        data_path = path['temp']
        # 字典解析
        size = dictionary['size']
        code = dictionary['code']
        class1 = dictionary['class1']
        class2 = dictionary['class2']
        supplier = dictionary['supplier']
        # 数据处理
        data_ibook = self.ReadInfo(data_path)
        data_isheet = self.ReadObj(data_path, 0)
        # 变量
        for i in range(1, len(data_isheet)):
            if data_isheet[i][1] != '':
                for j in range(len(size)):
                    # 尺码 库存
                    temp_size = data_isheet[0][6 + j]
                    temp_number = data_isheet[i][6 + j]
                    # 输出
                    if temp_number != '':
                        # 信息组合：名称 分类 条码 库存 进货价 销售价 批发价 会员价 积分商品 会员折扣 库存上限 库存下限 供货商 拼音码 颜色 尺码 商品状态 商品描述
                        temp_output = self.encode(data_isheet[i], temp_size, temp_number, size, code, class2, supplier)
                        # 总队列
                        output = output + [temp_output]
        # 数据输出
        self.WriteObj(output_path, 'output', output)
        return output
# ----------------------------------------------------------------------------------------------------
    def Sale(self, path):
        """
        销售数据预处理，分离无用的数据。
        """
        # 数据处理
        #data_ibook = self.ReadInfo(path['idat'])
        data_isheet = self.ReadObj(path['idat'], 0)
        # 数据预处理
        documents = []    # 销售单据
        products  = []    # 销售明细
        documents.append(['流水号', '日期', '时间', '类型', '店铺', '会员', '数量', '原价', '实收', '现金', '银联', '微信', '支付宝'])
        products.append(['流水号', '供应商', '商品', '货号', '条码', '数量', '原价', '实收'])
        number = ''       # 单据号
        index  = 0        # 流水号，用于单张单据多个商品
        # 处理标题，将标题的列号取出到column
        column = {}       # 标题的列号
        title = data_isheet[0]
        for i in range( len(title) ):
            #print(title[i])
            column[title[i]] = i
        #print(column)
        # 处理数据
        for i in range(1, len(data_isheet)):
            #print(data_isheet[i])
            old = data_isheet[i]
            if old[0] != '':
                # 销售单据 documents
                new = []
                new.append( old[column['流水号']] )    # 流水号
                new.append( old[column['日期']][:10] ) # 日期
                new.append( old[column['日期']][11:] ) # 时间
                new.append( old[column['类型']] )      # 类型
                new.append( old[column['收银员']] )    # 店铺
                new.append( old[column['会员']] )      # 会员
                new.append( str(int(float(old[column['商品数量']]))) ) # 数量
                new.append( str(int(float(old[column['商品原价']]))) ) # 原价
                new.append( str(int(float(old[column['实收金额']]))) ) # 实收
                new.append( str(int(float(old[column['现金支付']]))) ) # 现金
                new.append( str(int(float(old[column['银联支付']]))) ) # 银联
                new.append( str(int(float(old[column['微信']]))) )     # 微信
                new.append( str(int(float(old[column['支付宝']]))) )   # 支付宝
                number = old[column['流水号']]
                index = 0
                documents.append(new)
                # print(new)
            elif old[6].startswith('牌号：') != True and old[6] != '抹零' and old[6].startswith('原单据号：') != True and old[6] != '':
                # 销售明细 products
                new = []
                # 生成流水号
                index += 1
                new.append( number + '-%d' % (index) )   # 流水号
                # 解析供应商、商品、货号、条码
                su = '' # 供应商
                fo = old[column['商品信息']] # 商品
                no = old[column['商品条码']] # 货号
                co = old[column['商品条码']] # 条码
                if len(no) > 5: # 截取货号，-11xx为尺码信息
                    if no[-5] == '-':
                        no = no[:-5]
                if no == '': # 无码商品 = 100 + 价格
                    su = '100'
                    no = '100-' + str(old[6])
                    co = no + '-1182'
                elif no[:1] != '1': # 前两位为供应商
                    su = no[:2]
                else: # 10-19用于扩展供应商至101-199
                    su = no[:3]
                new.append( su ) # 供应商
                new.append( fo ) # 商品
                new.append( no ) # 货号
                new.append( co ) # 条码
                new.append( str(int(float(old[column['商品数量']]))) ) # 数量
                new.append( str(int(float(old[column['商品原价']]))) ) # 原价
                new.append( str(int(float(old[column['实收金额']]))) ) # 实收
                products.append(new)
                # print(new)
        # 数据输出
        self.WriteObjMulti(path['odat'], ['销售单据', '销售明细'], [documents, products])
# ----------------------------------------------------------------------------------------------------
