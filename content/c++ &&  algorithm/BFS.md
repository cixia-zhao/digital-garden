
## 发现输出-1，可能 continue 写成 return 了

## 依赖于输入变量的东西必须写在这个变量输入后，而不是全局；

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

## 【状压 BFS (字符串流派)】模板

```cpp
#include <bits/stdc++.h>
using namespace std;

// ================= 1. 全局变量区 (状态空间三件套) =================
unordered_map<string, int> dist; // 查库存钢印本：记录每张“照片”出现的最短步数
queue<string> q;                 // 办事大厅：存的是“照片”
int ans = -1;                    // 全局大喇叭
string tar = " ...";             // 🎯 目标照片 (记得最前面加空格占位！)

// 物理方向盘 (视题目变异规则而定)
int dx[5] = {0, 1, 0, -1, 0};
int dy[5] = {0, 0, 1, 0, -1};
int N = 3; // 矩阵的宽度 (如 3x3 则为 3)

// ================= 2. 幕后翻译机 (极其关键的解耦) =================
// 作用：把一维字符串照片，洗成你最熟悉的二维画板
void stom(string s, int g[10][10]) 
{
    // i 的上限看题目总共有几个格子
    for(int i = 1; i <= N * N; ++i) 
    {
        int r = (i - 1) / N + 1;
        int c = (i - 1) % N + 1;
        g[r][c] = s[i] - '0'; // 字符转数字
    }
}

// 作用：把二维画板上的废墟，重新拍成一张一维字符串照片
string mtos(int g[10][10]) 
{
    string s = " "; // 灵魂空格：维持万物从 1 开始！
    for(int i = 1; i <= N * N; ++i) 
    {
        int r = (i - 1) / N + 1;
        int c = (i - 1) % N + 1;
        s += to_string(g[r][c]); // 数字转字符拼上去
    }
    return s;
}

// ================= 3. 纯血无参干活机器 =================
void bfs()
{
    while(q.size() > 0)
    {
        string x = q.front();
        q.pop();
        
        // 🎯 1. 单点出口：长相跟目标一模一样，下班！
        if(x == tar)
        {
            ans = dist[x];
            return ;
        }
        
        // 🎯 2. 核心分支：枚举所有的【操作】 (比如按 9 个开关，或者移动空格)
        for(int i = 1; i <= N * N; ++i)
        {
            // --- 阶段 A：拿原片复印，准备作案 ---
            int g[10][10];
            stom(x, g); // 自动复印成二维矩阵，随便炸，不影响原字符串 x
            
            int r = (i - 1) / N + 1;
            int c = (i - 1) % N + 1;
            
            // --- 阶段 B：实施物理变异 (因题目而异) ---
            for(int j = 0; j < 5; ++j)
            {
                int nx = r + dx[j];
                int ny = c + dy[j]; 
                
                // 物理越界拦截
                if(nx < 1 || nx > N || ny < 1 || ny > N) continue;
                
                g[nx][ny] = 1 - g[nx][ny]; // 变异规则 (开灯题是翻转，八数码题是 swap 交换)
            }
            
            // --- 阶段 C：将作案现场拍成新照片 ---
            string ne_x = mtos(g);
            
            // ============ 安检门 (一贯的 continue 风格) ============
            if(dist.count(ne_x) != 0) continue; // 查库存：哈希表里有了，说明别人走过
            
            // ============ 进门盖章 ============
            dist[ne_x] = dist[x] + 1; 
            q.push(ne_x);
        }
    }
}

// ================= 4. 调度室 =================
int main()
{
    ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    
    // 开局拼接带空格的照片
    string sta_s = " ";
    for(int i = 1; i <= N * N; ++i)
    {
        char c;
        cin >> c;
        sta_s += c; 
    } 
    
    // 起点入队
    q.push(sta_s);
    dist[sta_s] = 0;
    
    bfs();
    cout << ans << '\n';
    
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
# P2385 [USACO07FEB] Bronze Lilypad Pond B

## 题目描述

为了让奶牛们娱乐和锻炼，农夫约翰建造了一个美丽的池塘。这个长方形的池子被分成了 M 行 N 列个方格（1 ≤ M, N ≤ 30） 。一些格子是坚固得令人惊讶的莲花，还有一些格子是岩石，其余的只是美丽、纯净、湛蓝的水。

贝西正在练习芭蕾舞，她站在一朵莲花上，想跳到另一朵莲花上去，她只能从一朵莲花跳到另一朵莲花上，既不能跳到水里，也不能跳到岩石上。

贝西的舞步很像象棋中的马步：每次总是先横向移动 M1 (1 ≤ M1 ≤ 30)格，再纵向移动 M2 (1 ≤ M2 ≤ 30, M1≠M2)格，或先纵向移动 M1 格，再横向移动 M2 格。最多时，贝西会有八个移动方向可供选择。

给定池塘的布局和贝西的跳跃长度，请计算贝西从起点出发，到达目的地的最小步数，我们保证输入数据中的目的地一定是可达的。

## 输入格式

第一行：四个用空格分开的整数：M，N，M1 和 M2

第二行到 M + 1 行：第 i + 1 行有 N 个用空格分开的整数，描述了池塘第

i 行的状态：0 为水，1 为莲花，2 为岩石，3 为贝西所在的起点，4 为贝西想去

的终点。

## 输出格式

第一行：从起点到终点的最少步数。

## 输入输出样例 #1

### 输入 #1

```
4 5 1 2
1 0 1 0 1
3 0 2 0 4
0 1 2 0 0
0 0 0 1 0
```

### 输出 #1

```
2
```

```cpp
#include <bits/stdc++.h>
using namespace std;
const int N = 39;
int dist[N][N],g[N][N];
queue<pair<int,int>> q;
int n,m,m1,m2;
int sx,sy,ex,ey;



