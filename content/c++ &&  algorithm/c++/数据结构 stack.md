---
title: stack
tags:
related: []
date: 2026-02-02T13:26:00
---
[[STL-map]]
[[数据结构 quque]]
[[数据结构 stack]]
[[sort]]
[[STL-set]]
### 🎯 核心功能 (Purpose)
>内容：
>![[Screenshot_2026-02-02-13-31-43-23_149003a2d400f6adb210d7e357a3a646.jpg]]

# #✍️ 模板

# B3614 【模板】栈

## 题目描述

请你实现一个栈（stack），支持如下操作：
- `push(x)`：向栈中加入一个数 $x$。
- `pop()`：将栈顶弹出。如果此时栈为空则不进行弹出操作，输出 `Empty`。
- `query()`：输出栈顶元素，如果此时栈为空则输出 `Anguei!`。
- `size()`：输出此时栈内元素个数。

## 输入格式

**本题单测试点内有多组数据**。  
输入第一行是一个整数 $T$，表示数据组数。对于每组数据，格式如下：  
每组数据第一行是一个整数，表示操作的次数 $n$。  
接下来 $n$ 行，每行首先由一个字符串，为 `push`，`pop`，`query` 和 `size` 之一。若为 `push`，则其后有一个整数 $x$，表示要被加入的数，$x$ 和字符串之间用空格隔开；若不是 `push`，则本行没有其它内容。

## 输出格式

对于每组数据，按照「题目描述」中的要求依次输出。每次输出占一行。

## 输入输出样例 #1

### 输入 #1

```
2
5
push 2
query
size
pop
query
3
pop
query
size
```

### 输出 #1

```
2
1
Anguei!
Empty
Anguei!
0
```

## 说明/提示

### 样例 1 解释
对于第二组数据，始终为空，所以 `pop` 和 `query` 均需要输出对应字符串。栈的 size 为 0。

### 数据规模与约定

对于全部的测试点，保证 $1 \leq T, n\leq 10^6$，且单个测试点内的 $n$ 之和不超过 $10^6$，即 $\sum n \leq 10^6$。保证 $0 \leq x \lt 2^{64}$。

### 提示
- 请注意大量数据读入对程序效率造成的影响。
- 请注意输出的 `Empty` 不含叹号，`Anguei!` 含有叹号。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int n;
unsigned long long  x; //2e64

int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	int T;cin >> T;
	while(T--)//全局 
	{//记得清全局；
		stack <unsigned long long> s;//这种开局自动0的直接开main 
	 cin >> n; string op;
	 for(int i = 1;i <= n;++i)
	 { 
	 	cin >> op;
	 
	 	if(op == "push") 
	 	{
	 		cin >> x;
	 		s.push(x);
		 }
		 else if(op == "pop")
		 {
		 	if(s.size() > 0) s.pop();
			else  cout << "Empty" <<'\n';
		 }
		 else if(op == "query") 
		 {
		 	if(!s.empty()) cout << s.top() <<'\n';
		 	else cout << "Anguei!" <<'\n';
		 }
		 else if(op == "size")
		 {
		 	cout << s.size() <<'\n';
		 }
	 
	 }
		
	}
	
	return 0;
}
```
