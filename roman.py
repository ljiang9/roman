#!/usr/bin/env python3
"""roman —— 罗马数字与阿拉伯数字互转 + 罗马数字四则运算。

纯标准库，纯本地。标准形式（1-3999），非法输入严格报错。
"""

import argparse
import json
import re
import sys

VERSION = "0.1.0"

# 标准罗马数字表（从大到小，含减法组合）
_TABLE = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]

# 严格校验正则：标准形式 1-3999
_STRICT_RE = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

_ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50,
                 "C": 100, "D": 500, "M": 1000}


def to_roman(n: int) -> str:
    """阿拉伯数字 -> 罗马数字（标准形式）。n 必须在 1-3999。"""
    if not isinstance(n, bool) and isinstance(n, int) and 1 <= n <= 3999:
        out = []
        for value, glyph in _TABLE:
            while n >= value:
                out.append(glyph)
                n -= value
        return "".join(out)
    raise ValueError(f"超出范围：只支持 1-3999（收到 {n}）")


def from_roman(s: str) -> int:
    """罗马数字 -> 阿拉伯数字。严格校验标准形式，非法则抛 ValueError。"""
    s = s.strip().upper()
    if not s:
        raise ValueError("输入为空")
    if not _STRICT_RE.match(s):
        raise ValueError(f"不是合法的标准罗马数字：{s}")
    total = 0
    prev = 0
    for ch in reversed(s):
        v = _ROMAN_VALUES[ch]
        if v < prev:
            total -= v
        else:
            total += v
            prev = v
    return total


def convert(token: str) -> str:
    """自动识别方向：纯数字 -> 罗马；罗马字母 -> 数字。"""
    token = token.strip()
    if re.fullmatch(r"\d+", token):
        return to_roman(int(token))
    if re.fullmatch(r"[ivxlcdmIVXLCDM]+", token):
        return str(from_roman(token))
    raise ValueError(f"无法识别的输入：{token}（请输入 1-3999 的数字或罗马数字）")


_ARITH_RE = re.compile(
    r"^\s*([ivxlcdmIVXLCDM]+)\s*([+\-*/])\s*([ivxlcdmIVXLCDM]+)\s*$"
)


def arith(expr: str) -> str:
    """罗马数字四则运算：解析 -> 计算 -> 渲染回罗马数字。"""
    m = _ARITH_RE.match(expr)
    if not m:
        raise ValueError(f"表达式格式错误，应为如 \"XIV + LX\" 的形式：{expr}")
    a_s, op, b_s = m.groups()
    a, b = from_roman(a_s), from_roman(b_s)
    if op == "+":
        r = a + b
    elif op == "-":
        r = a - b
    elif op == "*":
        r = a * b
    else:  # /
        if b == 0:
            raise ValueError("除数不能为零")
        r = a // b
    if r < 1:
        raise ValueError("结果小于 1：罗马数字没有零和负数")
    if r > 3999:
        raise ValueError("结果超过 3999：超出标准罗马数字范围")
    return to_roman(r)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="roman",
        description="罗马数字与阿拉伯数字互转（自动识别方向），支持罗马数字四则运算。",
    )
    p.add_argument("token", nargs="?",
                   help="数字（如 2026）或罗马数字（如 MMXXVI）")
    p.add_argument("--add", metavar="EXPR",
                   help="罗马数字算式，如 \"XIV + LX\"（支持 + - * /）")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    p.add_argument("--version", action="version", version=f"roman {VERSION}")
    return p


def emit(result: str, as_json: bool, **extra) -> int:
    if as_json:
        print(json.dumps({"result": result, **extra}, ensure_ascii=False))
    else:
        print(result)
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.add:
            res = arith(args.add)
            return emit(res, args.json, expression=args.add)
        if args.token is None:
            build_parser().print_usage(sys.stderr)
            print("error: 请提供一个数字或罗马数字，或使用 --add", file=sys.stderr)
            return 2
        res = convert(args.token)
        return emit(res, args.json, input=args.token)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
