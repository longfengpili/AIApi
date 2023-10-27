# AIApi

## install
1. 克隆代码
```bash
git clone git@github.com:longfengpili/AIApi.git
```
2. 进入代码目录
```bash
cd AIApi
```
3. 安装
```bash
python setup.py install
```
4. 配置jupyter lab
+ 方法1：在jupyter中使用`%load_ext xinghuo`加载
+ 方法2：把`mymagics.py`移动至目录/user/.ipython/profile_default/startup
5. 使用
+ 一句话沟通
```ipython
%chat_single 用pandas生成1个DataFrame
```
+ 连续沟通
```ipython
# 使用-v则显示连续对话内容
%%chat -v
用pandas生成1个DataFrame
```

## 定义
在您的代码中，您定义了两个函数来注册自定义的魔术命令。让我解释一下这两个函数的作用：

1. **`load_ipython_extension(ipython)` 函数：**
   这个函数是IPython的扩展加载机制的一部分。当您使用 `%load_ext your_module` 来加载您的自定义扩展时，IPython会尝试调用 `load_ipython_extension` 函数。在这个函数内部，您可以将您的自定义魔术命令注册到IPython中。

   例如，如果您的自定义魔术命令类叫做 `XhChater`，您可以在 `load_ipython_extension` 函数中将它注册为一个魔术命令。

   ```python
   def load_ipython_extension(ipython):
       ipython.register_magics(XhChater)
   ```

2. **`get_ipython().register_magics(XhChater)`：**
   这行代码是在全局命名空间中直接注册魔术命令。这种方式通常在交互式环境中使用，比如在Jupyter Notebook的代码单元格中。在这种情况下，您可以直接将您的 `XhChater` 类的实例注册为魔术命令。

   ```python
   get_ipython().register_magics(XhChater)
   ```

请注意，这两种注册魔术命令的方法在不同的环境下使用：

- `load_ipython_extension(ipython)` 函数通常在扩展模块中定义，用于在加载扩展时注册魔术命令。这种方式适用于将扩展打包成Python模块并安装到系统中，然后通过 `%load_ext your_module` 的方式在IPython中加载扩展。

- `get_ipython().register_magics(XhChater)` 这种方式通常在交互式环境中（例如Jupyter Notebook的代码单元格）使用，用于临时注册魔术命令，而不需要将它打包成模块并进行安装。这种方式适用于开发和调试阶段。

## load_ipython_extension如何将扩展打包并安装到系统
将自定义IPython扩展打包并安装到系统中，您可以使用Python的包管理工具`setuptools`。以下是一个通用的步骤，用于将您的IPython扩展打包并安装到系统中：

### 步骤 1: 创建项目目录结构

首先，在您的项目目录下创建一个包含以下文件的目录结构：

```
your_extension/
|-- your_extension/
|   |-- __init__.py
|   |-- your_magic_module.py
|-- setup.py
|-- README.md
```

- `your_extension/your_extension/` 目录中包含了您的扩展代码。`__init__.py` 文件用于将该目录视为Python包。
- `your_extension/your_extension/your_magic_module.py` 文件包含了您的自定义魔术命令类。
- `setup.py` 是用于打包和安装的`setuptools`配置文件。
- `README.md` 是您的项目文档，可以包含有关您的扩展的信息。

### 步骤 2: 编写魔术命令类

在 `your_extension/your_extension/your_magic_module.py` 文件中定义您的自定义魔术命令类。

```python
from IPython.core.magic import Magics, magics_class

@magics_class
class YourMagicCommand(Magics):
    # ... 定义您的魔术命令方法和逻辑 ...
    pass
```

### 步骤 3: 编写 `setup.py` 文件

在 `setup.py` 文件中定义您的项目信息和依赖关系。

```python
from setuptools import setup

setup(
    name='your_extension',
    version='0.1',
    packages=['your_extension'],
    install_requires=[
        'ipython',
        # 添加其他依赖项
    ],
)
```

### 步骤 4: 打包和安装

在项目根目录（包含`setup.py`的目录）中，运行以下命令来打包您的扩展：

```
python setup.py sdist
```

上述命令会在`dist/`目录下生成一个源分发包（`.tar.gz`文件）。然后，您可以使用`pip`命令安装这个分发包：

```
pip install dist/your_extension-0.1.tar.gz
```

这样，您的IPython扩展就被打包并安装到了系统中。安装完成后，您可以在IPython中使用 `%load_ext your_extension.your_magic_module` 来加载您的自定义魔术命令。

请确保在`setup.py`中正确指定了您的项目信息和依赖项，以便在安装时获得正确的配置。另外，根据需要修改`setup.py`以满足您的项目需求。