void bfs()
{
	int dx[9] = {0,m1,m2,-m1,-m2,m1,m2,-m1,-m2};
	int dy[9] = {0,m2,m1,m2,m1,-m2,-m1,-m2,-m1};
	while(q.size()>0)
	{
		auto t = q.front();
		q.pop();
		int x = t.first;
		int y = t.second;
		
		if(x==ex&&y==ey) return ;
		for(int i = 1;i <= 8;++i)
		{
			int nx = x+dx[i];
			int ny = y+dy[i];
			
			if(nx < 1 || nx > n || ny < 1 || ny > m) continue;
			if(g[nx][ny] == 2 || g[nx][ny] == 0) continue;
			if(dist[nx][ny] != -1) continue;
			
			dist[nx][ny] = dist[x][y]+1;
			q.push({nx,ny});
			
		}
		
		
	}
	
	
}


int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	cin >> n >> m >> m1 >> m2;
	memset(dist,-1,sizeof(dist));
	for(int i = 1;i <= n;++i)
	{
		for(int j = 1;j <= m;++j)
		{
			cin >> g[i][j];
			if(g[i][j] == 3) sx = i,sy = j;
			if(g[i][j] == 4) ex = i,ey = j;
			
		}
	}
	q.push({sx,sy});
	dist[sx][sy] = 0;
	
	bfs();
	
	cout << dist[ex][ey] <<'\n';
		
	
	
	
	return 0;
 } 
