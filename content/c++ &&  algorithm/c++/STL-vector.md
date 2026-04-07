---
title: vector容器
tags:
related: []
date: 2026-01-30T18:14:00
Revision Time: 2026-03-03T21:49:00
---

### 🎯 核心功能 (Purpose)
> vector(矢量表):一个可以扩容的数组
> 定义：
![[Screenshot_2026-01-30-18-21-24-66_149003a2d400f6adb210d7e357a3a646.jpg]]

> 方法：
> 1. v.push_back() 插入元素
> 2. v.size() 计算v大小
> 3. v.pop_back() 弹出最后一个元素
> 4. v.resize() 重新定义vector大小
> 

### ✍️ 标准语法 (Syntax)

![[Screenshot_2026-01-30-18-19-41-46_149003a2d400f6adb210d7e357a3a646.jpg]]

基于 for each 的另一种写法：
![[Screenshot_2026-01-30-18-22-58-97_149003a2d400f6adb210d7e357a3a646.jpg]]
排序去重：
![[Screenshot_2026-03-03-21-49-43-51_769977972775e0c6b41aa3dfaf766445.jpg]]
也可以 用unique 返回的地址减头指针 求出长度
遍历的时候遍历到长度即可。

普通数组：
// a 是数组首地址（头指针）
int len = unique(a, a + n) - a; 
Vector：
// v.begin() 是首地址迭代器（头指针）
int len = unique(v.begin(), v.end()) - v.begin(); 
