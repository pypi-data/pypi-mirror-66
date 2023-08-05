#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# 类 Process
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2019-04-28 | Zou Mingzhe   | Ver0.2  | 变更类名
# 2019-04-21 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
class Process:
    """
    Process类，信息编码处理。
    """
    def __init__(self):
        self.__version = "0.2"
# ----------------------------------------------------------------------------------------------------
    def Version(self, isShow = False):
        """
        返回（屏幕上打印，可选）版本号。
        """
        if(isShow):
            print("[ksystem]-[Process]-[vesion:%s]" % self.__version)
        return self.__version
# ----------------------------------------------------------------------------------------------------
    def encode(self, idata, isize, inumber, size, code, class2, supplier):
        """
        信息编码。
        """
        # data格式：名称 分类 货号 价格 补货 数量 均码 ...
        # 颜色colour
        clr = '-'
        # 积分商品member 会员折扣point
        mbr = '是'
        pt = '是'
        # 库存上限 库存下限
        upper = '100'
        lower = '0'
        # 拼音码cn 商品状态state 商品描述description
        cn = ''
        st = '启用'
        desc = ''
        # 分类class 货号Art.No
        cl = idata[1]
        art = idata[2]
        # 尺码 库存
        sz = isize
        num = inumber
        # 名称 条码 分类
        name = idata[0]
        if ((name == None) or (name == "")):
            name = code[cl] + art
        code = code[cl] + art + size[sz]
        # price 进货价 销售价 批发价 会员价
        pr_buy = '0'
        pr_sale = idata[3]
        pr_trade = pr_sale
        pr_vip = pr_sale
        # 供货商 分类
        supplier = supplier[cl]
        cl = class2[cl]
        # 信息组合：名称 分类 条码 库存 进货价 销售价 批发价 会员价 积分商品 会员折扣 库存上限 库存下限 供货商 拼音码 颜色 尺码 商品状态 商品描述
        encode_info = [name, cl, code, num, pr_buy, pr_sale, pr_trade, pr_vip, pt, mbr, upper, lower, supplier, cn, clr, sz, st, desc]
        return encode_info
# ----------------------------------------------------------------------------------------------------
    def decode_info(self, idata):
        """
        信息解码。
        """
        return idata
# ----------------------------------------------------------------------------------------------------
    def decode_database(self, idata):
        """
        数据库解码。
        """
        # 移除非必要项
        idata.pop(19)
        idata.pop(18)
        idata.pop(14)
        idata.pop(13)
        # 数字整形化
        idata[3] = str(int(float(idata[3])))
        idata[4] = str(int(float(idata[4])))
        idata[5] = str(int(float(idata[5])))
        idata[6] = str(int(float(idata[6])))
        idata[7] = str(int(float(idata[7])))
        idata[10] = str(int(float(idata[10])))
        idata[11] = str(int(float(idata[11])))
        idata[13] = ''
        return idata
# ----------------------------------------------------------------------------------------------------
