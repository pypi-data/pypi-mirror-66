import re
from .symbol2tex import sym2tex
from pylatex import NoEscape


# class MarkDown(La):
#     def __init__(self):
#         self.num = 0
#
#     def sym2tex(self, symbol, name=None):
#         self.num += 1
#         if name is None:
#             name = self.num
#         return sym2tex(symbol, False, f"Eq:{name}")
#
#     def ref(self, name=None):
#         if name is None:
#             name = self.num
#         return f"\\ref{{Eq:{name}}}"


def md2tex(path):
    """"""

    string = open(path, 'r', encoding='UTF-8').read()
    string = transform_formula(string)
    string = transform_struct(string)

    return NoEscape(string)


def transform_formula(string):
    """

    :param string: 需要转化的文本
    :return: 转换后的文本
    """
    names = [
        re.compile(r"\*\*(\S+)\*\*", re.IGNORECASE),
        re.compile(r"\*(\S+)\*"),
        re.compile(r"\$\$(\S+)\$\$"),
    ]
    codes = [
        lambda m: r"\textbf{"+m.group(1)+"}",
        lambda m: r"\emph{"+m.group(1)+"}",
        lambda m: sym2tex(m.group(1), False),
    ]
    for i, name in enumerate(names):
        code = codes[i]
        string = name.sub(code, string)
    return string


def transform_struct(string):
    """

    :param string: 需要转化的文本
    :return: 转换后的文本
    """
    names = [
        re.compile(r"### (\S+)\n"),
        re.compile(r"## (\S+)\n"),
        re.compile(r"# (\S+)\n"),
    ]
    codes = [
        lambda m: r"\subsubsection{"+m.group(1)+"}\n",
        lambda m: r"\subsection{"+m.group(1)+"}\n",
        lambda m: r"\section{"+m.group(1)+"}\n",
    ]
    for i, name in enumerate(names):
        code = codes[i]
        if type(name) is str:
            name = re.compile(f"{name}\b", re.IGNORECASE)
        string = name.sub(code, string)
    return string


def _beifen(string, *, replace=True, core=None):
    """

    :param replace:
    :param core:
    :param string:
    :return:
    """
    names = [
        re.compile(r"\*\*(\S+)\*\*", re.IGNORECASE),
        re.compile(r"\*(\S+)\*", re.IGNORECASE),
    ]
    codes = [
        lambda m: r"\textbf{"+m.group(1)+"}",
        lambda m: r"\emph{"+m.group(1)+"}",
    ]
    if replace:
        if core is None:
            raise ValueError("core cannot be None")
        with core.local_define(names, codes) as local_core:
            local_core.append(string, mode="re")
    else:
        for i, name in enumerate(names):
            code = codes[i]
            if type(name) is str:
                name = re.compile(f"{name}\b", re.IGNORECASE)
            string = name.sub(code, string)
        return string