```


# 多源bfs
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
# 173,矩阵距离


给定一个 N 行 M 列的 01 矩阵 A，A[i][j] 与 A[k][l] 之间的曼哈顿距离定义为：

dist(i,j,k,l)=|i−k|+|j−l|

输出一个 N 行 M 列的整数矩阵 B，其中：

B[i][j]=min1≤x≤N,1≤y≤M,A[x][y]=1dist(i,j,x,y)

#### 输入格式

第一行两个整数 N,M。

接下来一个 N 行 M 列的 01 矩阵，数字之间没有空格。

#### 输出格式

一个 N 行 M 列的矩阵 B，相邻两个整数之间用一个空格隔开。

#### 数据范围

1≤N,M≤1000

#### 输入样例：

```
3 4
0001
0011
0110
```

#### 输出样例：

```
3 2 1 0
2 1 0 0
1 0 0 1
```

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 1009;
queue <pair<int,int>> q;
int n,m;
int dx[5] = {0,1,0,-1,0};
int dy[5] = {0,0,1,0,-1};
int dist[N][N];
char g[N][N]; //char

void bfs()
{
	while(q.size() > 0)
	{
		auto t = q.front();
		q.pop();
		int x = t.first;
		int y = t.second;
		
		for(int i = 1;i <= 4;++i)
		{
			int nx = x+dx[i];
			int ny = y+dy[i];
			
			if(nx < 1 || nx > n || ny < 1 || ny > m) continue;
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
	cin >> n >> m;
	for(int i = 1;i <= n;++i)
	{
		for(int j = 1;j <= m;++j)
		{
			cin >> g[i][j];
			
			if(g[i][j] == '1') 
			{
				q.push({i,j});
				dist[i][j] = 0;
			}
		}
	}
	
	bfs();
	
	for(int i = 1;i <= n;++i)
	{
		for(int j = 1;j <= m;++j)
		{
			cout << dist[i][j] <<" \n"[j==m];
		}
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

# P2895 [USACO08FEB] Meteor Shower S

## 题目描述

贝茜听说一场特别的流星雨即将到来：这些流星会撞向地球，并摧毁它们所撞击的任何东西。她为自己的安全感到焦虑，发誓要找到一个安全的地方（一个永远不会被流星摧毁的地方）。

如果将牧场放入一个直角坐标系中，贝茜现在的位置是原点，并且，贝茜不能踏上一块被流星砸过的土地。

根据预报，一共有 $M$ 颗流星 $(1\leq M\leq 50,000)$ 会坠落在农场上，其中第 $i$ 颗流星会在时刻 $T_i$（$0 \leq T _ i \leq 1000$）砸在坐标为 $(X_i,Y_i)(0\leq X_i\leq 300$，$0\leq Y_i\leq 300)$ 的格子里。流星的力量会将它所在的格子，以及周围 $4$ 个相邻的格子都化为焦土，当然贝茜也无法再在这些格子上行走。

贝茜在时刻 $0$ 开始行动，她只能在会在横纵坐标 $X,Y\ge 0$ 的区域中，平行于坐标轴行动，每 $1$ 个时刻中，她能移动到相邻的（一般是 $4$ 个）格子中的任意一个，当然目标格子要没有被烧焦才行。如果一个格子在时刻 $t$ 被流星撞击或烧焦，那么贝茜只能在 $t$ 之前的时刻在这个格子里出现。 贝茜一开始在 $(0,0)$。

请你计算一下，贝茜最少需要多少时间才能到达一个安全的格子。如果不可能到达输出 $−1$。

## 输入格式

共 $M+1$ 行，第 $1$ 行输入一个整数 $M$，接下来的 $M$ 行每行输入三个整数分别为 $X_i, Y_i, T_i$。

## 输出格式

贝茜到达安全地点所需的最短时间，如果不可能，则为 $-1$。

## 输入输出样例 #1

### 输入 #1

```
4
0 0 2
2 1 2
1 1 2
0 3 5

```

### 输出 #1

```
5

