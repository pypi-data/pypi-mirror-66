<h1 id="pygrading" align="center">PyGrading</h1>

<p align="center">CourseGrading(希冀)计算机专业课一体化在线平台开发用Python工具包。包含通用评测内核创建以及HTML标签生成工具。</p>

<p align="center">
	<a href="http://www.educg.net/">
		<img src="https://img.shields.io/badge/site-CG-red"
				 alt="Official Site">
	</a>
	<a href="https://github.com/PhenomingZ/PyGrading">
		<img src="https://img.shields.io/github/stars/PhenomingZ/PyGrading"
				 alt="GitHub stars">
	</a>
	<a href="https://pypi.org/project/pygrading/">
			<img src="https://img.shields.io/badge/pypi-v0.4.1-orange"
					 alt="Pypi package">
		</a>
	<a href="https://github.com/PhenomingZ/PyGrading/issues">
				<img src="https://img.shields.io/github/issues/PhenomingZ/PyGrading"
						 alt="GitHub issues">
	</a>
	<a href="https://github.com/PhenomingZ/PyGrading/blob/master/LICENSE">
				<img src="https://img.shields.io/github/license/PhenomingZ/PyGrading"
						 alt="GitHub license">
	</a>
</p>

<p align="center">
	<a href="#what-is-it">What is it</a> •
	<a href="#install">Install</a> •
	<a href="#change-log">Change Log</a> •
	<a href="#getting-start">Getting Start</a> •
	<a href="#api">API</a> •
	<a href="#tutorials">Tutorials</a> •
	<a href="#faq">FAQ</a> •
	<a href="http://www.educg.net/" target="_blank">CG Site</a>
</p>

<p align="center">
		<img src="./img/logo.png" width="200">
</p>

<h6 align="center">Made by Charles Zhang • :globe_with_meridians: <a href="https://github.com/PhenomingZ">https://github.com/PhenomingZ</a></h6>

<h2 id="what-is-it" align="center">What is it</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

**希冀平台** 是一个国内最具专业深度、安全可扩展的计算机类课程一体化支撑平台，是一个定位于全面支撑计算机、人工智能和大数据专业建设的大型综合教学实验平台，而非一个只能支撑若干门课程的实验系统。

**通用评测** 是一个通用的自动评测框架，基于该框架可以定制开发任何自己需要的自动评测内核。

**PyGrading工具包** 目前该工具包包含以下功能：
1. 支持CourseGrading平台通用评测内核快速构建；
2. 支持适用于通用评测题和虚拟桌面环境的评测结果JSON串的快速生成；
2. 支持HTML标签文本内容的快速生成，绝对好用的HTML生成工具；

希望使用本工具能够提高大家的工作效率，祝各位开发顺利！

<h2 id="install" align="center">Install</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

使用pip可以轻松安装PyGrading：

```bash
pip install pygrading
```

也可以下载项目文件后，切换到`setup.py`所在的目录，执行以下命令来安装：

```bash
python setup.py install
```

也可使用下面的Dockerfile来构建一个装有PyGrading的通用评测环境：

```dockerfile
FROM jupyter/base-notebook

LABEL maintainer="Charles Zhang <694556046@qq.com>"

RUN pip install pygrading
```

切换至Dockerfile所在的目录，构建镜像命令为：

```bash
docker build -t cg/pygrading_env .
```

> 该镜像包含基本的Jupyter环境，可直接用于创建Jupyter调试环境。

启动镜像命令为：

```bash
docker run -it --name pygrading -p 8888:8888 cg/pygrading_env
```

> `8888`端口为Jupyter服务所需，如果被占用可以映射为其他端口

PyGrading的运行环境要求 **Python >= 3.7**，不支持Python2。

<h2 id="change-log" align="center">Change Log</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

**v0.4.1 Change Log (2020.04.20)**  
1. 将`gg.Job`类中的私有属性更新为公有属性，可以依据需求灵活配置。
2. 为`gg.Job`类添加了`set_prework()`、`set_run()`和`set_postwork()`函数，同时更新了该模块使用的最佳实践，样例将在后续版本中更新至文档。

**v0.4.0 Change Log (2020.03.26)**  
1. 添加了`gg.utils.exec(cmd: str, stdin: str = "")`函数

该函数用于执行Shell命令，相较于`gg.utils.bash(cmd)`函数新增特性如下：
    1. 支持区分`stdout`、`stderr`输出的内容；
    2. 支持直接添加标准输入字符串内容；
    3. 支持快速查看所执行的命令；
    4. 返回值优化为一个专用类，方便查看返回值包含的内容。

样例代码
```python
import pygrading.general_test as gg

ret = gg.utils.exec("python3 ./test/input_test.py", "Charles Zhang!")

print("======= Stdout =======")
print(ret.stdout)
print("======= Stderr =======")
print(ret.stderr)
print("======== Cmd =========")
print(ret.cmd)
print("======== Time ========")
print(ret.exec_time)
print("===== ReturnCode =====")
print(ret.returncode)
```

`input_test.py`中的内容如下：

```python
# 标准输出
name = input("what is your name?\n")
print(name)

# 错误输出
div = 1 // 0
```

执行后输出如下：

```
======= Stdout =======
what is your name?
Charles Zhang!

======= Stderr =======
Traceback (most recent call last):
  File "./test/input_test.py", line 6, in <module>
    div = 1 // 0
ZeroDivisionError: integer division or modulo by zero

======== Cmd =========
python3 ./test/input_test.py
======== Time ========
60
===== ReturnCode =====
1
```

<details>
<summary>以往版本更新日志(点击以展开...)</summary>
<br>

**v0.3.3 Change Log (2020.03.11)**  
1. 向`Job`类中补充了`secret`函数，用于设定输出JSON串的`secret`字段。

**v0.3.2 Change Log (2020.03.11)**  
1. 添加了Docker Network和Docker Volume功能，可快速创建容器网络和数据卷。

**v0.3.1 Change Log (2020.03.11)**  
1. 添加了批量复制文件到Docker容器的功能，支持在集群中分发文件。

**v0.3.0 Change Log (2020.03.10)**  
1. 添加了Docker控制模块，支持批量创建容器集群！

```python
import pygrading.docker as pk

# 创建节点名列表，也可不指定节点名，而根据集群名自动创建节点名称
name_list = ["node1", "node2", "node3", "node4"]

# 通过节点数，镜像名称等信息，创建Docker集群
cluster = pk.Cluster("mpi_cluster", 4, "cg/thread-kernel", network="mpi-network", name_list=name_list)

# 清理宿主机上的同名容器
cluster.clear()

# 创建集群
cluster.create()

# 集群执行命令
ret = cluster.exec("hostname")

print(ret)

"""
输出如下

[(0, 'b48a431f99e4', 248), (0, '152cfff79baf', 258), (0, '6ca9560f210f', 230), (0, 'e6800022a16e', 240)]
"""
```

**v0.2.9 Change Log (2020.03.06)**  
1. 修复了上个版本更新导致的新Bug。

