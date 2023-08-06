import search_file,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""search-file - A python module that searches files(or folders).
一个用于搜索文件或文件夹的Python模块。"""

try:
    with open("README.rst") as f:
        long_desc=f.read()
except OSError:
    long_desc=None

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