```

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 310;
int dist[N][N],g[N][N],d[N][N];
queue<pair<int,int>> q;
int m,ans = -1;
int dx[5] = {0,-1,0,1,0};
int dy[5] = {0,0,-1,0,1};

void bfs()
{
	
	if(d[1][1] == 0) return ;
	//特判 
	while(q.size() > 0)
	{
		auto t = q.front();
		q.pop();
		int x = t.first;
		int y = t.second;
		
		if(d[x][y] == 9999)  
		{
			ans = dist[x][y];
			return ;
		}
		
		for(int i = 1;i <= 4;++i)
		{
			int nx = x + dx[i];
			int ny = y + dy[i];
			
			if(nx < 1 || nx > 305 || ny < 1 || ny > 305) continue;
			if(dist[nx][ny] != -1) continue;
			if(dist[x][y] + 1 >= d[nx][ny]) continue;// 同时出现也不行 所以有等号； 
			
			dist[nx][ny] = dist[x][y] + 1;
			q.push({nx,ny}); 
		}
		
		
		
	}
	
	
 } 

int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	cin >> m;
	
	for(int i = 1;i <= 305;++i)
	{
		for(int j = 1;j <= 305;++j) //遍历的时候 不能等于或者大于N; 
		{
			d[i][j] = 9999;
		}
	}
	memset(dist,-1,sizeof(dist)); 
	
	for(int i = 1; i <= m;++i)
	{
		int x,y,t;
		
			cin >> x >> y >> t;
			x += 1;
			y += 1; //坐标x1 题目说了从0开始，转换一下； 
			
		d[x][y] = min(d[x][y],t);//注意 可能同一个位置 所以取最先的； 
		for(int i = 1;i <= 4;++i) //方向四周的  要接着 初位置定义的地方，初位置来一个，扫一下四周； 
		{
		int nx = x+dx[i];
		int ny = y+dy[i];
		d[nx][ny] = min(d[nx][ny],t) ;// 流星会同时砸四周； 
		}
	}
	
	q.push({1,1});
	dist[1][1] = 0;
	bfs();
	
	cout << ans <<'\n';
	
	return 0;
}
```

# P1135 奇怪的电梯

## 题目背景