**v0.2.8 Change Log (2020.03.06)**  
1. 修复了`html.str2html()`函数接受到空字符串时导致程序崩溃的问题。

**v0.2.7 Change Log (2020.03.05)**  
1. 现在结果设定函数`job.images()`中默认接受的参数类型从`str`调整为`List[str]`。

**v0.2.6 Change Log (2020.03.04)**  
1. 现在使用如下方式引用PyGrading即可在定义流程函数时对`job`对象和`testcases`指定类型。
```python
import pygrading.general_test as gg

def prework(job: gg.Job):
    pass

def run(job: gg.Job, testcases: gg.TestCases.SingleTestCase):
    pass

def postwork(job: gg.Job):
    pass
```

**v0.2.5 Change Log (2020.03.04)**  
1. 现在使用如下方式引用PyGrading即可在定义流程函数时对`job`对象和`testcases`指定类型。
```python
import pygrading.general_test as gg

def prework(job: gg.Job):
    pass

def run(job: gg.Job, testcases: gg.TestCases.SingleTestCase):
    pass

def postwork(job: gg.Job):
    pass
```

**v0.2.4 Change Log (2020.03.03)**  
1. 添加了`gg.job.get_result()`函数，解决了之前只能直接打印结果，无法获得执行结果对象的问题。

**v0.2.3 Change Log (2020.03.03)**  
1. 修复了`pygrading.general_test.compiler`模块中`c/c++`编译功能的问题，将编译选项`option`移动至生成编译命令的最后，添加了`flag`字段位于源文件字段之前，用与设定编译版本标志如`-std=c++11`

**v0.2.2 Change Log (2020.03.03)**  
1. 发现Python3.6以下版本可能会出现包导入错误，暂时仅支持Python3.7以上版本。

**v0.2.1 Change Log (2020.02.09)**  
1. 添加了构建通用评测环境的Dockerfile
2. 增加了`__version__`变量，方便查看程序包版本：
```python
import pygrading.general_test as gg

# 获取版本信息字符串
print(gg.__version__)

# 直接打印版本信息
gg.version()
```

**v0.2.0 Change Log (2020.02.04)**  
1. 使用文档施工完成；
2. 修复了postwork函数为None时prework函数不工作的问题；
3. 读写文件功能增加了读写选项；
4. HTML模块增加了`<br>`标签的支持。

**v0.1.2 Change Log (2020.02.01)**  
在`pygrading.heml`模块中添加了自定义标签方法`custom()`并支持形如`<input>`标签的不成组标签。

**v0.1.0 Change Log (2020.01.29)**  
通用评测内核功能完成，HTML构建功能初步搭建完成。

</details>

<h2 id="getting-start" align="center">Getting Start</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

### 通用评测内核构建

#### 1. 设计逻辑

PyGrading采用三段式的设计逻辑，将每一次评测任务分为三个阶段，分别完成“评测任务预处理”、“评测用例执行”、“评测结果处理”，如下图所示：

<p align="center">
		<img src="./img/flow.png" width="500">
</p>

**评测任务预处理** 通常包括读取配置文件信息、读取评测用例信息、编译学生提交的文件等任务。

**评测用例执行** PyGrading会自动迭代执行评测用例列表中的每个评测用例，而具体的评测规则可以用一个函数快速指定。

**评测结果处理** 通常包括评测结果汇总、生成评测报告、输出评测结果JSON串等任务。

在本文档这一部分接下来的内容中，将以一个普通编程题为例，创建一个评测内核并输出结果JSON串，样例题目如下：

> 题目名称：判断回文数  
> 问题描述：判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。  
> 示例 1:  
> 　　输入：121  
> 　　输出：True  
>
> 示例 2：  
> 　　输入：-121  
> 　　输出：False  
> 　　说明：从左向右为“-121”，从右向左为“121-”，故不是回文数。

本例使用的学生提交代码如下：
```python
def isPalindrome(num: int) -> bool:
    num = abs(num)
    num_str = str(num)
    return num_str == num_str[::-1]

x = eval(input())
print(isPalindrome(x))
```

本例使用的测试用例如下：
<table>
    <tr>
        <th>input</th>
        <th>output</th>
    </tr>
    <tr>
        <td>121</td>
        <td>True</td>
    </tr>
    <tr>
        <td>10</td>
        <td>False</td>
    </tr>
    <tr>
        <td>-12</td>
        <td>False</td>
    </tr>
    <tr>
        <td>331133</td>
        <td>True</td>
    </tr>
    <tr>
        <td>-121</td>
        <td>False</td>
    </tr>
</table>

> 样例学生代码在执行最后一组测试用例时会输出错误答案，本示例所有代码均可在`./example/GettingStart`目录下找到。

#### 2. 导入程序包

PyGrading安装完成之后，推荐在您的代码中使用如下方式导入通用评测相关模块：

```python
import pygrading.general_test as gg
```

如果您需要在评测结果中显示html内容，推荐如下方式导入html相关模块：

```python
from pygrading.html import *
```

#### 3. 创建评测任务预处理函数

首先创建用于评测任务预处理的`prework()`函数，完成配置文件和评测用例的读取，配置文件使用JSON格式，内容如下：

```json
{
    "testcase_num": "5",
    "testcase_dir": "./example/GettingStart/testdata",
    "submit_path": "./example/GettingStart/submit/main.py"
}
```

PyGrading推荐按照如下目录结构构建评测数据，学生提交的代码将会被挂载到`submit`目录中，测试数据的输入输出存放于`testdata`目录中。PyGrading提供了函数可用于直接读取以这种目录结构创建的评测用例：

```
.
├── config.json
├── submit
│   └── main.py
└── testdata
    ├── input
    │   ├── input1.txt
    │   ├── input2.txt
    │   ├── input3.txt
    │   ├── input4.txt
    │   └── input5.txt
    └── output
        ├── output1.txt
        ├── output2.txt
        ├── output3.txt
        ├── output4.txt
        └── output5.txt
```

创建`prework()`函数的代码如下，`job`为PyGrading创建的任务实例：

```python
def prework(job: gg.Job):
    # 读取配置文件
    config = gg.load_config("./example/GettingStart/config.json")

    # 创建测试用例实例
    testcases = gg.create_std_testcase(config["testcase_dir"], config["testcase_num"])

    job.set_config(config)
    job.set_testcases(testcases)
```

#### 4. 创建评测用例执行函数

接下来创建创建用于执行测试用例的`run()`函数，该函数接收单组测试用例，并返回一个可包含任意内容的字典，所有评测用例返回的内容最终会汇总到一个列表中传递给评测结果处理函数。

使用`gg.utils.bash()`执行Shell命令时，会返回当前命令的执行时间，可用做代码性能评判依据。

创建`run()`函数的代码如下，`job`为PyGrading创建的任务实例，`testcase`为字典类型，包含单个测试用例信息：

