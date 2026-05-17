
1. 什么是 pair？（双黄蛋模型）
pair 在英文里就是“一对、一双”的意思。
你可以把它当成一个只有左右两个口袋的小背包，或者一个双黄蛋。它最牛的地方在于：这两个口袋里可以装完全不同类型的数据！
2. 怎么声明

格式极其简单：pair<左口袋类型, 右口袋类型> 名字;
pair<int, int> p1;       // 左右都装整数（最常见，比如图纸上的坐标 x, y）
pair<int, string> p2;    // 左边装分数，右边装人名
pair<double, char> p3;   // 左边装小数，右边装字母

3. 怎么往里塞东西？（打包）
在现代 C++（C++11 及以后）中，最简单粗暴、最优雅的方法就是直接用大括号 {} 打包填入：
p1 = {2022, 6};
p2 = {100, "Lanqiao"};

注：你可能在学校老教材上看到过 make_pair(2022, 6)
4. 怎么把东西掏出来？（解包）
pair 字典里只有两个专属的“取件码”，直白到令人发指：
 * .first：掏出左口袋的“老大”。
 * .second：掏出右口袋的“小弟”。
cout << p2.first;  // 打印出 100
cout << p2.second; // 打印出 Lanqiao


当你把一堆 pair 塞进 vector 里并调用 sort() 时，它自带一套极其完美的**“双重排序法则”**，完全不需要你手写复杂的比较规则：
 * 第一准则（先拼爹）：优先比较所有的左口袋 .first，从小到大排。
 * 第二准则（爹一样，拼自己）：如果两个元素的 .first 完完全全相等，它会自动去比较右口袋 .second，依然从小到大排。
👉 纯享版实战场景：
假设你的 vector 里装了三个 pair：{3, 100}，{1, 50}，{1, 20}。
你啥也不用管，直接一行代码：sort(v.begin(), v.end());
排完序后，里面的元素会自动变成：
 * {1, 20} （老大是 1，虽然跟下面那位一样，但自己的小弟 20 更小，排最前）
 * {1, 50} （老大同样是 1，但小弟是 50，只能排第二）
 * {3, 100}（老大是 3，数值最大，直接被踢到垫底）
只要题目里出现以下这三种情况，直接掏出 vector<pair<...>>：
 * 二维平面找点：pair<int, int> 完美存储 (x, y) 坐标。
 * 带“前世记忆”的排序（就像刚做的那道题）：pair<排序特征, 原始肉身下标>。特征放左边当老大，用来排序；肉身放右边当小弟，排完序后还能认得出是谁。
 * 时间线/区间覆盖题：pair<开始时间, 结束时间>。

没问题，针对这几张关于 `std::pair` 的补充笔记，我帮你去掉了繁杂的连线和涂鸦，用更结构化、循序渐进的方式重新梳理一遍。把“红线”表达的逻辑直接变成了清晰的代码注释。

---

## 🤝 补充：`std::pair` 核心用法与嵌套结构

**概念**：`pair` 是 C++ 标准库 `<utility>` 中的一个模板类，它的作用非常纯粹——**将两个任意类型的数据组合成一个整体**。它也是我们前面学过的 `map` 容器底层存储键值对的基本单元。

### 📊 `pair` 常用形式速查表

|**代码形式**|**功能解释**|
|---|---|
|`pair<T1, T2> p1;`|创建一个空的 `pair` 对象，两个元素分别采用 `T1` 和 `T2` 类型的默认值初始化。|
|`pair<T1, T2> p1(v1, v2);`|创建并初始化对象。`first` 成员初始化为 `v1`，`second` 成员初始化为 `v2`。|
|`make_pair(v1, v2);`|**极力推荐的快捷方式**：直接根据传入的 `v1` 和 `v2` 自动推导类型并创建一个新的 `pair`。|
|`p1 < p2;`|大小比较（遵循字典序）：先比较 `.first`，如果相等，再比较 `.second`。|
|`p1 == p2;`|相等比较：只有当两个对象的 `first` 和 `second` 都分别相等时才返回 true。|
|`p1.first`|访问并返回 `pair` 中的**第一个**数据成员。|
|`p1.second`|访问并返回 `pair` 中的**第二个**数据成员。|

---

### 💻 1. 基础使用示例

最常见的用法是把两个不同类型的值绑定在一起，然后通过 `.first` 和 `.second` 提取它们。



```C++
#include <iostream>
#include <utility> // pair 需要引入此头文件
#include <string>

using namespace std;

int main() {
    // 显式指定类型来创建 pair
    pair<int, double> p1(1, 3.14);
    pair<char, string> p2('a', "hello");

    // 访问内部数据
    cout << p1.first << ", " << p1.second << endl; // 输出: 1, 3.14
    cout << p2.first << ", " << p2.second << endl; // 输出: a, hello

    return 0;
}
```

---

### 🪆 2. 进阶：`pair` 的嵌套 (Nesting)

**核心思想**：`pair` 的本质是装两个数据的容器，那么它的 `first` 或 `second` 完全**可以装另一个 `pair`**。

通过这种“套娃”的方式，我们可以非常方便地组合 3 个、4 个甚至更多的数据，形成复杂的数据结构（比如三维坐标）。



```C++
#include <iostream>
#include <utility>

using namespace std;

int main() {
    // 【层级 1】：普通的两个值组合
    pair<int, int> p1(1, 2); 
    
    // 【层级 2】：三维坐标点 (x, y, z) 
    // 第1个维度是 int，第2、3个维度由内部嵌套的 pair 提供
    pair<int, pair<int, int>> p2(3, make_pair(4, 5));

    // 【层级 3】：四个值的组合 (两两嵌套)
    pair<pair<int, int>, pair<int, int>> p3(make_pair(6, 7), make_pair(8, 9));

    // ==========================================
    // 如何访问嵌套的数据？（就像剥洋葱一样一层层剥开）
    // ==========================================

    cout << "--- 访问 p2 (三个值) ---" << endl;
    cout << p2.first << endl;                 // 获取最外层的 first: 3
    cout << p2.second.first << endl;          // 深入 second 获取它的 first: 4
    cout << p2.second.second << endl;         // 深入 second 获取它的 second: 5

    cout << "--- 访问 p3 (四个值) ---" << endl;
    cout << p3.first.first << endl;           // 获取左边 pair 的 first: 6
    cout << p3.first.second << endl;          // 获取左边 pair 的 second: 7
    cout << p3.second.first << endl;          // 获取右边 pair 的 first: 8
    cout << p3.second.second << endl;         // 获取右边 pair 的 second: 9

    return 0;
}
```

**💡 优化建议总结**：

手写复杂的嵌套 `pair<int, pair<int, int>>` 会让代码变得很长。在实际工程中，如果数据超过两个，通常会更倾向于使用 `struct` (结构体) 或者 C++11 的 `std::tuple` (元组)，这样代码的可读性会更高。但掌握 `pair` 嵌套对理解底层逻辑（尤其是在做算法题时）非常有帮助。