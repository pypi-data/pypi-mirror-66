# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdfwork']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0']

entry_points = \
{'console_scripts': ['pdfwork = pdfwork.cli:cli_main']}

setup_kwargs = {
    'name': 'pdfwork',
    'version': '0.1.1',
    'description': '基于 PyPDF2 封装的命令行工具，处理 PDF 文件用',
    'long_description': "#######\nPDFWork\n#######\n\n基于 PyPDF2 封装的一个便于使用的 pdf 处理命令行工具。\n提供以下功能：\n\n-   书签（也叫目录）\n    -   导入、导入、抹除PDF文件中的书签\n-   合并 PDF\n-   分割 PDF\n\n安装方法\n========\n\n可以通过 pip 或 pipx 安装：\n\n.. code:: sh\n\n    # pip\n    pip install pdfwork\n    # pipx\n    pipx install pdfwork\n\n使用\n====\n\n对于 merge 和 split，其命令行参数呈现如下形式：\n\n.. code:: text\n\n    pdfwork {merge|split} -i '输入' -o '输出'\n\n输入和输出中如果要设定多个文件（片段）的话，需要按照 ``<路径>:<页码>|<path>:<page range>``\n的格式排列，例如：\n\n-   将文件 example.pdf 拆分成 p1, p2, p3 三个部分：\n\n.. code:: text\n\n    pdfwork split -i example.pdf -o 'p1.pdf:1,3,5,7,9|p2.pdf:0,2,4,6,8|p3.pdf:2,3,5,7,11'\n\n-   将文件 p1, p2, p3 合并成一个文件：\n\n.. code:: text\n\n    pdfwork merge -i 'p1.pdf:-|p2.pdf:-|p3.pdf:-' -o merged.pdf\n\n对于导入导出书签，其命令行参数呈现如下形式：\n\n.. code:: text\n\n    pdfwork outline {erase|import|export} [-i outlines.txt] [-o outlines.txt] <被操作的PDF文件路径>\n\n例如：\n\n-   将 PDF 中的书签导出到 outlines.txt 文件中\n\n.. code:: text\n\n    pdfwork outline export -o outlines.txt example.pdf\n\n-   将 outlines.txt 的书签导入到 PDF 文件中（原有的书签被抹除）\n\n.. code:: text\n\n    pdfwork outline import -i outlines.txt example.pdf\n\n-   抹除 PDF 文件中的书签\n\n.. code:: text\n\n    pdfwork outline erase example.pdf\n\n.. warning::\n\n    在 outline 子命令下的 PDF 文件路径参数必须在最后。\n",
    'author': 'zombie110year',
    'author_email': 'zombie110year@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zombie110year/pdfwork',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
