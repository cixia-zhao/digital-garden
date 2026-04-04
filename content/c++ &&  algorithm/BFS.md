
## 发现输出-1，可能 continue 写成 return 了
## 万能无参 BFS模板:
```cpp
#include <bits/stdc++.h>
using namespace std;

// ================= 全局变量区 =================
const int N = 505;       
int dist[N][N];          // 二合一账本
int n, m;

int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

// 【核心蜕变】：办事大厅直接提拔为全局变量！
queue<pair<int, int>> q; 

// ================= 纯粹的干活机器 =================
// 连参数 sx, sy 都不需要了！它就是一个无情的叫号机
void bfs() 
{
    while (q.size() > 0) 
    {
        auto t = q.front(); 
        q.pop(); 
        
        int x = t.first;
        int y = t.second;

        // 如果题目需要单点出口，就在这里加 if(x == ex && y == ey) return;
        // 如果是全图蔓延，就不写出口，随它去。

        for (int i = 0; i < 4; ++i) 
        {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if (nx < 1 || nx > n || ny < 1 || ny > m) continue; 
            // if (g[nx][ny] == '#') continue;  // 撞墙安检（视题目而定）
            if (dist[nx][ny] != -1) continue;                   

            dist[nx][ny] = dist[x][y] + 1; 
            q.push({nx, ny});                      
        }
    }
}

int main() 
{
    ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    
    // 假设读入了 n 和 m
    if (cin >> n >> m) 
    {
        // 1. 场地大扫除（管你单源多源，开局必擦地）
        memset(dist, -1, sizeof(dist));

        // 2. 调度室放毒气弹！
        // ===============================================
        // 【单起点情况】
        // cin >> sx >> sy;
        // q.push({sx, sy});
        // dist[sx][sy] = 0;
        
        // 【多起点情况】
        // for(int i=1; i<=k; ++i) { 
        //     cin >> x >> y; 
        //     q.push({x, y}); 
        //     dist[x][y] = 0; 
        // }
        // ===============================================

        // 3. 关门，放狗！
        bfs();
        
        // 4. 查账本输出结果
        // cout << dist[ex][ey] << '\n';
    }
    
    return 0;
}
```

# P1443 马的遍历

## 题目描述

有一个 $n \times m$ 的棋盘，在某个点 $(x, y)$ 上有一个马，要求你计算出马到达棋盘上任意一个点最少要走几步。

## 输入格式

输入只有一行四个整数，分别为 $n, m, x, y$。

## 输出格式

一个 $n \times m$ 的矩阵，代表马到达某个点最少要走几步（不能到达则输出 $-1$）。

## 输入输出样例 #1

### 输入 #1

```
3 3 1 1

```

### 输出 #1

```
0 3 2    
3 -1 1    
2 1 4    
```

## 说明/提示

### 数据规模与约定

对于全部的测试点，保证 $1 \leq x \leq n \leq 400$，$1 \leq y \leq m \leq 400$。

2022 年 8 月之后，本题去除了对输出保留场宽的要求。为了与之兼容，本题的输出以空格或者合理的场宽分割每个整数都将判作正确。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 410;
int dist[N][N];
int n,m,sx,sy;
int dx[9] = {0,-2,-1,2,1,-2,-1,2,1};
int dy[9] = {0,1,2,1,2,-1,-2,-1,-2};
queue<pair<int,int>> q;
void bfs()
{
	while(q.size()> 0)
	{
		auto t = q.front();
		q.pop();
		int x = t.first;
		int y = t.second;
		
		//如果有出口；
		
		for(int i = 1;i <= 8;++i)//注意 方向数
		{
			int nx = x + dx[i];
			int ny = y + dy[i];
			
			if(nx < 1 || nx > n || ny < 1 || ny > m) continue; // 是或者
			// 撞墙； 
			if(dist[nx][ny] != -1) continue;
			dist[nx][ny] = dist[x][y] + 1;
			q.push({nx,ny});
			
		 } 
	}
	
	
}

int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	cin >> n >> m >> sx >> sy;
	
	memset(dist,-1,sizeof(dist));
	q.push({sx,sy});
	dist[sx][sy] = 0;
	
	bfs();
	for(int i = 1;i <= n;i++)
	{
		for(int j = 1;j <= m;j++)
		{
			cout << left << setw(5) << dist[i][j] <<' ';
		}
		cout <<'\n';
	}
	
	return 0;
}
```

# P1332 血色先锋队

## 题目背景

巫妖王的天灾军团终于卷土重来，血色十字军组织了一支先锋军前往诺森德大陆对抗天灾军团，以及一切沾有亡灵气息的生物。孤立于联盟和部落的血色先锋军很快就遭到了天灾军团的重重包围，现在他们将主力只好聚集了起来，以抵抗天灾军团的围剿。可怕的是，他们之中有人感染上了亡灵瘟疫，如果不设法阻止瘟疫的扩散，很快就会遭到灭顶之灾。大领主阿比迪斯已经开始调查瘟疫的源头。原来是血色先锋军的内部出现了叛徒，这个叛徒已经投靠了天灾军团，想要将整个血色先锋军全部转化为天灾军团！无需惊讶，你就是那个叛徒。在你的行踪败露之前，要尽快完成巫妖王交给你的任务。

## 题目描述

军团是一个 $n$ 行 $m$ 列的矩阵，每个单元是一个血色先锋军的成员。感染瘟疫的人，每过一个小时，就会向四周扩散瘟疫，直到所有人全部感染上瘟疫。你已经掌握了感染源的位置，任务是算出血色先锋军的领主们感染瘟疫的时间，并且将它报告给巫妖王，以便对血色先锋军进行一轮有针对性的围剿。

## 输入格式

第 $1$ 行：四个整数 $n$，$m$，$a$，$b$，表示军团矩阵有 $n$ 行 $m$ 列。有 $a$ 个感染源，$b$ 为血色敢死队中领主的数量。

接下来 $a$ 行：每行有两个整数 $x$，$y$，表示感染源在第 $x$ 行第 $y$ 列。

接下来 $b$ 行：每行有两个整数 $x$，$y$，表示领主的位置在第 $x$ 行第 $y$ 列。

## 输出格式

第 $1$ 至 $b$ 行：每行一个整数，表示这个领主感染瘟疫的时间，输出顺序与输入顺序一致。如果某个人的位置在感染源，那么他感染瘟疫的时间为 $0$。

## 输入输出样例 #1

### 输入 #1

```
5 4 2 3
1 1
5 4
3 3
5 3
2 4

