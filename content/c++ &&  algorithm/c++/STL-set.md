---
title: set容器
tags:
related: []
date: 2026-02-01T22:00:00
Revision Time: 2026-03-04T11:51:00
---
[STL-map](STL-map.md)
[数据结构 quque](数据结构%20quque.md)
[数据结构 stack](数据结构%20stack.md)
[sort](sort.md)
[STL-set](STL-set.md)
## `set` 容器核心功能 (Purpose)

**两大核心特点**：

1. **自动去重**：容器内不会有重复的元素。
    
2. **默认正序排序**：插入的元素会自动按照从小到大（升序）排列。
    

---

## 📊 常用操作与方法速查 (Operations)

### 1. 查找与基础判断

- `find(value)`：查找指定的元素。如果找到，返回指向该元素的**迭代器**；如果找不到，返回 **`end()` 的头迭代器**。
    
- `empty()`：判断容器是否为空。
    
- `count(value)`：统计元素出现的次数。
    
    > 💡 **技巧**：因为 `set` 自动去重，所以返回值只能是 `0` 或 `1`。它常被用来**查找一个元素是否存在**。
    

### 2. 边界查找 (Bound)

- `lower_bound(key)`：返回一个迭代器，指向**第一个 $\ge$ key** 的元素。
    
- `upper_bound(key)`：返回一个迭代器，指向**第一个 $>$ key** 的元素。
    

> ⚠️ **注意区分**：
> 
> 图片笔记中提到的 `*lower_bound(arr, arr+7, 3)` 属于 `<algorithm>` 库中对**普通数组**使用的泛型算法格式。
> 
> 如果是对 `set` 容器本身使用，应该直接调用其成员方法，且底层自带排序，格式为：`mySet.lower_bound(3);`

### 3. 删除操作 (Erase)

|**函数形式**|**功能说明**|
|---|---|
|`erase(iterator)`|删除**指定迭代器指向位置**的元素。（注意：`set` 迭代器不支持 `+` 偏移量直接相加）|
|`erase(value)`|直接删除**给定数据值**的那个元素。|
|`erase(iterator A, iterator B)`|删除 `[A, B)` 这个**左闭右开**区间内对应位置的元素。|

---

## ⚙️ 修改排序规则与变体

默认的 `set` 是从小到大排的，如果需要改变这种行为，可以在定义时做文章：



```C++
// 1. 修改为降序 (从大到小)
set<int, greater<int>> s; 

// 2. 使用不排序的 set 集合 (底层是哈希表，查找速度更快)
unordered_set<int> s1; 
```

---

## 💻 `set` 完整代码示例

```C++
#include <iostream>
#include <set>

using namespace std;

int main() {
    set<int> mySet;

    // 1. 插入元素 (测试自动排序和去重)
    mySet.insert(5);
    mySet.insert(2);
    mySet.insert(8);
    mySet.insert(2); // 尝试插入重复元素

    // 此时内部元素顺序自动变为: {2, 5, 8}
    cout << "Set elements: ";
    for (const auto& elem : mySet) {
        cout << elem << " "; 
    }
    cout << endl;

    // 2. 查找元素
    int searchValue = 5;
    auto it = mySet.find(searchValue); // 返回迭代器
    if (it != mySet.end()) {
        cout << searchValue << " found in the set." << endl;
    } else {
        cout << searchValue << " not found in the set." << endl;
    }

    // 3. 移除元素 (按值移除)
    int removeValue = 2;
    mySet.erase(removeValue);

    // 再次遍历，此时元素为: {5, 8}
    cout << "Set elements after removal: ";
    for (const auto& elem : mySet) {
        cout << elem << " ";
    }
    cout << endl;

    // 4. 清空与判空
    mySet.clear(); // 清空集合
    if (mySet.empty()) {
        cout << "Set is empty." << endl;
    } else {
        cout << "Set is not empty." << endl;
    }

    return 0;
}
```

---

## 🧬 拓展：`multiset` 容器

`multiset` 是一种与 `set` 极度相似的容器，用法几乎一模一样。

- **唯一的不同之处**：`multiset` **允许存储重复的元素**。
    

**它的底层定义结构如下：**



```C++
template <class Key, class Compare = less<Key>, class Allocator = allocator<Key>> 
class multiset;
```

- **Key**: 表示存储在 `multiset` 中的元素类型。
    
- **Compare**: 表示元素之间的比较函数对象类型。默认为 `less`（即按照元素的值从小到大进行比较）。
    
- **Allocator**: 表示用于分配内存的分配器类型，默认为 `allocator`。
    

**底层原理**：

无论是 `set` 还是 `multiset`，它们的内部实现通常都使用了**红黑树 (Red-Black Tree)** 这种平衡二叉搜索树来存储元素。这也就是为什么它们能够在插入元素的同时，自动保持元素的有序性。# 例题：

# P5250 【深基17.例5】木材仓库

## 题目描述

博艾市有一个木材仓库，里面可以存储各种长度的木材，但是保证没有两个木材的长度是相同的。作为仓库负责人，你有时候会进货，有时候会出货，因此需要维护这个库存。有不超过 $10^5$ 条的操作：

- 进货，格式 `1 Length`：在仓库中放入一根长度为 $Length$（不超过 $10^9$）的木材。如果已经有相同长度的木材那么输出 `Already Exist`。
- 出货，格式 `2 Length`：从仓库中取出长度为 $Length$ 的木材。如果没有刚好长度的木材，取出仓库中存在的和要求长度最接近的木材。如果有多根木材符合要求，取出比较短的一根。输出取出的木材长度。如果仓库是空的，输出 `Empty`。

## 输入格式

第一行一个数 $m$ 代表操作次数。

接下来 $m$ 行，每行一次操作，格式如题目描述所示。

## 输出格式

对于每次操作，按照题目描述要求输出答案。

## 输入输出样例 #1

### 输入 #1

```
7
1 1
1 5
1 3
2 3
2 3
2 3
2 3
```

### 输出 #1

```
3
1
5
Empty

```


```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

set<int> wood;
int m,op,len;
int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	cin >> m;
	for(int i = 1;i <= m;++i)
	{
		cin >> op >> len;
		if(op == 1)
		{
			if(wood.count(len))
			{
				cout <<"Already Exist"<<'\n';
			}
			else wood.insert(len);
			
		}
		if(op == 2)
		{
			if(wood.empty()) // 判空一定用.empty() 
			{
				cout <<"Empty"<<'\n';
				continue;
			}
			if(wood.count(len))
			{
				auto it = wood.lower_bound(len);
				cout << *it <<'\n';
				wood.erase(it);
			}
			else 
			{
				auto it = wood.lower_bound(len);
				if(it == wood.begin())
				{
					cout << *it <<'\n';
					wood.erase(it);
				}
				else if (it == wood.end())
				{
					--it;
					cout << *it <<'\n';
					wood.erase(it);
				}
				else 
				{
					auto l =it;
					auto r = it;
					--l;
					if(*r - len >= len - *l) // 是接近 
					{
						cout << *l <<'\n';
						wood.erase(l);
					}
					else
					{
						cout << *r <<'\n';
						wood.erase(r);
					}
				}
			}
			
		}
	}
	
	
	return 0;
}
```