---
title: vector容器
tags:
related: []
date: 2026-01-30T18:14:00
Revision Time: 2026-03-03T21:49:00
---
[STL-map](STL-map.md)
[数据结构 quque](数据结构%20quque.md)
[数据结构 stack](数据结构%20stack.md)
[sort](sort.md)
[STL-set](STL-set.md)
## 🎯 核心功能 (Purpose)

**定义**：`vector`（矢量表）可以理解为一个**动态/可扩展的数组**。

它的底层逻辑依旧是一段连续的内存空间（也就是数组），但它的强大之处在于：当容量不够时，它会自动帮你申请更大的内存并把数据搬运过去（自动扩容）。

C++

```
// 定义一个初始容量为 10 的 int 类型 vector
vector<int> v(10); 
```

---

## 🛠️ 常用基础方法 (Methods)

|**方法名**|**功能说明**|
|---|---|
|`v.push_back(val)`|**尾部插入**：在 vector 的最后面追加一个元素。如果容量不够，会自动扩容。|
|`v.pop_back()`|**尾部弹出**：删除 vector 的最后一个元素。|
|`v.size()`|**获取大小**：返回当前 vector 中实际存储的元素个数。|
|`v.resize(n)`|**重置大小**：重新定义 vector 的大小。|

---

## 💻 标准语法与基本操作 (Syntax)

这里演示了如何向 `vector` 中动态添加数据、删除数据以及最基础的下标访问。

C++

```
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> v;

    // 1. 动态插入数据 (容量不够时会自动扩容)
    v.push_back(1);
    v.push_back(2);
    v.push_back(3);
    v.push_back(4);
    
    cout << "当前大小: " << v.size() << endl; // 输出: 4

    // 2. 弹出最后一个元素
    v.pop_back(); // 此时 4 被删除了

    // 3. 传统的 for 循环遍历 (像普通数组一样用下标 i 访问)
    for (int i = 0; i < v.size(); ++i) {
        cout << v[i] << endl;
    }

    return 0;
}
```

---

## 🔄 遍历方式：范围 `for` 循环 (For-each)

除了上面的经典 `for` 循环，C++11 之后强烈推荐使用基于范围的 `for` 循环，代码更简洁，不需要去查容器到底有多长：

C++

```
// 依次将容器 v 中的元素赋值给 x 并打印
for (int x : v) {
    cout << x << endl;
}
```

---

## ✂️ 进阶操作：Vector 排序去重 (Deduplication)

要去除 `vector` 中的重复元素，有一个非常经典的“三步走”套路（需要引入 `<algorithm>` 头文件）：**排序 (Sort) -> 去重 (Unique) -> 删除 (Erase)**。

> **💡 原理简述**：
> 
> `std::unique` 并不会真正删除元素，它只是把相邻的重复元素“移”到了容器的末尾，然后返回一个**指向去重后最后一个有效元素之后位置的迭代器**。因此，必须先排序让重复元素相邻，最后再用 `erase` 把尾部的废弃元素真正删掉。



```C++
#include <iostream>
#include <vector>
#include <algorithm> // 必须包含此头文件

using namespace std;

int main() {
    vector<int> vec = {2, 1, 2, 3, 1, 4};

    // 第一步：排序 (让相同的元素相邻)
    // 排序后: {1, 1, 2, 2, 3, 4}
    std::sort(vec.begin(), vec.end());

    // 第二步：去重 (将重复元素移到末尾，并获取新逻辑末尾的迭代器)
    // 去重后前方有效部分: {1, 2, 3, 4, ...}，last 迭代器指向 4 后面的位置
    auto last = std::unique(vec.begin(), vec.end());

    // 第三步：真实删除 (将 last 到 原本 end 之间的废弃元素抹除)
    vec.erase(last, vec.end());

    return 0;
}
```

### 📏 补充：利用 unique 计算去重后的长度

如果你不需要真正 `erase` 删除尾部元素，只想要知道去重后有多少个独立元素，可以通过指针/迭代器相减来计算长度：

- **普通数组求长度**：
    
    `int len = unique(a, a + n) - a;` （头指针 - 头指针）
    
- **Vector 求长度**：
    
    `int len = unique(v.begin(), v.end()) - v.begin();` （头迭代器 - 头迭代器）