```

### 输出 #1

```
3
1
3
```

## 说明/提示

#### 输入输出样例 1 解释

如下图，标记出了所有人感染瘟疫的时间以及感染源和领主的位置。

![](https://cdn.luogu.com.cn/upload/image_hosting/3j3g02cn.png)

#### 数据规模与约定

对于 $100\%$ 的数据，保证 $1\le n,m\le500$，$1\le a,b\le10^5$。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 509;
int dist[N][N],g[N][N];
int n,m,a,b;
int dx[5] = {0,-1,0,1,0};
int dy[5] = {0,0,1,0,-1};
int sx,sy;
pair <int,int> lz[100009]; // 存一对数据的数组； 
queue<pair<int,int>> q;

void bfs()
{
	while(q.size()>0)
	{
		auto t = q.front();
		int x = t.first;
		int y = t.second;
		q.pop();
		for(int i = 1;i <= 4;++i)
		{
			int nx = x+dx[i];
			int ny = y+dy[i];
			
			if(nx < 1 || nx > n || ny < 1 || ny > m) continue ;
			if(dist[nx][ny] != -1) continue; ;
			
			dist[nx][ny] = dist[x][y] + 1;
			q.push({nx,ny});
			
		}
	}
	
	
 } 



int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	cin >> n >> m >> a >> b;
	memset(dist,-1,sizeof(dist));
	for(int i = 1;i <= a;++i)
	{
		cin >> sx >> sy;
		q.push({sx,sy});
		dist[sx][sy] = 0;
	}
	for(int i = 1;i <= b;++i)
	{
		cin >> lz[i].first >> lz[i].second;
	}
	
	bfs();
	for(int i = 1;i <= b;++i)
	{
		cout << dist[lz[i].first][lz[i].second] <<'\n';
	 } 
	
	
	return 0;
}
```

# P1747 好奇怪的游戏

## 题目背景

《爱与愁的故事第三弹·shopping》娱乐章。

调调口味来道水题。

## 题目描述

爱与愁大神坐在公交车上无聊，于是玩起了手机。一款奇怪的游戏进入了爱与愁大神的眼帘：\*\*\*（游戏名被打上了马赛克）。这个游戏类似象棋，但是只有黑白马各一匹，在点 $x_1,y_1$ 和 $x_2,y_2$ 上。它们得从点 $x_1,y_1$ 和 $x_2,y_2$ 走到 $(1,1)$。这个游戏与普通象棋不同的地方是：马可以走“日”，也可以像象走“田”。现在爱与愁大神想知道两匹马到 $(1,1)$ 的最少步数，你能帮他解决这个问题么？

注意不能走到 $x$ 或 $y$ 坐标 $\le 0$ 的位置。满足此限制的 $(x,y)$ 均可到达。

## 输入格式

第一行两个整数 $x_1,y_1$。

第二行两个整数 $x_2,y_2$。

## 输出格式

第一行一个整数，表示黑马到 $(1,1)$ 的步数。

第二行一个整数，表示白马到 $(1,1)$ 的步数。

## 输入输出样例 #1

### 输入 #1

```
12 16
18 10
```

### 输出 #1

```
8 
9
```

## 说明/提示

### 数据范围及约定

对于 $100\%$ 数据，$1\le x_1,y_1,x_2,y_2 \le 20$。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 29;
int dist[N][N],g[N][N];
int dx[13] = {0,-2,-2,-1,2,2,1,-2,-2,-1,2,2,1};
int dy[13] = {0,1,2,2,1,2,2,-1,-2,-2,-1,-2,-2};
queue<pair<int,int>> q;
int x1,x2,z1,z2;

void bfs()
{
	while(q.size() > 0)
	{
		auto t = q.front();
		q.pop();
		int x = t.first;
		int y = t.second;
		
		for(int i = 1;i <= 12;++i)
		{
			int nx = x+dx[i];
			int ny = y+dy[i];
			
			if(nx < 1 || nx > 25 || ny < 1 || ny > 25) continue; //小心越界 数组边界可不能随便跳； 
			if(dist[nx][ny] != -1) continue;
			
			dist[nx][ny] = dist[x][y] + 1;
			q.push({nx,ny});
			
		}
		
	}
	
}

int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	memset(dist,-1,sizeof(dist));
	
	q.push({1,1});
	dist[1][1] = 0;
	
	cin >> x1 >> z1;
	cin >> x2 >> z2;
	bfs();
	cout << dist[x1][z1] <<'\n';
	cout << dist[x2][z2] <<'\n';
	
	
	return 0;
}
```
