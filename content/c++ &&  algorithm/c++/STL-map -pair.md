---
title: STL-map
tags:
related:
  - pair
date: 2026-02-01T22:17:00
revision time 1: 2026-02-02T13:24:00
Revision Time: 2026-03-03T19:19:00
---

### 🎯 核心功能 (Purpose)
> map ,里面键值对两者之间有映射关系

map<KeyType, ValueType>` 是一个存储 键(Key)-值(Value)对的关联容器。

*   **KeyType**：键的类型（下标），用于唯一标识和查找。  
*   **ValueType**：值的类型，是与键相关联的数据。

    *   当 `ValueType` 是一个普通类型（如 `int`）时，它表现为**一对一**映射。  
    *   当 `ValueType` 是一个容器类型（如 `vector`）时，它表现为**一对多**映射。

> ![[Screenshot_2026-02-01-22-16-58-26_149003a2d400f6adb210d7e357a3a646.jpg]]

键值对 插入方法：
![[Screenshot_2026-02-01-22-23-59-08_149003a2d400f6adb210d7e357a3a646.jpg]]

补充：
![[Screenshot_2026-03-04-12-55-12-25_769977972775e0c6b41aa3dfaf766445.jpg]]
map 使用示例：
![[Screenshot_2026-03-04-13-01-12-27_769977972775e0c6b41aa3dfaf766445.jpg]]
最新的遍历方法：
for (auto const& [key, val] : my_map) {
    // 直接使用 key 和 val
}



pair：

定义示例：
![[Screenshot_2026-02-02-13-20-52-33_149003a2d400f6adb210d7e357a3a646.jpg]]

![[Screenshot_2026-02-02-13-21-57-47_149003a2d400f6adb210d7e357a3a646.jpg]]
补充：

![[Screenshot_2026-02-02-13-23-37-42_149003a2d400f6adb210d7e357a3a646.jpg]]
![[Screenshot_2026-03-03-19-17-31-39_769977972775e0c6b41aa3dfaf766445.jpg]]

![[Screenshot_2026-03-03-19-23-16-66_769977972775e0c6b41aa3dfaf766445.jpg]]



### ✍️ 标准语法 (Syntax)
```cpp