```python
def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    # 读取当前任务的配置信息
    configuration = job.get_config()
    
    # 创建和执行评测用Shell命令
    cmd = ["cat", testcase.input_src, "|", "python3 " + configuration["submit_path"]]
    status, output, time = gg.utils.bash(" ".join(cmd))

    # 初始化返回的字典对象
    result = {"name": testcase.name, "time": time}
    
    # 读取评测用例答案
    answer = gg.utils.readfile(testcase.output_src)

    # 将执行结果写回返回对象
    result["output"] = output
    result["answer"] = answer

    # 比较评测答案和实际输出将评测结果写回返回对象
    if gg.utils.compare_str(output, answer):
        result["verdict"] = "Accept"
        result["score"] = testcase.score
    else:
        result["verdict"] = "Wrong Answer"
        result["score"] = 0

    return result
```

#### 5. 创建评测结果处理函数

之后创建评测结果处理函数`postwork()`，并使用`pygrading.html`中的相关工具创建带有HTML标签的字符串。

创建`postwork()`函数的代码如下，`job`为PyGrading创建的任务实例：

```python
def postwork(job: gg.Job):
    # 设定结果verdict
    job.verdict(str(font(color="green").set_text("Accept")))

    # 设定结果score
    job.score(job.get_total_score())

    # 设定结果rank
    job.rank({"rank": str(job.get_total_time())})

    # 创建HTML标签
    detail = table(
        tr(
            th(),
            th().set_text("Verdict"),
            th().set_text("Output"),
            th().set_text("Answer")
        ), border="0"
    )
    for i in job.get_summary():
        if i["verdict"] == "Runtime Error":
            ver = font(color="red").set_text("Runtime Error")
            job.verdict(str(ver))
        elif i["verdict"] == "Wrong Answer":
            ver = font(color="red").set_text("Wrong Answer")
            job.verdict(str(ver))

        row = tr(
            td(align="center").set_text(str2html(i["name"])),
            td(align="center").set_text(str2html(i["verdict"])),
            td(align="center").set_text(str2html(i["output"])),
            td(align="center").set_text(str2html(i["answer"]))
        )
        detail << row

    # 将HTML标签转换为字符串，设定为结果detail
    job.detail(str(detail))
```

#### 6. 启动任务

完成三个阶段的函数编写后，将三个函数作为参数传入`gg.job()`函数，生成一个任务实例：

```python
# 创建任务实例
new_job = gg.job(prework=prework, run=run, postwork=postwork)

# 任务启动
new_job.start()

# 打印结果
new_job.print()
```

程序执行后输出结果如下：

```json
{"verdict": "<font color='red'>Wrong Answer</font>", "score": "80", "rank": {"rank": "238"}, "HTML": "enable", "detail": "<table border='1'><tr><th></th><th>Verdict</th><th>Output</th><th>Answer</th></tr><tr><td align='center'>TestCase1<br></td><td align='center'>Accept<br></td><td align='center'>True<br></td><td align='center'>True<br></td></tr><tr><td align='center'>TestCase2<br></td><td align='center'>Accept<br></td><td align='center'>False<br></td><td align='center'>False<br></td></tr><tr><td align='center'>TestCase3<br></td><td align='center'>Accept<br></td><td align='center'>False<br></td><td align='center'>False<br></td></tr><tr><td align='center'>TestCase4<br></td><td align='center'>Accept<br></td><td align='center'>True<br></td><td align='center'>True<br></td></tr><tr><td align='center'>TestCase5<br></td><td align='center'>Wrong Answer<br></td><td align='center'>True<br></td><td align='center'>False<br></td></tr></table>"}
```

在CG平台中显示效果如下：

<font color='red'>Wrong Answer</font>

<table border='0'>
    <tr>
        <th></th>
        <th>Verdict</th>
        <th>Output</th>
        <th>Answer</th>
    </tr>
    <tr>
        <td align='center'>TestCase1<br></td>
        <td align='center'>Accept<br></td>
        <td align='center'>True<br></td>
        <td align='center'>True<br></td>
    </tr>
    <tr>
        <td align='center'>TestCase2<br></td>
        <td align='center'>Accept<br></td>
        <td align='center'>False<br></td>
        <td align='center'>False<br></td>
    </tr>
    <tr>
        <td align='center'>TestCase3<br></td>
        <td align='center'>Accept<br></td>
        <td align='center'>False<br></td>
        <td align='center'>False<br></td>
    </tr>
    <tr>
        <td align='center'>TestCase4<br></td>
        <td align='center'>Accept<br></td>
        <td align='center'>True<br></td>
        <td align='center'>True<br></td>
    </tr>
    <tr>
        <td align='center'>TestCase5<br></td>
        <td align='center'>Wrong Answer<br></td>
        <td align='center'>True<br></td>
        <td align='center'>False<br></td>
    </tr>
</table>

一个简单的通用评测内核开发完成！

<h2 id="api" align="center">PyGrading API</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

在本节中，将会列出当前版本(v0.2.8)全部的接口与方法，详细使用方法请参考<a href="#tutorials">Tutorials</a>部分。

### pygrading.general_test

该包推荐导入方式：

```python
import pygrading.general_test as gg
```

包含有以下方法和类：

#### 1. gg.load_config(source: str)  

> 读取含有配置信息的JSON文件，返回字典类型。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

<b>Arguments:</b>
<table>
    <tr>
        <th>Arguments</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>source</td>
        <td>String</td>
        <td>Required</td>
        <td>配置文件的文件路径</td>
    </tr>
</table>

<b>Returns:</b>
<table>
    <tr>
        <th>Type</th>
        <th>Description</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>Dict</td>
        <td>以字典形式返回配置信息</td>
        <td>{'testcase_num': '3','testcase_dir': 'example/testdata','submit_path': 'example/submit/*'}</td>
    </tr>
</table>
</details>

#### 2. gg.create_std_testcase(testcase_dir: str, testcase_num: int) 
 
> 以推荐的方式创建TestCases对象实例。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

以推荐的方式构建评测用例目录，即可使用本方法直接创建一个TestCases对象实例。

推荐的目录构建方式如下：

```
testdata
├── input
│   ├── input1.txt
│   ├── input2.txt
│   └── input3.txt
└── output
    ├── output1.txt
    ├── output2.txt
    └── output3.txt
```

testdata目录为评测用例所在的根目录，评测用例的输入和输出分别放在input和output两个子目录中。

所有的评测用例输入按照input1.txt、input2.txt、input3.txt依次命名，所有的评测用例输出按照output1.txt、output2.txt、output3.txt依次命名。

<b>Arguments:</b>
<table>
    <tr>
        <th>Arguments</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>testcase_dir</td>
        <td>String</td>
        <td>Required</td>
        <td>评测用例目录路径</td>
    </tr>
    <tr>
        <td>testcase_num</td>
        <td>Integer</td>
        <td>Required</td>
        <td>评测用例的数目</td>
    </tr>
</table>

<b>Returns:</b>
<table>
    <tr>
        <th>Type</th>
        <th>Description</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>TestCases</td>
        <td>PyGrading创建的评测用例实例类型</td>
        <td>-</td>
    </tr>
