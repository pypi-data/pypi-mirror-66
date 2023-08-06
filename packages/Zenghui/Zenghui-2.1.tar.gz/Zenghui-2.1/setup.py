from distutils.core import setup

setup(
    name='Zenghui', # 对外我们模块的名字
    version='2.1', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='gaoqi', # 作者
    author_email='gaoqi110@163.com',
    py_modules=['Zenghui.B1','Zenghui.B2'] # 要发布的模块
)