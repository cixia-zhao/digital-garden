

🧠 一、 甩包袱哲学（O(N) 的物理真相）
想象你在招募团队打怪升级，你的战斗力是连续累加的（current_sum）。当你走到第 i 个人（a[i]）面前时，只有两种物理选择：
 * 选择 1：带上前面的兄弟（战斗力 = current_sum + a[i]）。
 * 选择 2：踢掉前面的兄弟，自己单干（战斗力 = a[i]）。
什么时候必须单干？ 当你发现前面的兄弟加起来是个“负资产”（current_sum < 0）时，带上他们只会拉低你当前的战斗力！与其被拖累，不如从 a[i] 开始另起炉灶！
用一行代码概括整个宇宙的抉择：
```cpp
 current_sum = max(a[i], current_sum + a[i]);
```

🚀 二、 四大变种实战（甩包袱哲学的花样玩法）
只要稍微改动一两个符号，这套心法就能瞬间秒杀蓝桥杯中经常出现的四种经典变体：
变种 1：求【最小】连续子段和
 * 物理真相：找团队里最坑爹的一帮人。只要前面的累计亏损是个正数（正资产），对我这个本身就是负数的人来说就是累赘，直接踢掉自己单干！
 * 无脑改法：把所有的 max 换成 min！
 * 核心代码
```cpp
long long min_sum = a[1];
long long current_sum = a[1];

for (int i = 2; i <= n; ++i) {
    // 核心抉择：前面是正资产吗？如果是，果断踢掉，自己单干！
    current_sum = min((long long)a[i], current_sum + a[i]);
    min_sum = min(min_sum, current_sum);
}
// 最终 min_sum 就是全场亏得最惨的连续区间
```
变种 2：定位最大子段和的【左右边界】（查户口）
 * 物理真相：不仅要记录最高战力，还要用游标卡尺把这帮人的门牌号记下来。你需要一个“临时起点”来试探。
 * 核心代码：
```cpp
long long max_sum = a[1], current_sum = a[1];
int start = 1, end = 1, temp_start = 1; // 游标三剑客

for (int i = 2; i <= n; ++i) {
    // 1. 探路阶段：遇到负资产，决定换个新起点单干
    if (a[i] > current_sum + a[i]) {
        current_sum = a[i]; 
        temp_start = i;     // 🌟 重点：记录试探性的新起点
    } else {
        current_sum = current_sum + a[i]; // 继续组队
    }

    // 2. 巅峰时刻：创下历史新高！
    if (current_sum > max_sum) {
        max_sum = current_sum; 
        start = temp_start;    // 🌟 重点：把临时起点正式转正！
        end = i;               // 终点就是当前位置
    }
}
// 最终结果：最大和是 max_sum，区间范围是 [start, end]
```
变种 3：【环形】数组的最大子段和
 * 物理真相：数组首尾相接。答案只有两种可能：
   * 没有跨越首尾边界：这就是普通的“最大连续子段和”。
   * 跨越了首尾边界：相当于中间挖掉了一块最坑爹的。算式为：整个数组的总和 - 数组的【最小】连续子段和。
 * 核心代码：
```cpp
long long total_sum = 0;
long long max_sum = -1e18, cur_max = 0;
long long min_sum = 1e18, cur_min = 0;

for (int i = 1; i <= n; ++i) {
    total_sum += a[i]; // 算总和
    
    // 同时跑两个 Kadane
    cur_max = max((long long)a[i], cur_max + a[i]);
    max_sum = max(max_sum, cur_max);
    
    cur_min = min((long long)a[i], cur_min + a[i]);
    min_sum = min(min_sum, cur_min);
}

// 🚨 极端防御陷阱：如果全都是负数，total_sum 会等于 min_sum，环形相减会变成 0！
// 但题目通常要求“至少选一个数”，0 是不合法的。
long long ans;
if (max_sum < 0) {
    ans = max_sum; // 全是负数，老老实实拿那个最小的负数（最不惨的那个）
} else {
    ans = max(max_sum, total_sum - min_sum); // 普通最大 vs 环形最大，神仙打架
}
```
变种 4：连续子数组的【最大乘积】
 * 物理真相：乘法世界里有“负负得正”的魔法！一个极小的负数，乘以一个负数，瞬间翻盘变成全场最大。因此，必须同时记录当前的最大值和最小值。
 * 核心代码：
