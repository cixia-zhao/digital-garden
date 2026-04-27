## 这页是怎么“设计出来”的（按模块拆开讲）

### 1) 为什么是“单文件 HTML + 内嵌 CSS/JS”
- **浏览器直接打开就能跑**：HTML 里放 `<style>` 和 `<script>`，不需要构建工具。
- **Web Bluetooth 的限制**：它是浏览器能力，不是普通网页 JS 库；用最少文件能减少部署/路径问题。

### 2) UI/交互为什么这么安排（按钮、输入框、状态区）
- **两步流程**：先“连接”，再“同步”。这是 BLE 的真实工作流：先建立 GATT 连接、拿到特征值句柄，才能写入。
- **状态区（statusBox）**是关键：蓝牙出错时用户很容易“什么都没发生”。把每一步（请求权限→连接→发现服务→写入）写出来，能快速定位失败点。
- **断开按钮**：BLE 连接不稳定、且调试时经常要重连；手动断开比刷新页面更可控。

### 3) 蓝牙部分的核心知识点（Web Bluetooth / GATT）
- **Web Bluetooth API**的典型流程：
  - `navigator.bluetooth.requestDevice(...)`：弹出设备选择器（浏览器强制要求用户手动选择，不能静默扫描）
  - `device.gatt.connect()`：连接 GATT Server
  - `server.getPrimaryService(serviceUuid)`：拿到服务
  - `service.getCharacteristic(charUuid)`：拿到特征值
  - `characteristic.writeValue(...)` / `writeValueWithoutResponse(...)`：写入数据
- **为什么要 filter**
  - `filters: [{ name: "FocusCore_BLE" }, { services: [uuid] }]`：减少用户选错设备，也让浏览器更快定位目标设备。
  - 你后来给了固定的 Service/Characteristic UUID，所以我把它们固化，连接时默认就能走“精确发现”。

### 4) 为什么要处理断连、拒绝权限等“容错”
- **用户拒绝权限**是常态：`requestDevice` 很容易被取消或拒绝，所以要捕获异常并转成人话提示。
- **设备会断开**是 BLE 常态：走远、省电、固件重启都会断。`gattserverdisconnected` 事件就是专门给这个场景的——收到后必须把 `server/writeCharacteristic` 清空，否则你以为还连着，写入会报奇怪错误。

### 5) 文本如何变成 ESP32 能收的字节（编码/拼接）
- **你要的协议**：多行待办 → 用 `|` 拼成一行字符串。
- **为什么用 `TextEncoder()`**
  - BLE 写入需要的是 **字节**（`Uint8Array`），不是 JS 字符串。
  - `TextEncoder` 会把 JS 字符串按 **UTF‑8** 编成字节数组，ESP32 端也很容易按 UTF‑8 还原。
- **为什么要去掉空行/trim**
  - 手机上的输入常带空行、末尾换行；如果不处理，设备端解析会多出空待办。

### 6) CSS 为什么看起来“现代、手机友好”
- **viewport**：`<meta name="viewport" ...>` 让手机按设备宽度渲染。
- **大字号 + 大按钮**：移动端点按更容易，不会误触。
- **响应式布局**：窄屏一列、宽屏两列（CSS media query），手机和电脑都好用。
- **配色跟随系统深浅色**：`prefers-color-scheme` 让深色/浅色都不刺眼。

### 7) 我做“固化默认 UUID”的思路
- 你给了最终标准 UUID 后，我做了两件事：
  - **常量默认值**：`DEFAULT_MEMO_SERVICE_UUID` / `DEFAULT_MEMO_CHARACTERISTIC_UUID`
  - **自动填入 + 自动使用**：页面加载就填输入框；连接时如果用户留空，也用默认值计算出 `effectiveServiceUuid/effectiveCharUuid`，保证“点连接就能用”。

---

## 你以后自己写类似页面，可以记住的“口诀”
- **BLE 三件套**：选设备（requestDevice）→ 连 GATT（connect）→ 找特征值（getService+getCharacteristic）
- **写入前两件事**：把数据变成 `Uint8Array`（TextEncoder）→ 处理断连/取消权限的异常
- **移动端三件套**：viewport、按钮够大、状态提示够清楚

