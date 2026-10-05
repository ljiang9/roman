# roman

罗马数字与阿拉伯数字互转小工具，附带罗马数字四则运算。纯标准库，纯本地，零依赖。

## 安装

```bash
cd roman
# 直接运行
python3 -m roman 2026
```

## 用法

自动识别方向：输入纯数字就转罗马数字，输入罗马字母就转回数字。

```bash
$ python3 -m roman 2026
MMXXVI

$ python3 -m roman MMXXVI
2026

$ python3 -m roman 944
CMXLIV

$ python3 -m roman IX
9
```

### 四则运算

```bash
$ python3 -m roman --add "XIV + LX"
LXXIV

$ python3 -m roman --add "C - X"
XC

$ python3 -m roman --add "VI * VII"
XLII
```

支持 `+ - * /`（除法为整除）。罗马数字没有零和负数，结果小于 1 会报错。

### JSON 输出

```bash
$ python3 -m roman 2026 --json
{"result": "MMXXVI", "input": "2026"}
```

## 设计取舍

- **标准形式 only**：只认 `IV` 不认 `IIII`，只支持 1–3999。非法输入（如 `IIII`、`VV`）严格报错，不静默给出错误答案。
- **方向自动识别**：纯 `\d+` 走数字→罗马；纯 `[IVXLCDM]` 走罗马→数字；其余报错。
- **无 vinculum**：4000 以上的上划线记法不支持，超出范围直接报错。

## 已知局限

- 标准罗马数字本身没有零、负数和小数，运算结果超出 1–3999 即报错（这是记数法的局限，不是 bug）。
- 校验正则只接受大写（输入会自动转大写，小写 `xiv` 也可用）。
- `/` 为整除，余数丢弃。

## 许可证

MIT，Copyright (c) 2026 ljiang9。
