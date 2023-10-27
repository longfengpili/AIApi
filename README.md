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

## 注册自定义的魔术命令
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

## python setup.py 介绍
`python setup.py` 是一个常用的命令，用于构建、安装和分发Python包。它支持一系列参数，每个参数都有特定的含义和用途。以下是常见的 `setup.py` 支持的参数及其含义：

1. **`sdist`**: 构建源代码分发包（Source Distribution）。这个命令会创建一个tarball（通常是 `.tar.gz` 格式），其中包含了源代码、`setup.py` 文件和其他必要文件。

   ```bash
   python setup.py sdist
   ```

2. **`bdist`**: 构建二进制分发包（Binary Distribution）。这个命令会创建一个二进制分发包，其中包含了已编译的Python模块。

   ```bash
   python setup.py bdist
   ```

3. **`bdist_wheel`**: 构建Wheel分发包，它是一种二进制分发格式，通常比sdist更高效。Wheel可以通过`pip`进行安装。

   ```bash
   python setup.py bdist_wheel
   ```

4. **`install`**: 安装包到系统中。这个命令会将包安装到Python的`site-packages`目录中。

   ```bash
   python setup.py install
   ```

5. **`develop`**: 安装包的开发版（development version）。这个命令会创建一个链接，指向包的源代码目录，从而允许您在源代码发生变化时立即看到变化，无需重新安装。

   ```bash
   python setup.py develop
   ```

6. **`test`**: 运行包的单元测试。这个命令会查找项目中的测试模块，并运行它们。

   ```bash
   python setup.py test
   ```

7. **`upload`**: 将包上传到Python包索引（PyPI）上，以便其他人可以通过`pip install`命令安装它。

   ```bash
   python setup.py upload
   ```

以上是常见的`setup.py`参数及其含义。确切的参数和用法可能会根据您的项目配置而有所不同，建议查阅相关文档或运行`python setup.py --help-commands`来获取关于特定版本的更详细信息。