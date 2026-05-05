---
title: queue
tags:
related: []
date: 2026-02-02T18:11:00
"Revision Time: 2026-03-03T19:19:00": "3.22"
revision time 1: 2026-04-07T08:55:00
---
[STL-map](STL-map.md)
[数据结构 quque](数据结构%20quque.md)
[数据结构 stack](数据结构%20stack.md)
[sort](sort.md)
[STL-set](STL-set.md)
### 🎯 核心概念
>先进先出
>常用方法：
![Screenshot_2026-02-02-18-13-18-02_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-02-18-13-18-02_149003a2d400f6adb210d7e357a3a646.jpg)

priority_quque 优先队列：按照从大到小顺序入队。
![Screenshot_2026-02-02-18-17-26-20_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-02-18-17-26-20_149003a2d400f6adb210d7e357a3a646.jpg)
     修改比较函数 
     ![Screenshot_2026-03-04-10-44-09-63_769977972775e0c6b41aa3dfaf766445](Screenshot_2026-03-04-10-44-09-63_769977972775e0c6b41aa3dfaf766445.jpg)


双端队列
![Screenshot_2026-03-04-10-50-58-38_769977972775e0c6b41aa3dfaf766445](Screenshot_2026-03-04-10-50-58-38_769977972775e0c6b41aa3dfaf766445.jpg)


  应用：
  
  
![Screenshot_2026-02-02-18-22-35-43_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-02-18-22-35-43_149003a2d400f6adb210d7e357a3a646.jpg)
最后cout输出。


# B3616 【模板】队列

## 题目描述

请你实现一个队列（queue），支持如下操作：
- `push(x)`：向队列中加入一个数 $x$。
- `pop()`：将队首弹出。如果此时队列为空，则不进行弹出操作，并输出 `ERR_CANNOT_POP`。
- `query()`：输出队首元素。如果此时队列为空，则输出 `ERR_CANNOT_QUERY`。
- `size()`：输出此时队列内元素个数。

## 输入格式

第一行，一个整数 $n$，表示操作的次数。  

接下来 $n$ 行，每行表示一个操作。格式如下：

- `1 x`，表示将元素 `x` 加入队列。
- `2`，表示将队首弹出队列。
- `3`，表示查询队首。
- `4`，表示查询队列内元素个数。

## 输出格式

输出若干行，对于每个操作，按「题目描述」输出结果。

每条输出之间应当用空行隔开。

## 输入输出样例 #1

### 输入 #1

```
13
1 2
3
4
1 233
3
2
3
2
4
3
2
1 144
3
```

### 输出 #1

```
2
1
2
233
0
ERR_CANNOT_QUERY
ERR_CANNOT_POP
144
```

## 说明/提示

### 样例解释
首先插入 `2`，队首为 `2`、队列内元素个数为 `1`。  
插入 `233`，此时队首为 `2`。  
弹出队首，此时队首为 `233`。  
弹出队首，此时队首为空。  
再次尝试弹出队首，由于队列已经为空，此时无法弹出。  
插入 `144`，此时队首为 `144`。  



### 数据规模与约定

对于 $100\%$ 的测试数据，满足 $n\leq 10000$，且被插入队列的所有元素值是 $[1, 1000000]$ 以内的正整数。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int n;
unsigned long long  x; //2e64

int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	
	queue <ll> s;//这种开局自动0的直接开main 
	 cin >> n; int op;
	 for(int i = 1;i <= n;++i)
	 { 
	 	cin >> op;
	 
	 	if(op == 1) 
	 	{
	 		cin >> x;
	 		s.push(x);
		 }
		 else if(op == 2)
		 {
		 	if(s.size() > 0) s.pop();
			else  cout << "ERR_CANNOT_POP" <<'\n';
		 }
		 else if(op == 3) 
		 {
		 	if(!s.empty()) cout << s.front() <<'\n';
		 	else cout << "ERR_CANNOT_QUERY" <<'\n';
		 }
		 else if(op == 4)
		 {
		 	cout << s.size() <<'\n';
		 }
	 
	 }
		
	
	
	return 0;
}
```
