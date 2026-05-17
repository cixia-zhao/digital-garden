---
title: string
tags:
  - 语法
related:
  - substr
date: 2026-01-21
---

---

# 🧵 C++ `std::string` 

## 一、 基础概念：C 语言风格字符数组 vs C++ `string`

在深入 C++ 之前，必须理清底层关于字符串的两种核心演变：

### 1. C 语言风格的字符串

- **本质**：是一组字符，必须借由**字符数组**来存储。
    
- **核心红线**：必须以 `'\0'`（空字符）作为结束标志。
    
- **远古初始化方式**：
    
    
    
    ```C++
    char arr[] = {'a', 'b', 'c', '\0'}; // 字符数组，远古已有的初始化方式，必须手动加 '\0'
    char str[] = "hello world";         // 如果是这种初始化方式，字符数组会默认在末尾追加 '\0'
    ```
    
- **C 语言标准库函数（需引入 `<string.h>`）**：
    
    - `strlen(str)`：计算字符串长度，**计数不包括 `\0`**。
        
    - `strcmp(a, b)`：比较两个字符数组的大小。若 `a > b` 返回 `1`；若 `a < b` 返回 `-1`；若相等则返回 `0`。
        
    - `strcpy(a, b)`：拷贝函数。**b 的内容完完全全把 a 变成 b 的内容，即便 a 比 b 长**。
        
    - `strcat(a, b)`：拼接函数。**把 b 连接到 a 的后面**。
        

### 2. C++ 风格的字符串

- **本质**：引入了头文件 `<string>` 后，它成为了一个**全新的数据类型 `string`**。
    
- **白话优势**：C++ 的 `string` 实例大小判断可以直接用**白话 `if()` 语句**（操作符重载）来直接判断，不再需要借助复杂的 C 库函数。
    

### 3. 相互转换

- **字符数组转 `string`**：
    
    
    
    ```C++
    char hh[] = "hhhhh";
    string ssss = hh; // 字符数组可以直接隐式转变为 string 类型
    ```
    

---

## 二、 `string` 的声明与多样化初始化方式

C++ 提供了极其丰富的构造函数来初始化一个字符串：


```C++

#include <iostream>
#include <string>
using namespace std;

int main() {
    string str1;                         // 声明并初始化一个空字符串
    string str2 = "Hello, World!";       // 使用字符串字面量初始化
    string arr = "hello world";          // 基础直接赋值
    string str3 = str2;                  // 使用另一个 string 对象进行拷贝初始化
    
    // 使用部分字符串初始化（利用 substr 截取）
    string str4 = str2.substr(0, 5);     // 格式：substr(起始位置, 长度) -> 得到 "Hello"
    
    // 使用 C 风格字符数组初始化
    const char* charArray = "Hello"; 
    string str5(charArray);              
    
    // 使用重复字符初始化
    string s(5, 'a');                    // 格式：string(个数, 字符) -> 得到 "aaaaa"
    string str6(5, 'A');                 // 得到 "AAAAA"
    
    string s1("three");                  // 直接传入字面量构造
}
```

---

## 三、 📥 输入与输出特殊技巧 (I/O 进阶)

### 1. 读入带空格的字符串

普通的 `cin >> str1;` 遇到空格、输入法空格或换行就会发生截断。如果需要读入整行（包含空格的字符串），必须使用 `getline`：



```C++
getline(cin, str); // 读入整行，包含空格字符串，这样就可以输入空格了
```

### 2. 高速 I/O 与 `printf` 兼容红线

在写算法竞赛或高性能代码时，经常会加入输入输出流解绑优化。但在 C++ 中，`std::string` 如果要配合 C 语言的 `printf` 输出，必须调用其成员函数 **`.c_str()`**：

- **`.c_str()` 的作用**：返回一个指向以空字符结尾的 C 风格字符串（即 `const char*` 类型）。
    
- **原因**：在进行 `printf` 输出时，**必须将 `string` 转换为 C 风格字符数组进行输出**。
    


