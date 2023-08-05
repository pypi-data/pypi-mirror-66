#coding=utf-8
from distutils.core import setup
setup(
    name="baizhansuperman",#对外我们模块的名字
    version='1.0',#版本号
    description='这是第一个对外发布的模块，测试用的',#描述
    author='xiedongdong',#作者
    author_email='xiedddd@qq444.com',
    py_modules=['baizhansupermath.demo1','baizhansupermath.demo2']#要发布的模块
)