## 代码讲解版（按“你要做什么”来读）

下面我按这页 `index.html` 里的 JS 结构，从上到下把每个函数的“目的、输入输出、关键点”讲清楚。你以后自己改协议/改 UUID/加分包，都可以照这个思路扩展。

### 1) 常量与全局变量：把“可变”和“不可变”分开

你会看到这些常量（不可变配置）：

- **`DEFAULT_DEVICE_NAME`**：用来在设备选择器里尽量过滤到你的 ESP32（避免选错）
- **`DEFAULT_MEMO_SERVICE_UUID` / `DEFAULT_MEMO_CHARACTERISTIC_UUID`**：你给的 UUID，固化为默认值

你会看到这些全局状态（连接过程中会变化）：

- **`device`**：用户在浏览器选择的蓝牙设备对象
- **`server`**：`device.gatt.connect()` 后得到的 GATT Server
- **`writeCharacteristic`**：最终要写入的特征值句柄（有了它才能 `writeValue`）

这是一种很常见的“状态机”写法：  
未连接时这三个是 `null`；连接成功后它们分别变成非空；断开后再清空。

---

## 2) DOM 元素引用：把 UI 当成“输入输出设备”

这几行：

- `elServiceUuid / elCharUuid / elTodos`：用户输入
- `btnConnect / btnDisconnect / btnSync / btnClear`：触发动作
- `connDot / connText / statusBox`：反馈状态

**核心思想**：网页就是一个小程序，“输入框+按钮”是输入，“状态区+连接徽标”是输出。

---

## 3) UI 小函数：只负责显示，不负责业务

### `setStatus(message)`
- **作用**：把文本写到状态框 `statusBox`
- **为什么要有它**：你不想在业务逻辑里到处写 `statusBox.textContent = ...`，封装后更清爽

### `setConnectedUI(isConnected, extra)`
- **作用**：连接成功时，把“连接徽标变绿”、按钮状态切换成“可以断开/可以同步”
- **本质**：根据连接状态去启用/禁用按钮，这是防呆（避免没连接就点同步）

### `setDisconnectedUI(reason)`
- **作用**：断开或失败时，把“连接徽标变红”、按钮状态回到“可以连接但不能同步”

你以后加“自动重连/重试次数”也建议仍然用这三个函数管 UI，不要把 UI 状态散落在各处。

---

## 4) 数据处理：把“人类输入”变成“协议字符串”

### `normalizeUuidLike(value)`
- **作用**：把用户输入的 UUID 去空格、转小写
- **意义**：避免用户复制时带了空格/大小写混乱导致找不到服务

### `buildPayloadFromTextarea()`
- **输入**：`textarea` 里的多行字符串
- **处理**：
  - `split(/\r?\n/)`：兼容 Windows 换行
  - `trim()`：去掉每行左右空格
  - `filter(Boolean)`：去掉空行
  - `join("|")`：按你的协议拼成单行
- **输出**：`{ joined, linesCount }`

这是把“UI数据”变成“业务数据”的典型边界函数。你未来要换分隔符、要加编号、要加校验和，就改这里最合适。

---

## 5) 环境检查：Web Bluetooth 的“硬门槛”

### `assertWebBluetoothAvailable()`
它做两件事：

1. **浏览器能力检查**：`"bluetooth" in navigator`  
   - 没有就提示去用 Chrome/Edge
2. **安全上下文检查**：必须 HTTPS 或 localhost  
   - 因为 Web Bluetooth 属于高权限 API，浏览器不允许普通 `file://` 或不安全 http 页面随便调用

这就是为什么很多人“复制一份 html 双击打开”会失败：不是代码错，是浏览器安全策略。

---

## 6) 连接流程：从“选择设备”到“拿到可写特征值”

### `connect()` 是整页的核心

你可以按顺序理解它（这是 BLE 的标准链路）：

#### A. 取用户输入 + 计算“最终要用的 UUID”
- 读输入框的 `serviceUuid/charUuid`
- 计算 `effectiveServiceUuid/effectiveCharUuid`
  - 如果用户没填，就用默认 UUID
- **回填输入框**
  - 这样 UI 上看到的就是实际正在使用的 UUID，避免“明明用默认值但输入框是空的”造成困惑

