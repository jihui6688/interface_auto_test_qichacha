>  近期在测试公司的大数据接口开放平台，原型及设计都是参照企查查的大数据接口平台（简直就是企查查的翻版，不过目前功能还没有企查查强大），针对公司的大数据接口开放平台，我自己设计了一套接口自动化测试框架。在这篇文章里，我把那套框架重新运用到对企查查大数据接口的自动化测试上

- 之前也写过 2 篇关于接口自动化测试的文章，在文章列表中可以找的到，分别是用 Python 的 requests 库和 jmeter 作为测试工具的

### 接口自动化测试框架的功能介绍

1. 使用Python 的 requests 库作为接口测试工具（Python 的 requests 库非常强大，可以作为接口测试工具，也可以作为爬虫获取网页数据的工具，同时开源性能测试工具 Locust 也是使用 requests 库对待测接口进行压力测试的，之前写的文章有介绍）
2. 使用 yaml 文件作为参数的配置文件（在公司搭建测试环境时，经常会使用 yaml 文件作为配置文件，yaml 和 python 一样简洁高效，二者的组合简直就是 perfect，CSDN 上的这篇文章介绍了 yaml 及 如何用 Python 操作 yaml：[yaml 介绍的链接](https://blog.csdn.net/lmj19851117/article/details/78843486)）
3. 完全实现了参数化及数据驱动：所有的数据都写在 yaml 文件中，实现了代码与数据的分离。可同时对任意多个不同的接口以及同一个接口的不同用户输入进行自动化测试，需要新增测试的接口或新增用户输入参数时，只需将相应的参数加入到 yaml 文件即可
4. 使用 unittest 作为单元测试框架，使用 HTMLTestRunner 对生成的测试报告进行美化
5. 使用 jenkins 作为持续集成工具，可手工启动 jenkins 进行构建，或在 jenkins 中设置定时执行
6. 测试执行完成并生成测试报告后，通过邮件将测试报告发送给指定的接收人

###  企查查接口的介绍

#### 申请接口

要对企查查接口进行自动化测试，首先必须对其有所了解，我们通过手机号注册企查查开放接口平台后，可以申请企查查的接口并免费使用指定的次数，如下图：

![申请企查查接口.png](https://upload-images.jianshu.io/upload_images/12273007-ea8abe3ae80dcb24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

申请的每个接口都有一定的免费使用测试

![免费使用次数.png](https://upload-images.jianshu.io/upload_images/12273007-7628d9d574f5dfad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 通过页面调用接口

我们点击上图某一已申请接口的调用测试链接，会进入接口调用页面，如下图：

![页面请求png.png](https://upload-images.jianshu.io/upload_images/12273007-3698b79dc85f31e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在页面的左下方输入请求参数，点击“调用新街口”按钮，页面的右上方会显示请求参数，右下方会显示响应参数

### 接口参数及调用介绍

上面介绍的是通过页面对接口进行调用，下面进入正题：使用 Python 自动化测试框架调用接口

在介绍自动化测试框架之前，我们必须对待测的接口有所了解，企查查在页面上对每一个接口都有详细非介绍，可以作为我们的需求文档，如下图：

![接口参数png.png](https://upload-images.jianshu.io/upload_images/12273007-3a4adfd24c5b5359.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

响应参数的错误码：

![错误码.png](https://upload-images.jianshu.io/upload_images/12273007-7ae8af0264cb63f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过上面接口详情页面对接口的介绍，我们可以得到接口的  URL、接口的权限验证、输入参数、输出参数、错误码等信息，这些参数可以作为我们设计用例的依据

### 测试框架代码的介绍

测试框架代码的目录结构如下图所示：

![项目目录结果.png](https://upload-images.jianshu.io/upload_images/12273007-fa701bbce402c724.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. case目录
-  run.py：脚本执行的入口
-  test_case.py：存放测试用例的目录
2. conf目录
- conf.yal：接口参数的配置文件，存放测试数据
- setting.py：存放系统中各个模块的路径
3. report目录：

存放生成的测试报告
4. util 目录：
- get_request_parameters.py：获取yaml文件中存放的接口参数，用来进行参数化
5. HTMLTestRunner.py：

用来对unittest 生成的报告进行美化
6. send_email.py：

将生成的测试报告发送给指定的接收人

- 通过前面的介绍，我们知道，在页面上调用接口时，只需要在输入框填写参数，然后点击“调用新接口”按钮即可成功调用接口，但是通过代码调用接口时，必须把所有的参数准备好，下面介绍接口的请求参数

### 权限验证

一般接口在设计时，都会给接口添加相应的访问权限，如果没有权限调用，任何人都可以调用高接口。企查查的接口也有权限验证，如下图：

![权限验证.png](https://upload-images.jianshu.io/upload_images/12273007-ab55622d176b5942.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 从上图我们可以得知，在接口请求的 URL 中，除了用户输入的请求参数外，我们还需要带上权限验证的参数，上图要求我们 通过 http header 头的方式传统 Token ：验证加密值（key+Timespan+SecretKey组成的32位md5加密的大写字符串）和 Timespan：精确到秒的Unix时间戳 这两个参数

- 如果我们在请求参数中不带上包含这两个参数的 header，请求就会被拦截，进而请求失败

下面是用来生成请求参数的 header 的代码，在 util.get_request_parameters.py 文件中写了生成权限验证的
代码，如下：

```
# 获取时间戳
def get_time_tup():
    """ :return: 13位精确到秒的时间戳
    """
    time_tup = str(int(time.time()))
    return time_tup

# md5加密
def set_md5(s):
    """
    :param s: 拼接的字符串
    :return: md5加密再转化为大写的字符串
    """
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    s_md5 = new_md5.hexdigest().upper()
    return  s_md5

# 设置请求头
def get_headers(key, screat_key):
    """
    :param key: 我的key
    :param screat_key: 我的密钥
    :return: 请求头
    """
    headers = dict()
    token = key + get_time_tup() + screat_key
    headers["Token"] = set_md5(token)
    headers["Timespan"] = get_time_tup()
    return headers
```
###  参数化
- 测试过程中，我们需要使用不同的请求参数对接口进行测试，这时候就需要对这些参数进行参数化，我使用的是 nose-parameterized（一个针对Python单元测试框架实现参数化的扩展）来进行参数化的，需要 pip install 一下相应的安装包。如下的链接介绍了nose-parameterized 的使用：[nose-parameterized 介绍的链接](https://www.cnblogs.com/royfans/p/7226360.html)
- nose-parameterized 参数化的具体使用，我在代码中有详尽的注释

###  测试用例的设计

- 设计了针对如下4个接口的的自动化测试： 企查查的企业对外投资接口（3个用例）、企业对外投资穿透接口（2个用例）、受益人穿透接口（2个用例）、企业人员董监高信息（1个接口），共8个接口
如下图：
![测试的接口.png](https://upload-images.jianshu.io/upload_images/12273007-67562ef607e8a97a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 在设计测试用例时，为了测试方便起见，只对接口返回的 http 响应状态码进行验证（也可以对多个其他的字段进行验证）
### Jenkins 构建
构建的过程如下：
1、首先得在 jenkins 里面新建一个项目，输入项目名称，选择构建一个自由风格的软件项目，再点击确定，如下图所示：

![构建一个自由风格的任务.png](https://upload-images.jianshu.io/upload_images/12273007-87166bcc649fb238.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、接着，在构建里面填上添加 Windows 批处理命令，然后点击确定，如下：
```
cd C:\Users\Administrator\eclipse-workspace1\qichacha_interface_auto_test\case
C:\Users\Administrator\AppData\Local\Programs\Python\Python37-32\python.exe  run.py
```
![windows批处理.png](https://upload-images.jianshu.io/upload_images/12273007-5243e80ded5f35a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、在jenkins 中找保存成功的项目，点击立即构建。构建完成后，发现构建失败了，报错信息如下：
```
Traceback (most recent call last):
  File "run.py", line 3, in <module>
    from util.HTMLTestRunner import HTMLTestRunner
ModuleNotFoundError: No module named 'util'
```
截图如下：

![找不到模块.png](https://upload-images.jianshu.io/upload_images/12273007-69fa2d6bcbaac272.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但是，在eclipse 中运行时，没有报错
- 产生的原因：

IDE运行时，会搜索全部相关的模块；而通过Jenkins来配置时，则只会搜索当前目录下的模块
- 解决的方法
配置Jenkins的环境变量 PYTHONPATH，值为该 Python 工程的路径，如下：
```
C:\Users\Administrator\eclipse-workspace1\qichacha_interface_auto_test
```
如下图所示：

![全局环境变量.png](https://upload-images.jianshu.io/upload_images/12273007-9e8c31ce09e95d86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 构建日志

添加了Jenkins的环境变量 PYTHONPATH 后，就可以构建成功了，构建的日志如下：

![构建日志.png](https://upload-images.jianshu.io/upload_images/12273007-41e45c6c143399af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 生成的测试报告

生成的测试报告如下：

![报告测试结果汇总.png](https://upload-images.jianshu.io/upload_images/12273007-f73c5a10833a5eb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击测试报告中的 pass 或 fail 链接，会显示测试执行的详情信息，如下图：

![报告错误的详情.png](https://upload-images.jianshu.io/upload_images/12273007-3a677de33f669df1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 邮件通知
生成测试报告后，会自动将生成的测试报告发送给指定的接收人，邮件如下：

![邮件png.png](https://upload-images.jianshu.io/upload_images/12273007-0bc1d8cfc3f8a0fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