</table>
</details>

#### 3. gg.create_testcase(total_score: int = 100)  

> 创建一个空的TestCases实例。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

在无法使用推荐的方式构建评测用例的情况下，可以创建一个空的TestCases实例并手动添加评测用例。添加方法请参考`gg.TestCases`类的介绍。

<b>Arguments:</b>
<table>
    <tr>
        <th>Arguments</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>total_score</td>
        <td>Integer</td>
        <td>100</td>
        <td>评测用例总分</td>
    </tr>
</table>

<b>Returns:</b>
<table>
    <tr>
        <th>Type</th>
        <th>Description</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>TestCases</td>
        <td>PyGrading创建的评测用例实例类型</td>
        <td></td>
    </tr>
</table>
</details>

#### 4. gg.TestCases 类

> 该类用于存储和传递关于评测用例的全部信息，通过迭代的方式将每个测试用例传入到评测用例执行函数中。  
> 请使用`gg.create_std_testcase()`或`gg.create_testcase()`获取TestCases实例。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

`gg.TestCases`类包含有1个子类`SingleTestCase`，该子类的实例用于存储单个评测用例的信息，且会作为一个必要参数传入评测用例执行函数中。

子类`SingleTestCase`包含的属性如下：

<table>
    <tr>
        <th>Attributes</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>Required</td>
        <td>评测用例的名称</td>
    </tr>
    <tr>
        <td>score</td>
        <td>Integer</td>
        <td>Required</td>
        <td>评测用例的满分分值</td>
    </tr>
    <tr>
        <td>input_src</td>
        <td>Object</td>
        <td>Required</td>
        <td>评测用例的输入，可以为任何类型</td>
    </tr>
    <tr>
        <td>output_src</td>
        <td>Object</td>
        <td>Required</td>
        <td>评测用例的输出，可以为任何类型</td>
    </tr>
    <tr>
        <td>extension</td>
        <td>Object</td>
        <td>None</td>
        <td>评测用例的额外信息，可以为任何类型</td>
    </tr>
</table>

`gg.TestCases`类包含有如下属性：

<table>
    <tr>
        <th>Attributes</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>__count</td>
        <td>Integer</td>
        <td>0</td>
        <td>保存该实例中评测用例的数量</td>
    </tr>
    <tr>
        <td>__cases</td>
        <td>List</td>
        <td>[ ]</td>
        <td>以列表的形式保存实例中所有的评测用例</td>
    </tr>
    <tr>
        <td>__total_score</td>
        <td>Integer</td>
        <td>100</td>
        <td>保存评测用例总分，默认为百分制</td>
    </tr>
</table>


`gg.TestCases`类包含有如下方法：

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>TestCases.append(self, name: str, score: float, input_src: object, output_src: object, extension: object = None)</td>
        <td>None</td>
        <td>向一个TestCases实例添加评测用例，传入参数的属性和<code>__SingleTestCase</code>中对应</td>
    </tr>
    <tr>
        <td>TestCases.get_count(self)</td>
        <td>Integer</td>
        <td>获取评测用例数目值</td>
    </tr>
    <tr>
        <td>TestCases.get_total_score(self)</td>
        <td>Integer</td>
        <td>获取评测用例总分</td>
    </tr>
    <tr>
        <td>TestCases.get_testcases(self)</td>
        <td>List[__SingleTestCase]</td>
        <td>获取评测用例列表</td>
    </tr>
    <tr>
        <td>TestCases.set_total_score(self, total_score: int)</td>
        <td>None</td>
        <td>设定评测用例总分</td>
    </tr>
    <tr>
        <td>TestCases.isempty(self)</td>
        <td>Boolean</td>
        <td>判断评测用例是否为空</td>
    </tr>
</table>
</details>

#### 5. gg.job(prework=None, run=None, postwork=None)

> 该方法用于创建评测任务实例，传入评测任务预处理、评测用例执行、评测结果处理的相关函数，返回一个Job实例。   

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

<b>Arguments:</b>
<table>
    <tr>
        <th>Arguments</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>prework</td>
        <td>Function</td>
        <td>None</td>
        <td>评测任务预处理函数</td>
    </tr>
    <tr>
        <td>run</td>
        <td>Function</td>
        <td>None</td>
        <td>评测用例执行函数</td>
    </tr>
    <tr>
        <td>postwork</td>
        <td>Function</td>
        <td>None</td>
        <td>评测结果处理函数</td>
    </tr>
</table>

<b>Returns:</b>
<table>
    <tr>
        <th>Type</th>
        <th>Description</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>Job</td>
        <td>PyGrading创建的评测任务实例类型</td>
        <td></td>
    </tr>
</table>
</details>

#### 6. gg.Job 类

> 该类用于创建评测任务实例，提供任务初始化、任务执行、输出结果的功能。   

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

`gg.Job`类包含有如下属性：

<table>
    <tr>
        <th>Attributes</th>
        <th>Type</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>__prework</td>
        <td>Function</td>
        <td>None</td>
        <td>评测任务预处理函数</td>
    </tr>
    <tr>
        <td>__run</td>
        <td>Function</td>
        <td>None</td>
        <td>评测用例执行函数</td>
    </tr>
    <tr>
        <td>__postwork</td>
        <td>Function</td>
        <td>None</td>
        <td>评测结果处理函数</td>
    </tr>
    <tr>
        <td>__testcases</td>
        <td>TestCases</td>
        <td>TestCases()</td>
        <td>评测用例</td>
    </tr>
    <tr>
        <td>__config</td>
        <td>Dict</td>
        <td>None</td>
        <td>配置信息</td>
    </tr>
    <tr>
        <td>__terminate</td>
        <td>Boolean</td>
        <td>False</td>
        <td>程序结束标记</td>
    </tr>
    <tr>
        <td>__result</td>
        <td>Dict</td>
        <td>{<br>
            "verdict": "Unknown Error",<br>
            "score": "0",<br>
            "rank": {"rank": "-1"},<br>
            "HTML": "enable"<br>
        }</td>
        <td>评测任务执行结果的内部存储字典</td>
    </tr>
    <tr>
        <td>__summary</td>
        <td>List</td>
        <td>[ ]</td>
        <td>每个测试用例的执行结果汇总列表</td>
    </tr>
</table>

