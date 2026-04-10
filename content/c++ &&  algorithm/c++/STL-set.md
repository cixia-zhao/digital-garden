---
title: set容器
tags:
related: []
date: 2026-02-01T22:00:00
Revision Time: 2026-03-04T11:51:00
---
[[STL-map]]
[[数据结构 quque]]
[[数据结构 stack]]
[[sort]]
[[STL-set]]
### 🎯 核心功能 (Purpose)
> 特点：自动去重 正序排序

其他：
find(数据)找这个数据的迭代器，找不到则返回end的迭代器
empty() 判空
count() 记元素出现的次数 它才是查找一个元素是否存在的方法。


![[Screenshot_2026-02-01-22-10-52-10_149003a2d400f6adb210d7e357a3a646.jpg]]
lower-bound()使用前必须有序，它们返回的是一个内存地址（下标）。格式：
![[Screenshot_2026-02-07-16-47-45-61_149003a2d400f6adb210d7e357a3a646.jpg]]
修改排序 为降序

![[Screenshot_2026-02-01-22-12-30-97_149003a2d400f6adb210d7e357a3a646.jpg]]
示例
![[Screenshot_2026-03-04-11-57-35-49_769977972775e0c6b41aa3dfaf766445.jpg]]


multiset

![[Screenshot_2026-03-04-11-50-29-98_769977972775e0c6b41aa3dfaf766445.jpg]]

# 例题：

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