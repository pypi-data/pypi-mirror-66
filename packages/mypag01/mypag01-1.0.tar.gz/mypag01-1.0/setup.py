from distutils.core import setup

setup(
    name='mypag01', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='jiaxiong_ye', # 作者
    author_email='2366728342@qq.com',
    py_modules=['mypag01.demo01'] # 要发布的模块
)