```cpp
long long max_prod = a[1];
long long cur_max = a[1];
long long cur_min = a[1];

for (int i = 2; i <= n; ++i) {
    if (a[i] < 0) {
        // 🌟 魔法时刻：遇到负数，最大变最小，最小变最大！
        swap(cur_max, cur_min);
    }
    
    cur_max = max((long long)a[i], cur_max * a[i]);
    cur_min = min((long long)a[i], cur_min * a[i]);
    
    max_prod = max(max_prod, cur_max);
}
```

👑 三、 Kadane 基础模板
不管变种怎么花里胡哨，这套骨架永远是所有逻辑的祖师爷。把下面这几行代码刻在骨子里，上了考场哪怕手抖也能肌肉记忆敲出来：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5 + 9;
long long a[N];

int main() {
    // 极致 I/O 加速
    ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    
    int n;
    if (cin >> n) {
        for (int i = 1; i <= n; ++i) cin >> a[i];
        
        // 1. 历史最高巅峰（🚨 必须用 a[1] 初始化，绝对不能用 0，防全负数陷阱！）
        long long max_sum = a[1];     
        // 2. 当前团队战斗力
        long long current_sum = a[1]; 

        for (int i = 2; i <= n; ++i) {
            // 3. 核心抉择：是单干，还是跟前面的团队混？
            current_sum = max((long long)a[i], current_sum + a[i]);
            
            // 4. 随时记录最高巅峰
            max_sum = max(max_sum, current_sum);
        }
        
        cout << max_sum << '\n';
    }
    return 0;
}
```
Kadane 算法本质上就是一维数组的动态规划（DP）降维版。它彻底干掉了两层 for 循环，把暴力枚举的时间复杂度拉回了绝对的线性级别 O(N)。以后只要在题目里看到“连续（子段/子数组）”和“极值（最大/最小和）”这两个词同时出现，并且数组里有正有负，第一时间想到这个模板

# P12889 [蓝桥杯 2025 国 Java B] 情绪链路

## 题目描述

在数字社交媒体的浩瀚世界中，运营者小蓝负责维护一条情绪链路。这条链路由 $n$ 个用户节点依次排列而成，每个节点上记录着一个情绪值。具体地，第 $i$ 个节点的情绪值为 $a_i$，其中 $a_i$ 是一个整数，可能为正，也可能为负。

为了改善整体情绪氛围，小蓝购买了一种名为“情绪放大器”的工具。该工具允许他选择一段**至少包含一个用户节点的连续区间**，并将这个区间内所有用户节点的情绪值都乘以一个整数 $k$。只是，工具启动成本高昂，小蓝只能使用它一次。

现在，请你帮助小蓝计算，在经过这样一次操作后（一定要操作），所有用户节点的情绪值之和最大会是多少。

## 输入格式

第一行包含两个整数 $n$ 和 $k$，分别表示情绪链路的长度和放大器的倍数。

第二行包含 $n$ 个整数 $a_1, a_2, \ldots, a_n$，表示每个用户节点的情绪值。

## 输出格式

输出一行，包含一个整数，表示经过一次操作后，所有用户节点情绪值之和的最大可能值。

## 输入输出样例 #1

### 输入 #1

```
5 2
-1 2 -3 4 -5
```

### 输出 #1

```
1
```

## 说明/提示

**【样例说明】**

最优的做法是选择区间 $[4]$ 并使用工具。使用后这 $n$ 个用户节点的情绪值依次为 $[-1, 2, -3, 8, -5]$，总和为 $1$。

**【评测用例规模与约定】**

对于 $30\%$ 的评测用例，$2 \leq n \leq 10^3$，$1 \leq k \leq 10^3$，$-10^3 \leq a_i \leq 10^3$。

对于 $100\%$ 的评测用例，$2 \leq n \leq 10^5$，$1 \leq k \leq 10^5$，$-10^5 \leq a_i \leq 10^5$。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int N = 1e5+9;
ll a[N];//数组也开Ll 
ll ans;
int main()
{
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	ll n,k;cin >> n >> k;
	ll sum = 0;
	for(int i = 1;i <= n;++i)
	{
		cin >> a[i];
		sum += a[i];
	}
	
	ll cu_team = a[1];
	ll max_sum = a[1];
	for(int i = 2;i <= n;++i)
	{
		cu_team = max(cu_team+a[i],a[i]);//注意只要不是负担 所以比的是加上前后 
		 max_sum = max(max_sum,cu_team);
	}
	
	ans = sum + (k-1)*max_sum;
	cout << ans <<'\n';
	
	return 0;
}
 

```
