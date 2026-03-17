---
title: string
tags:
  - 语法
related:
  - substr
date: 2026-01-21
---

### 🎯 核心功能 (Purpose)
> c语言：
> 定义：一组字符
> 需要用数组存→ 字符数组（必须用 /0 作为结束符结尾）
> 新的初始化方式。
![[Screenshot_2026-01-21-22-28-46-88_99c04817c0de5652397fc8b56c3b3817.jpg]]

c++：
![[Image_1769008791593_975.jpg]]

拼接：
![[Image_1769009005365_599.jpg]]

输入解决空格问题，
getline(cin,str) ,左边是流，右边是字符串，这样就可以输入空格了。

![[Screenshot_2026-03-01-23-06-33-14_769977972775e0c6b41aa3dfaf766445.jpg]]


![[Screenshot_2026-03-01-23-10-08-39_769977972775e0c6b41aa3dfaf766445.jpg]]


![[Screenshot_2026-03-01-23-13-49-36_769977972775e0c6b41aa3dfaf766445.jpg]]

![[Screenshot_2026-03-01-23-16-08-31_769977972775e0c6b41aa3dfaf766445.jpg]]


strlen计数不包括/0
strcmp (a,b) a大于b,返回1，a小于b返回负一，相等则返回0。
strcpy（a,b)，b的内容完完全全把a变成b的内容，即使a比b长。
strcat (a,b)把b接到a后面
使用string 数据类型需要头文件 string
c++ spring类型大小判断 直接if()判断

substr 函数有两种常用形式：

· substr(pos)：从位置 pos 开始，截取到字符串末尾。
· substr(pos, count)：从位置 pos 开始，截取 count 个字符。

判断两字符串接龙重合长度（读第一个就返回版）：
```cpp
// 鉴定专家：看看单词 a 的尾巴，和单词 b 的头，能不能接上？
// 如果能，返回【最短】的重合长度；如果不能，返回 0。
int get_overlap(string a, string b) {
    int min_len = min(a.length(), b.length());
    // 重合部分必须小于两个单词的自身长度（题目规定不能存在包含关系）
    for (int k = 1; k < min_len; k++) { 
        // a.substr(起始位置) 截取 a 的尾巴
        // b.substr(0, k) 截取 b 的头
        if (a.substr(a.length() - k) == b.substr(0, k)) {
            return k; // 从小到大找，找到的第一个就是最短的！直接返回！
        }
    }
    return 0; // 找不到重合部分，接不上
}

```



字符串数据类型的变量名.replace(下标-作为起始位置, 长度，替换的内容，后面同前)
![[IMG_20260122_202721.jpg]]
字符串数据类型的变量名.erase(字符串下标-作为起始位置，长度)

字符数组 转换为 string
![[Screenshot_2026-01-22-21-49-23-60_149003a2d400f6adb210d7e357a3a646.jpg]]

### ✍️ 标准语法 (Syntax)
```cpp