`gg.Job`类包含有如下方法：

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Job.verdict(self, src: str)</td>
        <td>None</td>
        <td>修改返回结果中的verdict字段</td>
    </tr>
    <tr>
        <td>Job.score(self, src: int)</td>
        <td>None</td>
        <td>修改返回结果中的score字段</td>
    </tr>
    <tr>
        <td>Job.rank(self, src: Dict)</td>
        <td>None</td>
        <td>修改返回结果中的rank字段</td>
    </tr>
    <tr>
        <td>Job.images(self, src: List[str])</td>
        <td>None</td>
        <td>修改返回结果中的images字段</td>
    </tr>
    <tr>
        <td>Job.comment(self, src: str)</td>
        <td>None</td>
        <td>修改返回结果中的comment字段</td>
    </tr>
    <tr>
        <td>Job.detail(self, src: str)</td>
        <td>None</td>
        <td>修改返回结果中的detail字段</td>
    </tr>
    <tr>
        <td>Job.detail(self, src: str)</td>
        <td>None</td>
        <td>修改返回结果中的detail字段</td>
    </tr>
    <tr>
        <td>Job.HTML(self, src: str)</td>
        <td>None</td>
        <td>修改返回结果中的HTML字段</td>
    </tr>
    <tr>
        <td>Job.custom(self, key: str, value: str)</td>
        <td>None</td>
        <td>在返回结果中创建自定义字段并赋值</td>
    </tr>
    <tr>
        <td>Job.get_summary(self)</td>
        <td>List</td>
        <td>获取评测用例汇总结果列表</td>
    </tr>
    <tr>
        <td>Job.get_config(self)</td>
        <td>Dict</td>
        <td>获取评测任务配置信息</td>
    </tr>
    <tr>
        <td>Job.get_total_score(self)</td>
        <td>Integer</td>
        <td>获取评测任务总分</td>
    </tr>
    <tr>
        <td>Job.get_total_time(self)</td>
        <td>Integer</td>
        <td>获取评测任务执行总时间</td>
    </tr>
    <tr>
        <td>Job.set_testcases(self, testcases: TestCases)</td>
        <td>None</td>
        <td>设定评测任务的评测用例</td>
    </tr>
    <tr>
        <td>Job.set_config(self, config: Dict)</td>
        <td>None</td>
        <td>设定评测用例的配置信息</td>
    </tr>
    <tr>
        <td>Job.terminate(self)</td>
        <td>None</td>
        <td>将终止标记置于True，执行完当前函数后评测终止</td>
    </tr>
    <tr>
        <td>Job.start(self)</td>
        <td>List</td>
        <td>开始任务，返回评测用例汇总结果列表</td>
    </tr>
    <tr>
        <td>Job.print(self)</td>
        <td>None</td>
        <td>将评测结果转化为JSON格式并打印到标准输出</td>
    </tr>
</table>
</details>

#### 7. gg.__version__ 和 gg.version()

> 用于查看PyGrading的版本信息

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

```python
import pygrading.general_test as gg

# 获取版本信息字符串
print(gg.__version__)

# 直接打印版本信息
gg.version()
```

</details>

### pygrading.general_test.utils

该包封装了在编写评测内核的过程中可能会使用到的基本操作，可分为如下几类：

#### 1. 执行操作  

> 执行Shell命令的方法，返回值包括执行状态、执行后输出的内容、执行时间。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>gg.utils.bash(cmd: str)</td>
        <td>Tuple</td>
        <td>执行Shell命令，返回值包括执行状态(status)、执行后输出的内容(output)、执行时间(time)</td>
    </tr>
</table>
</details>

#### 2. 文件操作  

> 有关文件读写增删的相关操作。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>gg.utils.copyfile(src: str, dst: str)</td>
        <td>None</td>
        <td>将src路径所指示的文件复制到dst所指示的位置</td>
    </tr>
    <tr>
        <td>gg.utils.copytree(src: str, dst: str)</td>
        <td>None</td>
        <td>将src路径所指示的目录递归地复制到dst所指示的位置</td>
    </tr>
    <tr>
        <td>gg.utils.move(src: str, dst: str)</td>
        <td>None</td>
        <td>将src路径所指示的文件移动到dst所指示的位置</td>
    </tr>
    <tr>
        <td>gg.utils.rmtree(src: str)</td>
        <td>None</td>
        <td>递归地删除src路径所指示的目录</td>
    </tr>
    <tr>
        <td>gg.utils.rmfile(src: str)</td>
        <td>None</td>
        <td>删除src路径所指示的文件</td>
    </tr>
    <tr>
        <td>gg.utils.rename(old: str, new: str)</td>
        <td>None</td>
        <td>将old路径所指示的文件重命名为new</td>
    </tr>
    <tr>
        <td>gg.utils.readfile(src: str)</td>
        <td>String</td>
        <td>读取路径为src的文件，并以字符串的形式返回文件内容，文件中的换行以'\n'表示</td>
    </tr>
    <tr>
        <td>gg.utils.writefile(src: str, lines: str, option: str = "w")</td>
        <td>None</td>
        <td>将lines中的内容写入src，通过option选项选择写入模式，默认为“w”</td>
    </tr>
    <tr>
        <td>gg.utils.readfile_list(src: str)</td>
        <td>List[str]</td>
        <td>读取路径为src的文件，并以列表的形式返回文件内容，文件中每行为列表中的一个元素</td>
    </tr>
    <tr>
        <td>gg.utils.writefile_list(src: str, lines: List, option: str = "w")</td>
        <td>None</td>
        <td>将lines中的内容写入src，通过option选项选择写入模式，默认为"w"</td>
    </tr>
    <tr>
        <td>gg.utils.str2list(src: str)</td>
        <td>List[str]</td>
        <td>将普通字符串转化为列表，根据"\n"进行分隔，并会自动去掉字符串末尾的空行</td>
    </tr>
</table>
</details>

#### 3. 比较操作  

> 关于评测用例执行结果比较打分的相关操作。

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>gg.utils.compare_str(str1: str, str2: str)</td>
        <td>Boolean</td>
        <td>返回输入的两个字符串是否相同，并自动忽略字符串尾的换行符</td>
    </tr>
    <tr>
        <td>gg.utils.compare_list(list1: List, list2: List)</td>
        <td>Boolean</td>
        <td>返回输入的两个列表是否相同，并自动忽略列表最后的换行符和空白字符串</td>
    </tr>
    <tr>
        <td>gg.utils.edit_distance(obj1, obj2)</td>
        <td>Integer</td>
        <td>返回两个可迭代类型的参数是否相同，在比较字符串和列表时不会自动处理空行，建议在进行字符串比较时，使用<code>str2list()函数</code>预处理传入的数据</td>
    </tr>compiler
</table>
</details>

### pygrading.general_test.compiler

该包封装了部分编程语言的编译方法，目前支持如下编程语言：

> c, cpp

包含的方法如下：

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>gg.compiler.compile_c(source: str, target: str, compiler_type: str = "gcc", flag: str = "-O2 -Wall -std=c99", option: str = "")</td>
        <td>Tuple</td>
        <td>针对c语言编译的方法，通过source传入源文件路径，target指定编译后文件路径，compiler_type选择编译器类型，通过flag设定版本标签和一些前置选项，通过option添加编译选项。返回执行状态和执行过程中的输出</td>
    </tr>
    <tr>
        <td>gg.compiler.compile_cpp(source: str, target: str, compiler_type: str = "g++", flag: str = "-O2 -Wall -std=c++11", option: str = "")</td>
        <td>Tuple</td>
        <td>针对c++语言编译的方法，通过source传入源文件路径，target指定编译后文件路径，compiler_type选择编译器类型，通过flag设定版本标签和一些前置选项，通过option添加编译选项。返回执行状态和执行过程中的输出</td>
    </tr>