```C++
#include <iostream>
#include <string>
#include <cstdio>

using namespace std;

int main() {
    // 高速 I/O 优化
    ios::sync_with_stdio(false); 
    cin.tie(nullptr); 
    cout.tie(nullptr);

    char buf[10];
    scanf("%s", buf);
    printf("%s\n", buf);

    // string 配合 printf 输出的正确姿势
    string str = "hello"; 
    printf("%s\n", str.c_str()); // 必须通过 .c_str() 转换
    
    return 0;
}
```

---

## 四、 🛠️ `string` 核心操作与常用 API 详解

### 1. 获取字符串长度 (length / size)

`.length()` 和 `.size()` 没有任何区别，完全等价。

```C++
std::string str = "Hello, World!"; 
int length = str.length(); // 或者 int length = str.size();
// 对于 "Hello, World!"，其长度为 13
std::cout << "Length: " << length << std::endl;
```

### 2. 拼接字符串 (`+` 或 `append`)

- **使用 `+` 运算符**：
    
    C++
    
    ```
    string a = "hello "; 
    a = "pre" + a + "world"; // 拼接 strcat 字符串的拼接 + 号 -> "prehello world"
    ```
    
- **使用 `append()` 函数**：
    
    ```C++
    std::string str1 = "Hello";
    std::string str2 = "World!";
    std::string result1 = str1 + ", " + str2;
    std::string result2 = str1.append(", ").append(str2); // 链式调用 append 函数
    ```
    

### 3. 提取子字符串 (`substr`)

- **核心参数规则**：`substr` 的参数对应的永远是 **`(起始位置, 长度)`**。注：千万注意不要越界。
    
- **两种常用形式**：
    
    1. `.substr(pos)`：从位置 `pos` 开始，**一直截取到字符串末尾**。
        
    2. `.substr(pos, count)`：从位置 `pos` 开始，**截取固定 `count` 个字符**。
        
- **示例**：
    
    
    
    ```C++
    std::string str = "Hello, World!";
    std::string subStr = str.substr(7, 5); // 从下标 7("W") 开始截取 5 个字符 -> "World"
    ```
    

### 4. 字符串删除 (`erase`)

- **核心参数规则**：`.erase(字符串下标作为起始位置, 长度)`
    
- **示例**：
    
    ```C++
    std::string s = "abcdefg";
    s.erase(2, 3); // 从索引 2（即 'c'）开始，往后抹除 3 个字符 -> 结果变为 "abfg"
    ```
    

### 5. 字符串查找 (`find`)

```C++
std::string str = "Hello, World";
size_t pos = str.find("World"); // 查找子字符串的位置并返回首字母下标

// 💡 核心考点：如果查找不到，函数会返回一个特殊的标记常量：std::string::npos (底层通常代表 -1)
if (pos != std::string::npos) {
    std::cout << "Substring found at position: " << pos << std::endl;
} else {
    std::cout << "Substring not found." << std::endl;
}
```

### 6. 字符串替换 (`replace`)

- **形式一：基础替换 `(起始位置, 长度, 新字符串)`**
    
    
    
    ```C++
    std::string str = "Hello, World!";
    str.replace(7, 5, "Universe"); // 从位置 7 开始，把长度为 5 的子串替换为 "Universe" -> "Hello, Universe!"
    ```
    
- **形式二：高级局部替换**
    
    - **参数规则**：`.replace(下标作为起始位置, 长度, 替换的数据源, 数据源的起始下标, 拿取数据源的长度)`
        
    - **经典用例**：
        
        ```C++
        // 假设原串为 "123456"，对其执行如下操作：
        str.replace(2, 3, "ABCD", 2, 2); 
        // 解析：
        // 1. 锁定了原串中下标为 2 开始、长度为 3 的片段（即 "345" 被挖空）
        // 2. 从数据源 "ABCD" 中，提取出从下标 2 开始、长度为 2 的子串（即 "CD"）
        // 3. 将 "CD" 补入挖空的位置
        // 4. 最终拼接结果为： "12" + "CD" + "6" -> "12CD6"
        ```
        

---

## 五、 ⚖️ 字符串比较与字典序法则 (Compare)

