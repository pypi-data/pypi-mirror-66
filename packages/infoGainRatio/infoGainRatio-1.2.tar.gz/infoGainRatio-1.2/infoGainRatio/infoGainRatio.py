import numpy as np

# 进行数据整理
# from scipy import stats


class gain:

    """
    计算信息熵
    """
    def entropy(data, att_name):
        """
        data: 数据集
        att_name: 需要计算信息熵的属性名
        lables: att_name的取值
        """
        lables = data[att_name].unique()
        # 信息熵
        ent = 0
        for lv in lables:
            pi = sum(data[att_name]==lv) / data.shape[0]
            ent += pi*np.log(pi)
        return -ent


    # """
    # 通过scipy内置的stats.entropy函数计算信息熵
    # 使用的log是以自然对数e为底
    # """
    # def entropy_scipy(data, att_name):
    #     """
    #     data: 数据集
    #     att_name: 需要计算信息熵的属性名
    #     n: data数据集中数据总数
    #     values:
    #     """
    #     n = data.shape[0]
    #     """
    #     data['name']value_counts(): 计算name中有哪些不同的值，并计算每个值有多少个重复值
    #     """
    #     values = data[att_name].value_counts()
    #     return stats.entropy(values/n)


    """
    计算条件信息熵
    """
    def conditional_entropy(data, xname, yname):
        """
        data: 数据集
        xname: 数据集的分类标准属性
        yname: 需要求条件信息熵的特征
        """
        xlable = data[xname].unique()
        ylable = data[yname].unique()
        """
        px: xname中 不同取值所占的比例 
        """
        px= data[xname].value_counts() / data.shape[0]
        """
        计算属性xname的条件信息熵
        """
        ce = 0
        for xl in xlable:
            ce += px[xl]*gain.entropy(data[data[xname]==xl], yname)
        return ce


    """
    计算信息增益
    """
    def gain(data, xname, yname):
        """
        data: 数据集
        xname: 数据集的分类标准属性
        yname: 需要求条件信息熵的特征
        en: 数据集data中属性yname的信息熵
        ce: 在属性xname的条件下，属性yname的信息熵
        """
        en = gain.entropy(data, yname)
        ce = gain.conditional_entropy(data, xname, yname)
        return en - ce



    """
    计算信息增益率
    """
    def gain_ratio(data, xname, yname):
        """
        data: 数据集
        xname: 数据集的分类标准属性
        yname: 需要求条件信息熵的属性
        ig: 在属性xname条件下，属性yname的信息增益
        ie: 属性xname的信息熵
        """
        ig = gain.gain(data, xname, yname)
        ie = gain.entropy(data, xname)
        return ig / ie