</table>
</details>

### pygrading.html

该包提供了创建HTML标签文本的相关功能，支持成对标签和不成对标签的创建，支持标签之间的嵌套创建，推荐导入方式如下：

```python
from pygrading.html import *
```

导入包之后目前可以通过如下方式创建并打印HTML标签实例，详细的使用方法请参考[评测结果的展示优化](#评测结果的展示优化)：

```python
from pygrading.html import *

a = table(
    tr(
        td(font(color="red").set_text("Hello World"))
    )
)

print(a)
```

生成的HTML文本如下：

```html
<table><tr><td><font color='red'>Hello World</font></td></tr></table>
```

<details>
<summary>详细信息(点击以展开...)</summary>
<br>

目前已经支持的内置标签有如下几种：

1. 成组标签：
```html
<a> <body> <div> <font> <form> <h1> <h2> <h3> <h4> <h5> <h6>
<head> <html> <p> <table> <th> <title> <tr> <td>
```

2. 不成组标签

```html
<br> <img> <input> 
```

> 由于`input()`为Python内置方法，故创建`<input>`标签的方法为`input_tag()`。

这些标签均可通过`tag()`的方式创建，并可以通过`print(tag())`的方式打印，或通过`str(tag())`的方式转化为字符串。

除了内置标签外，PyGrading还支持创建自定义标签：

<table>
    <tr>
        <td>custom_single_tag(tag_name)</td>
        <td>传入自定义的标签名称，创建一个不成组的标签</td>
    </tr>
    <tr>
        <td>custom(tag_name)</td>
        <td>传入自定义的标签名称，创建一个成组的标签</td>
    </tr>
</table>

成组标签继承于`pygrading.html.Tag`类，包含有如下方法：

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Tag.append(self, obj)</td>
        <td>None</td>
        <td>向当前标签实例中添加一个子标签</td>
    </tr>
    <tr>
        <td>Tag.pop(self, index=-1)</td>
        <td>None</td>
        <td>从当前标签实例中移除一个子标签，默认移除最后的一个</td>
    </tr>
    <tr>
        <td>Tag.insert(self, index, obj)</td>
        <td>None</td>
        <td>向当前标签实例中插入一个子标签</td>
    </tr>
    <tr>
        <td>Tag.extend(self, seq)</td>
        <td>None</td>
        <td>向当前标签实例中追加一个子标签列表</td>
    </tr>
    <tr>
        <td>Tag.set_text(self, src: str)</td>
        <td>None</td>
        <td>设定当前标签中的文本</td>
    </tr>
    <tr>
        <td>Tag.print(self)</td>
        <td>None</td>
        <td>将标签实例转化为HTML文本并打印到标准输出</td>
    </tr>
    <tr>
        <td>Tag.__str__(self)</td>
        <td>String</td>
        <td>重载方法，将标签实例转化为HTML文本字符串</td>
    </tr>
    <tr>
        <td>Tag.__lshift__(self, other)</td>
        <td>Tag</td>
        <td>重载操作符<code><<</code>，用法同<code>append</code>，向当前标签实例中添加一个子标签</td>
    </tr>
</table>

不成组标签继承于`pygrading.html.SingleTag`类，包含有如下方法：

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>SingleTag.print(self)</td>
        <td>None</td>
        <td>将标签实例转化为HTML文本并打印到标准输出</td>
    </tr>
    <tr>
        <td>SingleTag.__str__(self)</td>
        <td>String</td>
        <td>重载方法，将标签实例转化为HTML文本字符串</td>
    </tr>
</table>

此外，该包还提供了一个方法用于将普通字符串中的换行符转换为HTML的换行符：

<table>
    <tr>
        <th>Function</th>
        <th>Return</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>str2html(src: str)</td>
        <td>String</td>
        <td>将src字符串中的"\n"替换为"<br>"并返回新的字符串</td>
    </tr>
</table>
</details>


<h2 id="tutorials" align="center">Tutorials</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

在本章中，将会通过例子，详细解析不同模块的用法。本章的所有例子均可在`example`目录下找到。

<details>
<summary>目录 (点击以展开...)</summary>
<br> 

> - [构建并读取配置文件](#构建并读取配置文件)
> - [构建并读取评测用例](#构建并读取评测用例)
> - [评测结果的收集反馈](#评测结果的收集反馈)
> - [评测结果的打印输出](#评测结果的打印输出)
> - [评测结果的展示优化](#评测结果的展示优化)

</details>

### 构建并读取配置文件

在第一个例子中，我们将要演示如何构建并读取你的配置文件。由于在通用评测内核的实际使用中，教师账号没有权限操作实验环境的管理，因此对于不同的题目需要使用测试数据编辑器功能进行配置，配置文件就成为了用一个评测内核支持多个题目的关键。

配置文件是一个JSON格式的文本文件，用于向评测内核传递当前题目所需的配置项。一般来说，配置文件中的配置项至少应当包含：评测用例的数目(testcase_num)、评测用例的挂载路径(testcase_dir)和学生提交文件的挂载路径(submit_path)。如下面例子所示：

```json
{
    "testcase_num": "5",
    "testcase_dir": "./example/GettingStart/testdata",
    "submit_path": "./example/GettingStart/submit/main.py"
}
```

当然，配置文件中的配置项可以根据实际情况自行添加，因为如何处理这些配置项也是由开发者决定的。

PyGrading提供了`load_config(source)`方法来读取配置文件，该方法传入配置文件的路径，返回一个由配置文件中的JSON串转换成的字典。我们推荐在评测任务预处理函数（prework）中完成配置文件的读取，并将配置信息传递给当前任务（job）的config属性，以便在其他函数中可以使用这些配置信息。

下面一段代码展示了如何读取并使用我们配置文件，由于还没配置评测用例，所以我们创建一个只包含prework和postwork的评测任务：

```python
import pygrading.general_test as gg

def prework(job: gg.Job):
    config = gg.load_config("./example/构建并读取配置文件/config.json")
    job.set_config(config)

def postwork(job: gg.Job):
    config = job.get_config()
    testcase_num = config["testcase_num"]
    testcase_dir = config["testcase_dir"]
    submit_path = config["submit_path"]

    print("testcase_num:", testcase_num)
    print("testcase_dir:", testcase_dir)
    print("submit_path:", submit_path)

myjob = gg.job(prework=prework, run=None, postwork=postwork)

myjob.start()
```

执行结果如下：

```
testcase_num: 5
testcase_dir: ./example/GettingStart/testdata
submit_path: ./example/GettingStart/submit/main.py
```

以上就是构建并读取配置文件的方法。

### 构建并读取评测用例

接下来，我们尝试构建几组评测用例。评测用例一般来说是一组包含输入和输出的文件，每一组评测用例都会作为参数传递给评测用例执行函数（run()）迭代执行并返回结果。

PyGrading推荐使用`gg.create_std_testcase()`方法进行评测用例实例的创建，该方法要求遵照标准形式配置评测用例目录，具体要求如下：

```
testdata
├── input
│   ├── input1.txt
│   ├── input2.txt
│   ├── input3.txt
│   ├── input4.txt
│   └── input5.txt
└── output
    ├── output1.txt
    ├── output2.txt
    ├── output3.txt
    ├── output4.txt
    └── output5.txt
```

`testdata`为评测用例目录的根目录，建议将这个路径写入配置文件。根目录下分别设有`input`和`output`目录，分别用于存放输入和输出文件。

输入和输出文件的命名从`input1.txt`和`output1.txt`开始并一一对应。

在以此方式创建的评测用例实例中，总分默认为100分，传递给评测用例执行函数（run()）的输入输出参数为每组`input`和`output`文件的路径，下面通过一段代码展示具体的使用方法：

```python
import pygrading.general_test as gg


def prework(job: gg.Job):
    config = gg.load_config("./example/构建并读取评测用例/config.json")
    testcases = gg.create_std_testcase(config["testcase_dir"], config["testcase_num"])

    job.set_testcases(testcases)


def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    print("######################")
    print("Name:", testcase.name)
    print("score:", testcase.score)
    print("input_src:", testcase.input_src)
    print("output_src:", testcase.output_src)
    print("extension:", testcase.extension)


myjob = gg.job(prework=prework, run=run, postwork=None)

myjob.start()
```

执行结果如下：

```
######################
Name: TestCase1
score: 50.0
input_src: ./example/构建并读取评测用例/testdata_std/input/input1.txt
output_src: ./example/构建并读取评测用例/testdata_std/output/output1.txt
extension: None
######################
Name: TestCase2
score: 50.0
input_src: ./example/构建并读取评测用例/testdata_std/input/input2.txt
output_src: ./example/构建并读取评测用例/testdata_std/output/output2.txt
extension: None
```

上面的例子展示了如何使用推荐的方式构建、读取并使用评测用例，接下来我们将展示如何使用`gg.testcase()`方法来自定义评测用例。

假设根据要求，不必从文件中读取评测用例，而是直接由程序创建。参见下面代码实例：

```python
import pygrading.general_test as gg


def prework(job: gg.Job):
    # 自定义评测用例总分
    testcases = gg.create_testcase(100)

    for i in range(1, 5):
        input_src = i
        output_src = pow(2, i)

        # 使用append()方法向testcases追加评测用例
        testcases.append("TestCase{}".format(i), 25, input_src, output_src)

    job.set_testcases(testcases)


def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    print("######################")
    print("Name:", testcase.name)
    print("score:", testcase.score)
    print("input_src:", testcase.input_src)
    print("output_src:", testcase.output_src)
    print("extension:", testcase.extension)


myjob = gg.job(prework=prework, run=run, postwork=None)

myjob.start()
```

执行结果如下：

```
######################
Name: TestCase1
score: 25.0
input_src: 1
output_src: 2
extension: None
######################
Name: TestCase2
score: 25.0
input_src: 2
output_src: 4
extension: None
######################
Name: TestCase3
score: 25.0
input_src: 3
output_src: 8
extension: None
######################
Name: TestCase4
score: 25.0
input_src: 4
output_src: 16
extension: None
```

以上就是构建并读取评测用例的方法。

### 评测结果的收集反馈

我们在评测任务预处理阶段完成了读取配置文件和评测用例的任务，接下来评测用例将会传递给评测用例执行函数执行并收集结果。

如果在评测过程中需要执行Shell命令，可以使用`gg.utils.bash()`方法，该方法接收一个Shell命令字符串，返回值依次为：执行状态、执行过程输出、执行时间。

对于获取到的执行结果，我们提供了字符串比较和编辑距离比较两种方式：

1. 字符串比较支持单个字符串和字符串列表两种形式，返回结果为两个字符串是否相同的布尔值；
2. 编辑距离比较在接收到两个字符串列表时会返回两个列表之间的编辑距离，常用与按行比较的情况，返回结果为两个列表之间的编辑距离数值。

推荐以字典的形式收集并返回每个评测用例的执行结果，这些结果会保存在评测任务实例`job`的`summary`变量中，可以使用`job.get_summary()`来获取。

下面以一个简单的例子演示如何获取并收集评测结果：

```python
import pygrading.general_test as gg


def prework(job: gg.Job):
    testcases = gg.create_testcase(100)

    for i in range(1, 5):
        input_src = i
        output_src = pow(2, i)
        testcases.append("TestCase{}".format(i), 25, input_src, output_src)

    job.set_testcases(testcases)


def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    # 使用Shell命令计算2^n
    cmd = ["echo", "$((", "2", "**", str(testcase.input_src), "))"]

    # 获取执行情况
    status, output, time = gg.utils.bash(" ".join(cmd))

    # 初始化返回结果的字典
    result = {"name": testcase.name, "time": time}

    # 获取评测用例给出的答案
    answer = testcase.output_src

    result["output"] = output
    result["answer"] = answer

    # 根据字符串比较结果返回单个测试用例的评判情况
    if gg.utils.compare_str(str(output), str(answer)):
        result["verdict"] = "Accept"
        result["score"] = testcase.score
    else:
        result["verdict"] = "Wrong Answer"
        result["score"] = 0

    return result


def postwork(job: gg.Job):
    # 打印收集到的每个评测用例的结果
    print(job.get_summary())


myjob = gg.job(prework=prework, run=run, postwork=postwork)

myjob.start()
```

根据上面的例子，结合特定的评测用例情况，应当可以编写出满足需求的评测用例执行函数。

> 在实际应用中，应当在各个阶段的函数中对可能发生的异常进行捕获，以保证评测程序顺利执行，让学生能查看到正确的反馈信息并预防可能的作弊行为。

### 评测结果的打印输出

在评测任务执行完毕后，我们在评测结果处理函数中对收集到的评测结果进行最后处理并生成CG平台支持的JSON串格式，关于所支持的格式详情请查看[通用评测题开发指南](http://com.educg.net:8888/admin/help/projJudge.jsp#dockerImage)。

在评测任务实例`Job`中，有如下几个内置的方法，用于设定待输出的JSON串字段：

<table>
    <tr>
        <th>Function</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>job.verdict()</td>
        <td>基本判定，一般为简要的评测结果描述或者简写，例如OJ系统的AC、PE、CE等</td>
    </tr>
    <tr>
        <td>job.rank()</td>
        <td>选择排行榜模式时，必须有该项，浮点数(正常值 ≥0)，该值决定了本次提交在排行榜上的位置，排行榜从小到大排序。如果提交的材料有误或者其它异常，将rank值置为负数，不参与排行!</td>
    </tr>
    <tr>
        <td>job.score()</td>
        <td>选择直接评测得分时，必须有该项，按照百分制给分，必须为大于等于0的整数，例如90</td>
    </tr>
    <tr>
        <td>job.images()</td>
        <td>可选，如果评测结果有图表，需要转换为base64或者SVG(启用HTML)格式</td>
    </tr>
    <tr>
        <td>job.comment()</td>
        <td>可选，评测结果的简要描述。</td>
    </tr>
    <tr>
        <td>job.detail()</td>
        <td>可选，评测结果的详细描述，可以包含协助查错的信息。布置作业的时候，可以选择是否显示这项信息。</td>
    </tr>
    <tr>
        <td>job.secret()</td>
        <td>可选，该信息只有教师评阅时才能看到。</td>
    </tr>
    <tr>
        <td>job.HTML()</td>
        <td>可选，如果置为enable，开发者可以使用HTML标签对verdict、comment、detail的输出内容进行渲染。</td>
    </tr>
    <tr>
        <td>job.custom()</td>
        <td>可选，自定义字段。</td>
    </tr>
</table>

设定好JSON字段之后可以使用`job.print()`打印JSON字段到标准输出。

下面通过一个简单的示例展示如何配置评测任务的输出结果：

```python
import pygrading.general_test as gg


def postwork(job: gg.Job):
    job.verdict("Accept")
    job.score(100)
    job.detail("Detail Message!")
    job.custom("custom_key", "custom_value")


myjob = gg.job(prework=None, run=None, postwork=postwork)

myjob.start()

myjob.print()
```

输出结果如下：

```
{"verdict": "Accept", "score": "100", "rank": {"rank": "-1"}, "HTML": "enable", "detail": "Detail Message!", "custom_key": "custom_value"}
```

实际应用中，请使用`job.get_summary()`获取评测结果列表，再根据评测结果决定要输出的内容。

### 评测结果的展示优化

为了更好地展示评测结果，CG平台支持在返回JSON结果中的`verdict`、`comment`、`detail`、`secret`字段中添加HTML标签，经过渲染后显示为最终展示结果。

PyGrading中提供了强大的HTML文档构建工具`pygrading.html`，详细的API请参考[pygrading.html API](#pygradinghtml)，接下来通过几个实例讲解各种场景的使用方法。

#### 1. 修改文本颜色

在`verdict`字段中我们通常希望展示如`Accept`、`Wrong Answer`这样的内容，为了让这些信息显示的更加直观，则需要给他们添加颜色。

下面创建一段HTML文本，对`Accept`显示为绿色，对`Wrong Answer`显示为红色：

```python
from pygrading.html import *

# 在括号中可以输入任意组键值对，他们将作为标签的属性显示在最终的HTML文本中
accept = font(color="green").set_text("Accept")
wrong_answer = font(color="red").set_text("Wrong Answer")

accept.print()
wrong_answer.print()
```

输出结果如下：

```html
<font color='green'>Accept</font>
<font color='red'>Wrong Answer</font>
```

显示效果如下：

![html01](./img/html01.png)

#### 2. 创建表格

在`comment`、`detail`、`secret`字段中，通常需要表格进行内容的展示，接下来通过一个实例说明如何创建表格。

假设我们需要创建一个表格来比较每个评测用例中，学生输出的内容和标准答案的区别，解决方案如下：

```python
from pygrading.html import *

# 可以看到字符串中含有换行符，推荐使用str2html()函数进行处理，将换行符转化为<br>
outputs = ["1", "1\n2", "1\n2\n3", "1\n2\n3\n4", "5\n4\n3\n2\n1"]
answers = ["1", "1\n2", "1\n2\n3", "1\n2\n3\n4", "1\n2\n3\n4\n5"]

# 标签之间可以相互嵌套，任意数量的子标签可以作为参数传递给父标签
result = table(
    tr(
        th().set_text("Output"),
        th().set_text("Answer")
    )
)

for out, ans in zip(outputs, answers):
    tmp = tr(
        td().set_text(str2html(out)),
        td().set_text(str2html(ans)),
    )
    # 可以使用“<<”操作符将一个标签作为子标签传递给另一个标签
    result << tmp

result.print()
```

生成HTML文本如下：

```html
<table><tr><th>Output</th><th>Answer</th></tr><tr><td>1<br></td><td>1<br></td></tr><tr><td>1<br>2<br></td><td>1<br>2<br></td></tr><tr><td>1<br>2<br>3<br></td><td>1<br>2<br>3<br></td></tr><tr><td>1<br>2<br>3<br>4<br></td><td>1<br>2<br>3<br>4<br></td></tr><tr><td>5<br>4<br>3<br>2<br>1<br></td><td>1<br>2<br>3<br>4<br>5<br></td></tr></table>
```

显示效果如下：

<table><tr><th>Output</th><th>Answer</th></tr><tr><td>1<br></td><td>1<br></td></tr><tr><td>1<br>2<br></td><td>1<br>2<br></td></tr><tr><td>1<br>2<br>3<br></td><td>1<br>2<br>3<br></td></tr><tr><td>1<br>2<br>3<br>4<br></td><td>1<br>2<br>3<br>4<br></td></tr><tr><td>5<br>4<br>3<br>2<br>1<br></td><td>1<br>2<br>3<br>4<br>5<br></td></tr></table>

#### 3. 创建表单

下面以创建一个用户名输入表单为例，展示如何创建不成对的HTML标签文本：

```python
from pygrading.html import *

# 由于input()为Python内置方法，故创建<input>标签的方法为`input_tag()`
result = form(
    font().set_text("First name"),
    br(),
    input_tag(type="text", name="firstname"),
    br(),
    font().set_text("Last name"),
    br(),
    input_tag(type="text", name="lastname"),
    br(),
    input_tag(type="submit", value="Submit")
)

result.print()
```

生成HTML文本如下：

```html
<form><font>First name</font><br><input type='text' name='firstname'><br><font>Last name</font><br><input type='text' name='lastname'><br><input type='submit' value='Submit'></form>
```

显示效果如下：

![html02](./img/html02.png)


<h2 id="faq" align="center">FAQ</h2>
<p align="right"><a href="#pygrading"><sup>▴ Back to top</sup></a></p>

**Q: 评测流程没有正确执行，但是为何程序执行结束没有任何报错信息？**  
**A:** 在整个评测流程中，PyGrading会自动抓取执行过程中的异常，且保证这些异常不会影响评测程序的完整执行。
因此有些问题不会显示地报错，而是保存在`job.__result`和`job.__summary`对象中。如果发现执行问题，
可以在评测任务的最后，使用`print(your_job_name.get_result())`和`print(your_job_name.get_summary())`
查看评测过程中的日志。

**Q: 我在prework函数里面创建了一些变量希望能在run函数中使用，应该如何操作？**  
**A:** 对于此类情况，可以通过向`gg.load_config()`返回的字典中添加一些您需要的信息组成键值对，再通过`gg.set_connfig()`函数将添加了新的键值对的函数赋值给当前job，即可再当前job中的所有函数中使用这些信息。
