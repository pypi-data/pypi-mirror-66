search-file - *A python module that searches files(or folders).*
һ�����������ļ����ļ��е�Pythonģ�顣

:�����ĺ��� FUNCTIONS:

:directories(path):

- һ��������, �г�path�µ�������Ŀ¼���ļ�����
- ��

.. code-block:: python

    >>> from search_file import directories
    >>> list(directories("C:"))
    ['C:\Users',  #��һ��Ŀ¼
    'C:\\\\Users\\\\Administrator', #�ڶ���Ŀ¼
    ...,
    'C:\Windows',
    'C:\\\\Windows\\\\System32',
    ...]

:search(filename,path,minsize=0,maxsize=None):

- һ��������,��path������һ���ļ����ļ��С�
- ��

.. code-block:: python

    >>> from search_file import search
    >>> list(search("cmd.exe","C:"))
    ['C:\\\\Windows\\\\System32\\\\cmd.exe',
    ...]


����:*�߷ֳ��� qq:3076711200 ����:3416445406@qq.com*