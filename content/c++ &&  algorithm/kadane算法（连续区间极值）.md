

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
Kadane 算法本质上就是一维数组的动态规划（DP）降维版。它彻底干掉了两层 for 循环，把暴力枚举的时间复杂度拉回了绝对的线性级别 O(N)。以后只要在题目里看到“连续（子段/子数组）”和“极值（最大/最小和）”这两个词同时出现，并且数组里有正有负**，第一时间想到这个模板
