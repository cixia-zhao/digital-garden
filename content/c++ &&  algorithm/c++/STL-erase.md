C++中，erase 函数用于从容器（如 vector, list, deque, map, set 等）中移除元素。下面是几种常见容器中使用 erase 的示例。

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};

    // 删除单个元素，例如删除值为3的元素
    auto it = std::find(vec.begin(), vec.end(), 3);
    if (it != vec.end()) {
        vec.erase(it);
    }

    // 删除指定位置的元素，例如删除第一个元素
    vec.erase(vec.begin());

    // 删除一系列元素，例如删除第二个到第四个元素
    vec.erase(vec.begin() + 1, vec.begin() + 3);

    for (const int& value : vec) {
        std::cout << value << " ";
    }
    return 0;
}
```