#### B. 请求设备权限（会弹浏览器选择器）
- `navigator.bluetooth.requestDevice({ filters, optionalServices })`
- filters 里用了：
  - `{ services: [effectiveServiceUuid] }`：按服务过滤（很关键）
  - `{ name: DEFAULT_DEVICE_NAME }`：按名称过滤（辅助）
- 这一步最常见的异常：
  - 用户点取消 → `NotFoundError`
  - 用户拒绝权限 → `NotAllowedError`

#### C. 监听断开事件（非常重要）
- `device.addEventListener("gattserverdisconnected", ...)`
- 一旦断开：
  - 清空 `server/writeCharacteristic`
  - UI 变成断开状态
  - 状态区提示“请重新连接”

**为什么要清空**：不清空的话，你可能还拿着旧 characteristic 去写，报错会很难读。

#### D. 连接 GATT
- `server = await device.gatt.connect()`

#### E. 发现服务和特征值
- `service = await server.getPrimaryService(effectiveServiceUuid)`
- `writeCharacteristic = await service.getCharacteristic(effectiveCharUuid)`

拿到 `writeCharacteristic` 后，才算“你已经找到了设备里那个邮箱地址”，后面写入就是往这个地址投递数据。

#### F. 检查是否可写
- 看 `properties.write` 或 `properties.writeWithoutResponse`
- 如果两者都不支持，就直接报错（否则你写的时候才会失败）

---

## 7) 同步流程：把字符串编码成字节，然后写入

### `syncTodos()`

#### A. 确认已连接
- 没有 `writeCharacteristic` 就直接 throw

#### B. 构造 payload（协议字符串）
- 调 `buildPayloadFromTextarea()`
- joined 为空则提示“待办为空”

#### C. UTF-8 编码
- `const data = new TextEncoder().encode(joined)`
- 得到 `Uint8Array`，里面是 UTF‑8 字节序列

#### D. 写入特征值
- 如果设备支持 `writeWithoutResponse` 就用它（通常更快、少一次确认）
- 否则用 `writeValue`（带响应确认）

#### E. 状态区输出写入信息
- 条目数、字节数、最终拼接内容

---

## 8) 断开流程：把状态机复位

### `disconnect()`
- 如果 `device.gatt.connected` 就 `disconnect()`
- 清空 `server/writeCharacteristic`
- UI/状态回到未连接

---

## 9) 错误“翻译成人话”

### `humanizeError(err)`
把常见的浏览器异常 name 映射成更友好的中文提示，比如：

- `NotFoundError`：用户取消选择
- `SecurityError`：非 https/localhost 等安全限制
- `NotAllowedError`：拒绝权限或策略阻止

这属于“产品化”思路：工程上错误不是给开发者看的，是给用户看的。

---

## 10) 事件绑定：把按钮点击连到函数上

- 连接按钮 → `connect()`
- 同步按钮 → `syncTodos()`
- 断开按钮 → `disconnect()`
- 清空按钮 → 清空文本框 + 状态提示

并且每个按钮点击都用了 `try/catch/finally`：
- **try**：执行主流程
- **catch**：把错误显示到状态区
- **finally**：把按钮 disabled 状态恢复到合理值（防止卡死）

---

## 你下一步“学会修改”的两个练习（最有用）

### 练习 A：改协议分隔符
现在是 `|`，你要改成 `\n` 或 `;`，只改 `buildPayloadFromTextarea()` 里 `join("|")` 那一行就行。

### 练习 B：加一个“最大长度限制”
BLE 单次写入可能有 MTU/栈限制。你可以在 `syncTodos()` 里加：

- 如果 `data.byteLength` 超过某个阈值，就提示“内容太长，请减少待办或分批同步”

（如果你告诉我 ESP32 端一次最多接收多少字节，我可以直接把这个限制和分包写好。）

---

如果你愿意继续深入：把你 ESP32 端接收特征值写入的那段代码（比如 NimBLE 的 `gatt_svr_chr_access` 回调）贴出来，我可以用同样的“讲解版”把设备端怎么解析 `|`、怎么处理 UTF‑8、怎么处理分包/多次写入也讲清楚，并把网页端升级成“自动分包发送”。
