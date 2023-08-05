import search_file,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""search-file - *A python module that searches files(or folders).*
一个用于搜索文件或文件夹的Python模块。"""

long_desc=r"""search-file - *A python module that searches files(or folders).*
一个用于搜索文件或文件夹的Python模块。

:包含的函数 FUNCTIONS:

:directories(path):

- 一个生成器, 列出path下的所有子目录和文件名。
- 如

.. code-block:: python

    >>> from search_file import directories
    >>> list(directories("C:"))
    ['C:\Users',  #第一层目录
    'C:\\\\Users\\\\Administrator', #第二层目录
    ...,
    'C:\Windows',
    'C:\\\\Windows\\\\System32',
    ...]

:search(filename,path,minsize=0,maxsize=None):

- 一个生成器,在path中搜索一个文件或文件夹。
- 如

.. code-block:: python

    >>> from search_file import search
    >>> list(search("cmd.exe","C:"))
    ['C:\\\\Windows\\\\System32\\\\cmd.exe',
    ...]


作者:*七分诚意 qq:3076711200 邮箱:3416445406@qq.com*
"""
setup(
  name='search-file',
  version=search_file.__version__,
  description=desc,
  long_description=long_desc,
  author=search_file.__author__,
  author_email=search_file.__email__,
  py_modules=['search_file'], #这里是代码所在的文件名称
  keywords=["path","search","file"],
  classifiers=[
      'Programming Language :: Python',
      "Topic :: System :: Filesystems"]
)
