# WorldTamerCNTr

World Tamer 简体中文汉化补丁 by Lenten

> **本仓库只存放发布信息与授权说明，不含汉化文件。**
> 请到 [**Releases**](../../releases) 页面下载，不要点 Code → Download ZIP。

对应游戏版本：**0.43.0**

---

## 下载

两个文件都在同一个 Release 的 Assets 里，认文件名里的 **`Smooth`**（流畅）和 **`Deep`**（深度）。

| 版本 | 特点 | 文件 |
| --- | --- | --- |
| **流畅翻译**<br>（正式版，推荐） | 只替换文本，未改菜单界面，理论上没有 bug | **[WorldTamer-ZH-v0.43.0-Smooth.zip](https://github.com/coten73/WorldTamerCNTr/releases/download/v0.43.0-zh/WorldTamer-ZH-v0.43.0-Smooth.zip)**<br>1.73 MB |
| **深度翻译**<br>（实验性） | 额外修改了菜单界面，**bug 数量与严重性未知，介意勿用** | **[WorldTamer-ZH-v0.43.0-Deep.zip](https://github.com/coten73/WorldTamerCNTr/releases/download/v0.43.0-zh/WorldTamer-ZH-v0.43.0-Deep.zip)**<br>21.9 MB |

两者文本内容基本一致，**选一个装即可，不要同时装两个**。

也可以直接进 [Releases 页面](https://github.com/coten73/WorldTamerCNTr/releases/tag/v0.43.0-zh)，
在最下面的 Assets 里下载。

> 文件名带版本号，所以上面的直链在换版本后会失效。
> 如果打不开，请到 [Releases](https://github.com/coten73/WorldTamerCNTr/releases) 拿最新版。

## 安装

1. 下载并解压 zip
2. 把里面的 `chinese_simp` 文件夹整个复制到游戏的 `game/tl/` 目录下
   （最终路径应为 `游戏目录/game/tl/chinese_simp/`）
3. 启动游戏，在Language选择里选「CN旗」

如果 `game/tl/` 下已经有旧的 `chinese_simp`，**先删掉再复制**。

**安卓版**：因为涉及重新签名，暂时不适用。请等开发者把汉化编译进下个版本的安装包，
或者自行编译。

## 两个版本的区别

| | 流畅翻译 | 深度翻译 |
| --- | --- | --- |
| 菜单界面 | 未修改 | 有修改 |
| 稳定性 | 理论上没有 bug | bug 数量与严重性未知 |
| 自带字体 | 无（用游戏本体内置的 Noto Sans SC） | 有（Noto Serif CJK SC Bold，约 25 MB） |

## 已知问题

- **切换别的语言后文字错乱** → 改一下游戏内时间（例如睡一觉）刷新即可
- **部分文本流畅度待优化**

## 出问题了怎么办

1. 退出游戏，删掉 `game/tl/chinese_simp` 整个文件夹
2. 换成另一个版本试试
3. 还有问题请到 `vx.kong@qq.com` 反馈，**请附截图**，并说明：
   - 游戏版本号
   - 用的是哪个版本（流畅 / 深度）
   - 问题出现在哪个界面
   - 注意标注来意

尽量优先发到邮箱而不是 [Issues](../../issues)，后者我不怎么会及时查看。

---

## 授权范围

本汉化补丁包含多种来源的内容，适用**不同**的授权条款。

### 一、译者原创内容

包括全部翻译文本，以及 `forcechange.rpy`、`replace_cn.rpy`、`name.rpy` 等脚本。

采用 **CC BY-NC-SA 4.0（署名 - 非商业性使用 - 相同方式共享 4.0 国际）** 授权。

- 协议全文见本仓库根目录 [`LICENSE`](LICENSE)，发布包内也附有一份
- 允许自由转载、修改、分发，但**必须署名**、**不得商用**、**派生作品须沿用同一协议**

### 二、第三方内容（**不在**上述授权范围内）

**Noto Serif CJK SC Bold** —— 仅「深度翻译」版附带

| 项目 | 内容 |
| --- | --- |
| 文件 | 发布包内 `chinese_simp/NotoSerifCJKsc-Bold.otf` |
| 版权 | © 2017-2024 Adobe (<http://www.adobe.com/>) |
| 商标 | Noto is a trademark of Google Inc. |
| 许可 | **SIL Open Font License 1.1** |

该字体**仅**依 SIL Open Font License 1.1 分发，**不适用**本仓库的 `LICENSE`。
协议全文与完整声明见发布包内 `chinese_simp/OFL.txt` 与 `chinese_simp/FONT-NOTICE.txt`，
**这两份必须和字体放在一起保留，不得单独删除**。

**Ren'Py** —— `common.rpy` 由引擎翻译系统生成

| 项目 | 内容 |
| --- | --- |
| 来源 | Ren'Py 的翻译生成功能，从 MIT 授权的 `renpy/common/` 生成 |
| 版权 | Copyright 2004-2026 Tom Rothamel `<pytom@bishoujo.us>` |
| 许可 | MIT License |

全文见 [`RENPY-LICENSE.txt`](RENPY-LICENSE.txt)。

完整汇总见 [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md)。

### 三、与原作的关系

本补丁是**非官方的玩家汉化**，与原作作者无任何隶属关系，也未获得其背书。

原作游戏的文本、图像、音频等一切内容的版权均归原作者所有。
**本仓库与发布包只包含译者原创的翻译内容，以及上述第三方字体**，
不包含原作的任何资源文件。

使用本补丁需要自行拥有**原版游戏本体**。
