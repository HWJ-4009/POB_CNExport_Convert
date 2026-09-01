# POB_CNExport_Convert

把《流放之路》国服中文客户端复制的物品文本，转换成 [PathOfBuilding](https://github.com/PathOfBuildingCommunity/PathOfBuilding) / [PoeCharm](https://github.com/Chuanhsing/PoeCharm)（PoB 的中文汉化发行版）能正确识别导入的英文格式。

## 背景

游戏内对物品按 `Ctrl+C` 复制、在 PoB / PoeCharm 里按 `Ctrl+V` 本应自动识别装备属性并添加到构筑中。但国服中文物品直接粘贴进去会**变成乱码**，无法导入。

根因（已在 PathOfBuilding 官方源码里确认）：

- `Item.lua` 在解析粘贴内容前会调用 `sanitiseText()`（`Common.lua`），其中 `text:gsub("[\128-\255]", "?")` 会把**所有字节值 ≥0x80 的字符全部替换成问号**。中文 UTF-8 字符全部是多字节且每个字节都 ≥0x80，所以会被直接打成一串问号。
- 物品解析器本身完全硬编码英文关键字（`Item Class:`、`Rarity:`、`Requirements:` 等），没有任何多语言支持。
- PoeCharm 是编译好的二进制发行包，没有可修改的源码，无法直接打补丁修复；其官方发布说明也明确把"国服人物/装备导入"标注为"维护中"。

## 解决方式

不改 PoB / PoeCharm 本身，而是在粘贴之前先把中文物品文本转换成标准英文格式——转换在浏览器本地完成，纯 ASCII 输出，天然不会触发上述乱码问题。

数据来源：PoeCharm 汉化数据集里的 `statDescriptions.csv`（GGG 官方词条文本主翻译表）与各 `Items_*.txt.csv`（基底物品名对照表）。

## 使用

打开 [`dist/poe_item_decoder.html`](dist/poe_item_decoder.html)（双击直接在浏览器打开，不用装任何东西，也不联网）：

1. 游戏里对物品按 `Ctrl+C`
2. 粘贴进左边文本框
3. 右边自动生成 PoB 能识别的英文文本（没匹配上的词条会保留中文原文并标红列出来，不会静默丢弃或猜错）
4. 复制右边结果，粘贴进 PoB / PoeCharm

## 完整构筑一键转码

页面下半部分还有一个「完整构筑一键转码」区块：粘贴国服 BD 导出工具生成的完整角色 JSON（包含 `items` 和 `passiveSkills` 两个字段），自动翻译全部装备词条、识别技能石（宝石名 + 等级 + 品质）、读取天赋配点（配点是纯数字节点 ID，天生跟语言无关），拼装压缩成一段可以直接粘贴进 PoB「输入 URL 或代码」框的构筑码。

已知局限：
- 天赋树上珠宝插槽（史实/星团/深渊珠宝等）里的珠宝会作为物品一起导入，但暂不会自动插回天赋树上对应的插槽，需要手动拖拽。
- 文身（Tattoo）改造过的天赋节点效果暂不支持，会保留原始节点。
- 这个功能没有经过真实 PoB 客户端逐项验证（生成逻辑对照 PathOfBuilding 开源代码核实过格式，但无法在本环境里实际打开 PoB 测试导入结果），建议导入后自行核对装备与技能是否正确。

## 从源码重新构建

`dist/poe_item_decoder.html` 是自包含的产物（把编译好的词条字典、以及 [pako](https://github.com/nodeca/pako)（MIT/Zlib 双授权，用于构筑码的 deflate 压缩）直接内嵌进了页面），日常使用不需要重新构建。只有更新翻译数据、或想改转换逻辑时才需要：

```bash
# 1. 编译词条字典（需要你本机装好的 PoeCharm 的汉化数据目录）
python build_dict.py --poecharm-data "D:\PoeCharm\Data\Translate\zh-rCN"

# 2. 把字典内嵌进单文件页面
python gen_html.py
```

产物写到 `dist/poe_item_decoder.html`。

## 已知局限

- 只支持普通粘贴格式，不解析游戏内"高级物品描述"格式里的 `{ 词缀批注 }` 括号行——这些本来就不是 PoB 解析普通英文物品文本所必需的，直接丢弃不影响识别结果。
- 花哨的物品命名（比如"活尸加护"）不参与任何计算，转换时统一用基底物品名代替，这跟 PoB 自身处理未知命名时的行为一致。
- 词条覆盖率取决于 PoeCharm 汉化数据集本身的完整度，遇到版本更新后措辞变化、或数据集本身缺失的词条时会在页面上如实标出未匹配，不会静默出错。

## 目录结构

```
build_dict.py       编译 CN→EN 字典（statDescriptions.csv / Items_*.txt.csv / tree_dn.csv / Gems_data.txt.csv → build/*.json）
gen_html.py         把字典 + vendor_pako.min.js 内嵌进单文件页面 → dist/poe_item_decoder.html
vendor_pako.min.js  第三方 deflate 压缩库（MIT/Zlib 授权，用于生成构筑码），直接提交进仓库
dist/               最终产物，唯一需要分发的文件
build/              中间产物（.gitignore 排除，本地重新生成）
```
