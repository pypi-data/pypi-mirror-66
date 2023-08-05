search-file - *A python module that searches files(or folders).*
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