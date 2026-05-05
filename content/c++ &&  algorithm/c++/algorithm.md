---
title:
tags:
related: []
date: 2026-02-07T16:16:00
---

### 🎯 核心功能 (Purpose)
> sort:
![Screenshot_2026-02-07-16-16-43-81_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-16-43-81_149003a2d400f6adb210d7e357a3a646.jpg)


若想改变顺序，则可利用sort的第三个参数，再通过回调函数（函数作为参数传参），来实现

![Screenshot_2026-02-07-16-19-59-43_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-19-59-43_149003a2d400f6adb210d7e357a3a646.jpg)
。
![Screenshot_2026-02-07-16-21-59-78_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-21-59-78_149003a2d400f6adb210d7e357a3a646.jpg)

_ _cd 最大公因数：
![Screenshot_2026-02-07-16-25-32-48_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-25-32-48_149003a2d400f6adb210d7e357a3a646.jpg)
long long __gcd(long long a, long long b) {
    return b ? __gcd(b, a % b) : a;
}

long long GCD(long long a, long long b) {
    while (b ^= a ^= b ^= a %= b);
    return a;
}

绝对值：
![Screenshot_2026-02-07-16-31-03-61_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-31-03-61_149003a2d400f6adb210d7e357a3a646.jpg)
reverse: 反转
![Screenshot_2026-02-07-16-34-44-05_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-34-44-05_149003a2d400f6adb210d7e357a3a646.jpg)
全排列 next_permutation :
![Screenshot_2026-02-07-16-38-01-68_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-38-01-68_149003a2d400f6adb210d7e357a3a646.jpg)

![Screenshot_2026-02-07-16-38-34-72_149003a2d400f6adb210d7e357a3a646](Screenshot_2026-02-07-16-38-34-72_149003a2d400f6adb210d7e357a3a646.jpg)


### ✍️ 标准语法 (Syntax)
```cpp
