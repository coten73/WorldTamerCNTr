# 第三方组件与许可 / Third-Party Notices

本翻译包（World Tamer 简体中文）包含或依赖以下第三方组件。
发布前请确认对应文件已随包分发。

---

## 1. Noto Serif CJK SC Bold（深度翻译版内随包分发）

| 项目 | 内容 |
| --- | --- |
| 文件 | `chinese_simp/NotoSerifCJKsc-Bold.otf` |
| 字体名 | Noto Serif CJK SC Bold |
| 版本 | Version 2.003 |
| 版权 | © 2017-2024 Adobe (http://www.adobe.com/) |
| 商标 | Noto is a trademark of Google Inc. |
| 上游 | <https://github.com/notofonts/noto-cjk> |
| 许可 | **SIL Open Font License 1.1** |
| 协议全文 | <https://scripts.sil.org/OFL> |
| LICENSE 文件 | 上游 `Serif/LICENSE` 或 `Sans/LICENSE`（**两份内容完全相同**，取哪份都行） |

**OFL 1.1 要求**：随包分发的每一份副本都必须附带版权声明和许可证全文。
因此 **`OFL.txt` 与 `FONT-NOTICE.txt` 必须和字体放在同一个目录里一起发布**，
不能只放在仓库根目录而后把字体单独打包。

📌 **注意区分**：上游的 `Serif/LICENSE` 与 `Sans/LICENSE` 两份文件**逐字相同**，
都只是 OFL 1.1 正文，**里面没有版权行、也没有声明保留字体名**。
真正有区别的是**字体文件内部 name 表**里内嵌的版权声明：

| 字体 | 内嵌版权声明行 |
| --- | --- |
| 本包分发的 `NotoSerifCJKsc-Bold.otf` | `© 2017-2024 Adobe (http://www.adobe.com/).`（无保留字体名） |
| 游戏自带的 `NotoSansSC/JP/KR-SemiBold.ttf` | `(c) 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'.` |

本包内的字体为原版未修改文件。若日后做子集化或任何修改，则该文件成为
Modified Version：Serif 那份没有保留字体名，OFL 层面不强制改名，但 `Noto` 是
Google 商标，修改版仍沿用有商标风险，建议改用自定义名称；若涉及游戏自带的黑体
（带 `Reserved Font Name 'Source'`），则修改版绝对不得沿用该名称。
无论哪种情况，都必须继续附带 `OFL.txt` 与版权声明。

---

## 2. Noto Sans SC / JP / KR SemiBold（**仅依赖，不随包分发**）

| 项目 | 内容 |
| --- | --- |
| 文件 | `fonts/NotoSansSC-SemiBold.ttf`、`NotoSansJP-SemiBold.ttf`、`fonts/NotoSansKR-SemiBold.ttf` |
| 位置 | 游戏本体的 `fonts.rpa` 内，属于原作发行内容 |
| 版权 | (c) 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. |
| 许可 | SIL Open Font License 1.1（LICENSE 文件与第 1 节相同，区别只在字体内嵌的版权声明行） |

本翻译包中的 `chinese_simp/style.rpy` 只是**引用**了游戏本体已带的
`fonts/NotoSansSC-SemiBold.ttf`（`流畅翻译` 版即依赖此方式显示中文），
并没有重新打包这个字体文件，因此**不需要**为它额外附带许可文本。

⚠️ 如果以后你把 `fonts.rpa` 或这些 ttf 一起打包进发布物，那么第 1 节的
OFL 义务会同时适用。LICENSE 文件内容一样（可以复用同一个 `OFL.txt`），
但**必须在 `FONT-NOTICE.txt` 里改成黑体的版权声明行**，
并遵守它多出来的 `Reserved Font Name 'Source'` 限制。

---

## 3. Ren'Py（`common.rpy` 由引擎翻译系统生成）

| 项目 | 内容 |
| --- | --- |
| 文件 | `chinese_simp/common.rpy` |
| 来源 | 由 Ren'Py 的翻译生成功能从 `renpy/common/` 生成 |
| 许可 | MIT License（Ren'Py 本体） |
| 版权 | Copyright 2004-2026 Tom Rothamel `<pytom@bishoujo.us>` |

严格来说，MIT 要求再分发衍生内容时附带其版权与许可声明。若希望完全合规，
可把游戏目录下的 `renpy/LICENSE.txt` 一并附在发布物里作为
`RENPY-LICENSE.txt`。

---

## 4. 本翻译作品自身

本翻译文本、`forcechange.rpy`、`replace_cn.rpy`、`name.rpy` 等为译者原创内容，
与上述字体许可无关，可以自行选择授权方式（例如 CC BY-NC-SA 4.0，或
「转载请注明出处、禁止商用」）。建议在 README 中明确写出。

---

## 5. 与原作的关系

本包是**非官方的玩家汉化补丁**，与原作作者无隶属关系，也未获得其背书。
发布物中**只应包含翻译相关的 .rpy 脚本与本翻译自带的字体**，不应包含原作的
`scripts.rpa` / `images.rpa` / `fonts.rpa` 等任何原始资源文件。