C++ `string` 内部重载了不等号，所以你可以直接使用 `s1 < s2` 的方式来比较 `string` 的大小。

### 1. 字典序比较的铁律

- 比较的规则是**按照字典序大小**进行比较。
    
- 字典序的比较方法是**从小到大一个一个字符进行垂直对比，一旦遇到不相等的字符就立刻确定大小关系**，后续字符再长再大也无法逆转关系。
    
- 如果前缀完全一样，但其中一个串先结束了，则**短的更小**。
    

### 2. 经典实例解析

- `aaaa < bbbb` （首位 `a` < `b` 决定）
    
- `azz < baaa` （虽然 `z` 很大，但在第一位 `a` < `b` 时，胜负已分）
    
- `azzzzzzzzzzzz < b` （依然由第一位 `a` < `b` 决定，不拘泥于长度）
    
- `lanqiao == lanqiao` （完全相等）
    

### 3. `.compare()` 成员函数写法

```C++
std::string str1 = "Hello";
std::string str2 = "World";
int result = str1.compare(str2); // 垂直对比

if (result == 0) {
    std::cout << "Strings are equal." << endl;
} else if (result < 0) {
    std::cout << "String 1 is less than String 2." << endl; // 因为 'H' < 'W'，所以进入此分支
} else {
    std::cout << "String 1 is greater than String 2." << endl;
}
```

---

## 六、 🧩 算法实战拓展：判断两个字符串的衔接最大重合长度

这是一个非常经典的算法题逻辑（常用于字符串接龙、单词拼盘等场景）：

```C++
// 🧠 虚空专家思维：看看单词 a 的尾巴，有单词 b 的头，能不能接上？
// 如果能接上，返回重合部分的长度；如果完全接不上，则返回 0。
int get_overlap(string a, string b) {
    // 重合部分的长度不可能超过任意一个单词自身的长度
    int min_len = min(a.length(), b.length());
    
    // 重合部分必须小于两个单词的自身长度（不然设定不包含全包含）
    for (int k = 1; k < min_len; k++) {
        // a.substr(起始位置) -> 动态截取单词 a 的“尾巴”
        // b.substr(0, k)     -> 动态截取单词 b 的“开头”
        if (a.substr(a.length() - k) == b.substr(0, k)) {
            return k; // 从小到大找，找到第一个就是最短的！直接返回！
        }
    }
    return 0; // 遍历完找不到重合部分，说明接不上
}
```

---

## 七、 🗃️ 核心法则：`string 数组` 的多维深度理解

C++ `string` 数组的核心法则可以深度总结为以下三个经典规律：

### 1. 本质：两层嵌套的“收纳盒”

`string` 数组不仅是一个存放了多段文本的列表。因为文本（字符串）本身也是由一个个具体的字符/数字组合而成的，所以它天然自带“二维”属性：

- **外层**：装着多个字符串的超大数组（大盒子）。
    
- **内层**：装着具体字符的小数组（小盒子，由字符本身构成）。
    

### 2. 定位秘籍：方括号 `[]` 的用法

记住核心口诀：**“先抓大件，再找小件，并且永远从 0 开始数”**。

|**代码写法**|**作用**|**提取出的具体类型**|**对应层级举例参考**|
|---|---|---|---|
|**单方括号 `[i]`**|抽取出第 `i+1` 个**完整的字符串**|字符串 (`string`)|`arr[0]` 顺利拿到首行整个二进制串 `"1111110"`|
|**双方括号 `[i][j]`**|抽取出该字符串里的第 `j+1` 个**具体字符**|单个字符 (`char`)|`arr[0][0]` 精准拿到最左上角的单个字符 `'1'`|

### 3. 安全红线：绝不越界

- **总数减一**：如果你的大数组里一共存了 `10` 个字符串，你外层最多只能查到 `[9]`。
    
- **长度减一**：如果某个具体字符串的长度是 `7`，你内层最多只能查到 `[6]`。
    
- **越界警告**：试图跨域越界（比如字符串长度只有 7，你却去查 `arr[0][7]`）就是强行去了不属于你的内存硬盘空间，**程序极大概率会直接崩溃报运行时错误**！