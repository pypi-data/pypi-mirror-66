# -*- coding: utf-8 -*-


BOT_NAME = 'yzw'
SPIDER_MODULES = ['yzwspider.yzw.spiders']
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
CONCURRENT_REQUESTS = 32
ITEM_PIPELINES = {
    'yzwspider.yzw.pipelines.YzwPipeline': 300,
}

# 日志级别与输出路径
LOG_LEVEL = 'INFO'
LOG_FILE = 'log.txt'



SSDM = '11'
MLDM = '01'
YJXKDM = '0101'

# MYSQL
MYSQL = False
HOST = 'localhost'
USER = 'root'
PASSWORD = ''
PORT = 3306
DATABASE = 'yanzhao'
TABLE = 'major'
CHARSET = 'utf8'
# EXCEL
EXCEL_FILE_NAME = "研招网专业信息"
EXCEL_FILE_PATH = "."



# 固定内容
FCSI_FILE = 'first_class_subject_index.txt'
PROVINCE_LISE = ['11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33', '34', '35', '36', '37',
                '41', '42', '43', '44', '45', '46', '50', '51', '52', '53', '54', '61', '62', '63', '64', '65', '71',
                '81', '82']
PROVINCE_DICT = {'35': '福建', '21': '辽宁', '51': '四川', '34': '安徽', '63': '青海', '42': '湖北', '64': '宁夏', '33': '浙江', '46': '海南',
        '82': '台湾', '61': '陕西', '37': '山东', '41': '河南', '13': '河北', '45': '广西', '54': '西藏', '14': '山西', '81': '澳门',
        '36': '江西', '52': '贵州', '50': '重庆', '44': '广东', '32': '江苏', '53': '云南', '71': '香港', '11': '北京', '31': '上海',
        '23': '黑龙江', '62': '甘肃', '22': '吉林', '65': '新疆', '43': '湖南', '15': '内蒙古', '12': '天津'}
SCHOOL_FEATURE = {'北京大学': '985(自划线)', '中国人民大学': '985(自划线)', '清华大学': '985(自划线)', '北京交通大学': '211', '北京工业大学': '211', '北京航空航天大学': '985(自划线)', '北京理工大学': '985(自划线)', '北京科技大学': '211', '北京化工大学': '211', '北京邮电大学': '211', '中国农业大学': '985(自划线)', '北京林业大学': '211', '北京中医药大学': '211', '北京师范大学': '985(自划线)', '北京外国语大学': '211', '中国传媒大学': '211', '中央财经大学': '211', '对外经济贸易大学': '211', '北京体育大学': '211', '中央音乐学院': '211', '中央民族大学': '985', '中国政法大学': '211', '华北电力大学': '211', '华北电力大学(保定)': '211', '南开大学': '985(自划线)', '天津大学': '985(自划线)', '天津医科大学': '211', '河北工业大学': '211', '太原理工大学': '211', '内蒙古大学': '211', '辽宁大学': '211', '大连理工大学': '985(自划线)', '东北大学': '985(自划线)', '大连海事大学': '211', '吉林大学': '985(自划线)', '延边大学': '211', '东北师范大学': '211', '哈尔滨工业大学': '985(自划线)', '哈尔滨工程大学': '211', '东北农业大学': '211', '东北林业大学': '211', '复旦大学': '985(自划线)', '同济大学': '985(自划线)', '上海交通大学': '985(自划线)', '华东理工大学': '211', '东华大学': '211', '华东师范大学': '985', '上海外国语大学': '211', '上海财经大学': '211', '上海大学': '211', '第二军医大学': '211', '南京大学': '985(自划线)', '苏州大学': '211', '东南大学': '985(自划线)', '南京航空航天大学': '211', '南京理工大学': '211', '中国矿业大学': '211', '中国矿业大学(北京)': '211', '河海大学': '211', '江南大学': '211', '南京农业大学': '211', '中国药科大学': '211', '南京师范大学': '211', '浙江大学': '985(自划线)', '安徽大学': '211', '中国科学技术大学': '985(自划线)', '合肥工业大学': '211', '厦门大学': '985(自划线)', '福州大学': '211', '南昌大学': '211', '山东大学': '985(自划线)', '中国海洋大学': '985(自划线)', '中国石油大学': '211', '中国石油大学(华东)': '211', '中国石油大学(北京)': '211', '郑州大学': '211', '武汉大学': '985(自划线)', '华中科技大学': '985(自划线)', '中国地质大学': '211', '中国地质大学(北京)': '211', '中国地质大学(武汉)': '211', '武汉理工大学': '211', '华中农业大学': '211', '华中师范大学': '211', '中南财经政法大学': '211', '湖南大学': '985(自划线)', '中南大学': '985(自划线)', '湖南师范大学': '211', '国防科学技术大学': '211', '中山大学': '985(自划线)', '暨南大学': '211', '华南理工大学': '985(自划线)', '华南师范大学': '211', '广西大学': '211', '海南大学': '211', '四川大学': '985(自划线)', '西南交通大学': '211', '电子科技大学': '985(自划线)', '四川农业大学': '211', '西南财经大学': '211', '重庆大学': '985(自划线)', '西南大学': '211', '贵州大学': '211', '云南大学': '211', '西藏大学': '211', '西北大学': '211', '西安交通大学': '985(自划线)', '西北工业大学': '985(自划线)', '西安电子科技大学': '211', '长安大学': '211', '西北农林科技大学': '985', '陕西师范大学': '211', '第四军医大学': '211', '兰州大学': '985(自划线)', '青海大学': '211', '宁夏大学': '211', '新疆大学': '211', '石河子大学': '211', '国防科技大学': '985'}
SUBJECT_INDEX = {'01': '哲学', '02': '经济学', '03': '法学', '04': '教育学', '05': '文学', '06': '历史学', '07': '理学',
                '08': '工学', '09': '农学', '10': '医学', '11': '军事学', '12': '管理学', '13': '艺术学'}

CREATE_TEBLE_SQL = "CREATE TABLE `{0}` (" \
                   "`id` char(21) PRIMARY KEY,`招生单位` varchar(40) NOT NULL," \
                   "`院校特性` varchar(10) DEFAULT NULL," \
                   "`院系所` varchar(40) DEFAULT NULL," \
                   "`专业` varchar(40) DEFAULT NULL," \
                   "`研究方向` TINYTEXT DEFAULT NULL," \
                   "`学习方式` varchar(30) DEFAULT NULL," \
                   "`拟招生人数` varchar(40) DEFAULT NULL," \
                   "`业务课一` varchar(40) DEFAULT NULL," \
                   "`业务课二` varchar(40) DEFAULT NULL," \
                   "`外语` varchar(40) DEFAULT NULL," \
                   "`政治` varchar(40) DEFAULT NULL," \
                   "`所在地` varchar(30) DEFAULT NULL," \
                   "`指导老师` TINYTEXT DEFAULT NULL," \
                   "`专业代码` varchar(10) DEFAULT NULL," \
                   "`门类` varchar(20) DEFAULT NULL," \
                   "`一级学科` varchar(40) DEFAULT NULL)" \
                   " ENGINE=MyISAM DEFAULT CHARSET=utf8"