感谢 @[yummy](https://www.luogu.com.cn/user/101694) 提供的一些数据。

## 题目描述

呵呵，有一天我做了一个梦，梦见了一种很奇怪的电梯。大楼的每一层楼都可以停电梯，而且第 $i$ 层楼（$1 \le i \le N$）上有一个数字 $K_i$（$0 \le K_i \le N$）。电梯只有四个按钮：开，关，上，下。上下的层数等于当前楼层上的那个数字。当然，如果不能满足要求，相应的按钮就会失灵。例如：$3, 3, 1, 2, 5$ 代表了 $K_i$（$K_1=3$，$K_2=3$，……），从 $1$ 楼开始。在 $1$ 楼，按“上”可以到 $4$ 楼，按“下”是不起作用的，因为没有 $-2$ 楼。那么，从 $A$ 楼到 $B$ 楼至少要按几次按钮呢？

## 输入格式

共二行。  

第一行为三个用空格隔开的正整数，表示 $N, A, B$（$1 \le N \le 200$，$1 \le A, B \le N$）。

第二行为 $N$ 个用空格隔开的非负整数，表示 $K_i$。

## 输出格式

一行，即最少按键次数，若无法到达，则输出 `-1`。

## 输入输出样例 #1

### 输入 #1

```
5 1 5
3 3 1 2 5

```

### 输出 #1

```
3

```

## 说明/提示

对于 $100 \%$ 的数据，$1 \le N \le 200$，$1 \le A, B \le N$，$0 \le K_i \le N$。

本题共 $16$ 个测试点，前 $15$ 个每个测试点 $6$ 分，最后一个测试点 $10$ 分。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 220;
queue <int> q;
int dist[N],k[N];
int n,a,b;
int ans = -1;

void bfs()
{
	while(q.size() > 0)
	{
		
		auto t = q.front();
		q.pop();
		int x = t;
		
		if(x==b) 
		{
			ans = dist[x];
			return ;
		}
		
		int dx[3] = {0,k[x],-k[x]};
		
		for(int i = 1;i <= 2;++i)
		{
			int nx = x + dx[i];
			
			if(nx < 1 || nx > n) continue;
			if(dist[nx] != -1) continue;
			
			dist[nx] = dist[x] + 1;
			q.push(nx);
		}
		
	}
	
	
 } 

int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	memset(dist,-1,sizeof(dist));
	cin >> n >> a >> b;
	for(int i = 1;i <= n;++i)
	{
		cin >> k[i];
	}
	q.push(a);
	dist[a] = 0;
	
	bfs();
	cout << ans <<'\n';
	
	
	return 0;
}
```

# P2040 打开所有的灯

## 题目背景

pmshz 在玩一个益 (ruo) 智 (zhi) 的小游戏，目的是打开九盏灯所有的灯，这样的游戏难倒了 pmshz……

## 题目描述

这个灯很奇 (fan) 怪 (ren)，点一下就会将这个灯和其周围四盏灯的开关状态全部改变。现在你的任务就是就是告诉 pmshz 要全部打开这些灯。

例如
```plain
0  1  1
1  0  0
1  0  1
```
点一下最中间的灯 $(2,2)$ 就变成了

```plain
0  0  1
0  1  1
1  1  1
```

再点一下左上角的灯 $(1,1)$ 就变成了

```plain
1  1  1
1  1  1
1  1  1
```

达成目标。

最少需要 $2$ 步。

## 输入格式

$9$ 个数字，以 $3\times3$ 的格式输入，每两个数字中间只有一个空格，表示灯初始的开关状态。（$0$ 表示关，$1$ 表示开）

## 输出格式

一个整数，表示最少打开所有灯所需要的步数。

## 输入输出样例 #1

### 输入 #1

```
0 1 1
1 0 0
1 0 1
```

### 输出 #1

```
2
```

## 说明/提示

这个题水不水，就看你怎么考虑了……

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
unordered_map<string,int> dist;
queue <string> q;
int ans = -1;
string tar = " 111111111";//留空 s从一开始 
int dx[5] = {0,1,0,-1,0};
int dy[5] = {0,0,1,0,-1};//这里是余波 不是门 包括自己 0有效哦 

void stom(string s,int g[4][4])
{
	for(int i = 1;i <= 9;++i)
	{
		int r = (i-1) / 3 + 1;
		int c = (i-1) % 3 + 1;
		g[r][c] = s[i] - '0';
		
	 } 
}
string mtos(int g[4][4])
{
	string s = " ";
	for(int i = 1;i <= 9;++i)
	{
		int r = (i-1) / 3 + 1;
		int c = (i-1) % 3 + 1;
		s += to_string(g[r][c]);// 数字变字符直接拼 ； 
	}
	return s;
}

void bfs()
{
	while(q.size() > 0)
	{
		auto t = q.front();
		q.pop();
		string x = t;
		if(x == tar)
		{
			ans = dist[x];
			return ;
		}
		
		for(int i = 1;i <= 9;++i) //这个才是移动 
		{
			int g[4][4];
			stom(x,g); //转换成矩阵坐标 方便 变换； 
			int r = (i-1) / 3 + 1;
			int c = (i-1) % 3 + 1;//算二维矩阵坐标，相当于 x,y 
			
			for(int j = 0;j < 5;++j)//这个是算余波 不是方向 
			{
				int nx = r + dx[j];
				int ny = c + dy[j]; 
				if(nx < 1 || nx > 3 || ny < 1 || ny > 3) continue;
				g[nx][ny] = 1 - g[nx][ny];//翻转 
				
			}
			
			string ne_x = mtos(g) ;
			if(dist.count(ne_x) != 0) continue;//是否重复 安检 
			
			dist[ne_x] = dist[x] + 1; 
			q.push(ne_x);
				
			
			
			
		}
		
	}
	
	
}


int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	string sta_s = " ";//从一开始 
	for(int i =1;i <= 9;++i)
	{
		char c;
		cin >> c;
		sta_s += c; 
	 } 
	q.push(sta_s);
	dist[sta_s] = 0;//入队 
	bfs();
	cout << ans <<'\n';
	
	
	
	return 0;
}
```