# -*- coding: utf-8 -*-
"""
把 build_dict.py 生成的三份字典内嵌进单文件 HTML 页面。
先跑 build_dict.py，再跑这个脚本：
    python build_dict.py --poecharm-data "D:\\PoeCharm\\Data\\Translate\\zh-rCN"
    python gen_html.py
输出：dist/poe_item_decoder.html（这是唯一需要分发/发布的文件，自包含，双击/托管即可用）。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "build")
DIST_DIR = os.path.join(HERE, "dist")

with open(os.path.join(BUILD_DIR, "mod_dict.json"), encoding="utf-8") as f:
    mod_dict = json.load(f)
with open(os.path.join(BUILD_DIR, "base_dict.json"), encoding="utf-8") as f:
    base_dict = json.load(f)
with open(os.path.join(BUILD_DIR, "notable_dict.json"), encoding="utf-8") as f:
    notable_dict = json.load(f)
with open(os.path.join(BUILD_DIR, "gem_dict.json"), encoding="utf-8") as f:
    gem_dict = json.load(f)
with open(os.path.join(HERE, "vendor_pako.min.js"), encoding="utf-8") as f:
    pako_source = f.read()

mod_dict_json = json.dumps(mod_dict, ensure_ascii=False, separators=(",", ":"))
base_dict_json = json.dumps(base_dict, ensure_ascii=False, separators=(",", ":"))
notable_dict_json = json.dumps(notable_dict, ensure_ascii=False, separators=(",", ":"))
gem_dict_json = json.dumps(gem_dict, ensure_ascii=False, separators=(",", ":"))

TEMPLATE = r"""<!doctype html>
<meta charset="utf-8">
<title>PoE 物品译码器</title>
<style>
:root {
  --bg: #17151f;
  --surface: #1f1c29;
  --surface-2: #262233;
  --border: #363047;
  --text: #ece7db;
  --text-dim: #9992a8;
  --accent: #c8a04d;
  --accent-soft: #4a3f24;
  --mono-glow: #2a2438;
  --rarity-normal: #cfc9bd;
  --rarity-magic: #6f9fe8;
  --rarity-rare: #d9c34a;
  --rarity-unique: #c96a3f;
  --danger: #d9765a;
  --danger-soft: #3a2320;
  --ok: #7fae6e;
  --font-display: 'Cinzel', 'Iowan Old Style', Georgia, serif;
  --font-ui: 'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', 'Cascadia Code', Consolas, monospace;
}
:root:not([data-theme="light"]) {
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --bg: #f4f1ea;
    --surface: #ffffff;
    --surface-2: #ece6d8;
    --border: #d8d0bd;
    --text: #2a2416;
    --text-dim: #6e6650;
    --accent: #92651f;
    --accent-soft: #ecd9ab;
    --mono-glow: #f7f2e4;
    --rarity-normal: #4a4438;
    --rarity-magic: #2a5aa8;
    --rarity-rare: #8a7412;
    --rarity-unique: #a44a1f;
    --danger: #a8402a;
    --danger-soft: #f6dcd3;
    --ok: #3f7a2e;
  }
}
:root[data-theme="light"] {
  --bg: #f4f1ea;
  --surface: #ffffff;
  --surface-2: #ece6d8;
  --border: #d8d0bd;
  --text: #2a2416;
  --text-dim: #6e6650;
  --accent: #92651f;
  --accent-soft: #ecd9ab;
  --mono-glow: #f7f2e4;
  --rarity-normal: #4a4438;
  --rarity-magic: #2a5aa8;
  --rarity-rare: #8a7412;
  --rarity-unique: #a44a1f;
  --danger: #a8402a;
  --danger-soft: #f6dcd3;
  --ok: #3f7a2e;
}
:root[data-theme="dark"] {
  --bg: #17151f;
  --surface: #1f1c29;
  --surface-2: #262233;
  --border: #363047;
  --text: #ece7db;
  --text-dim: #9992a8;
  --accent: #c8a04d;
  --accent-soft: #4a3f24;
  --mono-glow: #2a2438;
  --rarity-normal: #cfc9bd;
  --rarity-magic: #6f9fe8;
  --rarity-rare: #d9c34a;
  --rarity-unique: #c96a3f;
  --danger: #d9765a;
  --danger-soft: #3a2320;
  --ok: #7fae6e;
}

* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-ui);
  line-height: 1.5;
  padding: 2.5rem clamp(1rem, 4vw, 3rem) 4rem;
}

.wrap { max-width: 1240px; margin: 0 auto; }

header.page {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.75rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 1.5rem;
}
h1 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(1.6rem, 2.6vw, 2.2rem);
  letter-spacing: 0.02em;
  margin: 0;
  color: var(--accent);
  text-wrap: balance;
}
.subtitle {
  color: var(--text-dim);
  font-size: 0.95rem;
  max-width: 62ch;
}
.subtitle b { color: var(--text); font-weight: 600; }

.panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  align-items: start;
}
@media (max-width: 880px) {
  .panels { grid-template-columns: 1fr; }
}

.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.7rem 0.9rem;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2);
}
.panel-label {
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-dim);
  font-weight: 600;
}
.rarity-chip {
  font-size: 0.72rem;
  font-family: var(--font-mono);
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  border: 1px solid currentColor;
  display: none;
}
.rarity-chip.show { display: inline-block; }
.rarity-normal { color: var(--rarity-normal); }
.rarity-magic { color: var(--rarity-magic); }
.rarity-rare { color: var(--rarity-rare); }
.rarity-unique { color: var(--rarity-unique); }

textarea, pre.output {
  width: 100%;
  border: 0;
  resize: vertical;
  background: var(--mono-glow);
  color: var(--text);
  font-family: var(--font-mono);
  font-size: 0.86rem;
  line-height: 1.55;
  padding: 0.9rem;
  min-height: 380px;
  font-variant-numeric: tabular-nums;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}
textarea:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
textarea::placeholder { color: var(--text-dim); opacity: 0.7; }

.miss-line { color: var(--danger); }

.panel-foot {
  display: flex;
  gap: 0.6rem;
  padding: 0.7rem 0.9rem;
  border-top: 1px solid var(--border);
  background: var(--surface-2);
}

button {
  font-family: var(--font-ui);
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 7px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  padding: 0.5rem 0.95rem;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease;
}
button:hover { border-color: var(--accent); }
button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
button.primary {
  background: var(--accent-soft);
  border-color: var(--accent);
  color: var(--accent);
}
button.primary:hover { background: var(--accent); color: var(--bg); }
button:disabled { opacity: 0.45; cursor: default; }

.status-line {
  margin-left: auto;
  font-size: 0.8rem;
  color: var(--text-dim);
  align-self: center;
  font-variant-numeric: tabular-nums;
}
.status-line.ok { color: var(--ok); }
.status-line.warn { color: var(--danger); }

.report {
  margin-top: 1.25rem;
  background: var(--danger-soft);
  border: 1px solid var(--danger);
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
  display: none;
}
.report.show { display: block; }
.report h2 {
  margin: 0 0 0.5rem;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--danger);
  font-family: var(--font-ui);
}
.report ul { margin: 0; padding-left: 1.2rem; font-family: var(--font-mono); font-size: 0.85rem; }
.report li { margin-bottom: 0.25rem; }

footer.note {
  margin-top: 2rem;
  color: var(--text-dim);
  font-size: 0.82rem;
  max-width: 72ch;
}
footer.note code {
  font-family: var(--font-mono);
  background: var(--surface-2);
  padding: 0.05rem 0.35rem;
  border-radius: 4px;
  border: 1px solid var(--border);
}
.section-divider {
  border: 0;
  border-top: 1px solid var(--border);
  margin: 2rem 0 1.5rem;
}
.bd-panel { margin-top: 0; }
.bd-panel textarea { min-height: 220px; }
.bd-desc {
  padding: 0.7rem 0.9rem 0;
  margin: 0;
  color: var(--text-dim);
  font-size: 0.85rem;
  line-height: 1.5;
}
.bd-desc code {
  font-family: var(--font-mono);
  background: var(--surface-2);
  padding: 0.05rem 0.35rem;
  border-radius: 4px;
  border: 1px solid var(--border);
}
.bd-caveat {
  padding: 0.7rem 0.9rem;
  margin: 0;
  color: var(--rarity-magic);
  font-size: 0.8rem;
  line-height: 1.5;
  border-top: 1px solid var(--border);
}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">

<div class="wrap">
  <header class="page">
    <h1>PoE 物品译码器</h1>
    <div class="subtitle">
      把国服中文客户端复制的物品文本，转换成 <b>PathOfBuilding / PoeCharm</b> 能正确识别的英文格式——
      国服物品直接粘贴进 PoB 会因为一个已知的字符处理 bug 变成乱码，先在这里转一道就不会了。
      转换在浏览器本地完成，不上传任何数据。
    </div>
  </header>

  <div class="panels">
    <section class="panel">
      <div class="panel-head">
        <span class="panel-label">中文物品文本</span>
        <span class="rarity-chip" id="rarityIn"></span>
      </div>
      <textarea id="input" spellcheck="false" placeholder="在游戏里对物品按 Ctrl+C，然后粘贴到这里……"></textarea>
      <div class="panel-foot">
        <button class="primary" id="convertBtn">转换 →</button>
        <button id="clearBtn">清空</button>
        <span class="status-line" id="inStatus"></span>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <span class="panel-label">英文物品文本（粘贴进 PoB）</span>
        <span class="rarity-chip" id="rarityOut"></span>
      </div>
      <pre class="output" id="output" aria-live="polite"></pre>
      <div class="panel-foot">
        <button class="primary" id="copyBtn" disabled>复制结果</button>
        <span class="status-line" id="outStatus"></span>
      </div>
    </section>
  </div>

  <div class="report" id="report">
    <h2>未匹配的词条（保留了中文原文，请手动核对）</h2>
    <ul id="reportList"></ul>
  </div>

  <footer class="note">
    数据来源：PoeCharm 汉化数据集里的 <code>statDescriptions.csv</code>（词条主翻译表）与各 <code>Items_*.txt.csv</code>（基底物品名对照表）。
    花哨的物品命名（比如"活尸加护"）不参与任何计算，转换时统一用基底物品名代替。
    高级复制格式里的 <code>{ 词缀批注 }</code> 和 <code>（提示文字）</code> 行会被丢弃——PoB 解析普通英文物品文本时本来就不需要这些，丢了不影响识别结果。
  </footer>

  <hr class="section-divider">

  <section class="panel bd-panel">
    <div class="panel-head">
      <span class="panel-label">完整构筑一键转码（装备 + 技能 + 天赋）</span>
    </div>
    <p class="bd-desc">
      粘贴国服 BD 导出工具生成的完整角色 JSON（包含 <code>items</code> 和 <code>passiveSkills</code> 两个字段），
      自动翻译装备词条、识别技能石、读取天赋配点，拼装成一段可以直接粘贴进 PoB「输入 URL 或代码」框的构筑码。
    </p>
    <textarea id="bdInput" spellcheck="false" placeholder="把完整角色 JSON 粘贴到这里……"></textarea>
    <div class="panel-foot">
      <button class="primary" id="bdConvertBtn">生成构筑码 →</button>
      <span class="status-line" id="bdStatus"></span>
    </div>
    <textarea id="bdOutput" spellcheck="false" readonly placeholder="生成的构筑码会显示在这里"></textarea>
    <div class="panel-foot">
      <button class="primary" id="bdCopyBtn" disabled>复制构筑码</button>
    </div>
    <div class="report" id="bdReport">
      <h2 id="bdReportTitle"></h2>
      <ul id="bdReportList"></ul>
    </div>
    <p class="bd-caveat">
      已知局限：天赋树上珠宝插槽（史实/星团/深渊珠宝等）里的珠宝会作为物品一起导入，但暂时不会自动插回天赋树上对应的插槽，需要手动拖拽；
      文身（Tattoo）改造过的天赋节点效果暂不支持，会保留原始节点。这段代码没有经过真实 PoB 客户端验证，请导入后自行核对装备与技能是否正确。
    </p>
  </section>
</div>

<script>PAKO_SOURCE_PLACEHOLDER</script>
<script>
const MOD_DICT = MOD_DICT_PLACEHOLDER;
const BASE_DICT = BASE_DICT_PLACEHOLDER;
const NOTABLE_DICT = NOTABLE_DICT_PLACEHOLDER;
const GEM_DICT = GEM_DICT_PLACEHOLDER;

const CLASS_MAP = {
  "头盔":"Helmet","胸甲":"Body Armour","护手":"Gloves","手套":"Gloves","鞋子":"Boots","靴子":"Boots",
  "盾牌":"Shield","腰带":"Belt","项链":"Amulet","戒指":"Ring","箭袋":"Quiver",
  "匕首":"Dagger","短剑":"Dagger","单手剑":"One Hand Sword","双手剑":"Two Hand Sword",
  "细剑":"Thrusting One Hand Sword","单手斧":"One Hand Axe","双手斧":"Two Hand Axe",
  "单手锤":"One Hand Mace","双手锤":"Two Hand Mace","权杖":"Sceptre","法杖":"Wand",
  "长杖":"Staff","弓":"Bow","法器":"Focus","鱼竿":"Fishing Rod",
  "爪":"Claw","军旗":"War Banner",
  "生命药剂":"Life Flask","魔力药剂":"Mana Flask","混合药剂":"Hybrid Flask","神圣药剂":"Utility Flask",
  "功能药剂":"Utility Flask",
  "珠宝":"Jewel","异能珠宝":"Abyss Jewel","星团珠宝":"Cluster Jewel",
  "地图碎片":"Map Fragment","地图":"Map","符石":"Rune",
};
const RARITY_MAP = { "普通":"Normal","一般":"Normal","魔法":"Magic","稀有":"Rare","传奇":"Unique" };
const RARITY_EN2ZH = { "Normal":"普通","Magic":"魔法","Rare":"稀有","Unique":"传奇" };

const NUM_RE = /[+-]?\d+(?:\.\d+)?(?:\((?:-?\d+(?:\.\d+)?)-(?:-?\d+(?:\.\d+)?)\))?/g;

function normalizeLine(line) {
  const values = [];
  const template = line.replace(NUM_RE, (m) => {
    values.push(m);
    return "{" + (values.length - 1) + "}";
  });
  return { template, values };
}

// A handful of connective words appear inconsistently between otherwise-identical
// templates in the source data (e.g. "与" vs "和", both meaning "and").
// Tried only as a fallback when the exact template isn't found.
const SYNONYM_SWAPS = [["与", "和"], ["和", "与"], ["生效时间", "持续时间"], ["持续时间", "生效时间"]];

// Manually-confirmed entries for lines statDescriptions.csv either doesn't
// cover (flask base-type buffs - fixed strings from PathOfBuilding source's
// src/Data/Bases/flask.lua, not a rolled affix) or covers only under
// different CN phrasing than the client actually uses for that stat.
// Extend only with entries confirmed against a real item + source data.
const EXTRA_MOD_DICT = {
  "{0}% 所有元素抗性": "{0}% to all Elemental Resistances", // Bismuth Flask base buff
  "{0}% 法术伤害格挡几率": "{0}% Chance to Block Spell Damage",
  "{0}% 攻击伤害格挡几率上限": "{0}% to maximum Chance to Block Attack Damage",
  "{0}% 法术伤害格挡几率上限": "{0}% to maximum Chance to Block Spell Damage",
  // Ewar's Mirage local added-damage implicit; confirmed exact wording via
  // PathOfBuilding source (src/Data/Uniques/sword.lua: "Adds 1 to (45-55)
  // Lightning Damage"). Other elements' CN wording not yet confirmed.
  "该装备附加 {0} - {1} 基础闪电伤害": "Adds {0} to {1} Lightning Damage",
  // Confirmed via statDescriptions.csv id 10405/16109 modulo wording drift
  // ("击中有" vs "击中时有", "威吓" vs "恐惧" - both mean the same Unnerve
  // ailment, just different CN phrasing for the same EN stat).
  "击中有 {0}% 的几率威吓敌人 {1} 秒": "{0}% chance to Unnerve Enemies for {1} seconds on Hit",
  // The Red Nightmare (Timeless/Historic-style Crimson Jewel); confirmed
  // exact multi-line wording via PathOfBuilding source
  // (src/Data/Uniques/jewel.lua:656-657, variant 2 = the 50% roll).
  "范围内提高火焰抗性或所有元素的天赋\n也会以 {0}% 的比例提高攻击伤害格挡几率":
    "Passives granting Fire Resistance or all Elemental Resistances in Radius\nalso grant Chance to Block Attack Damage at {0}% of its value",
  // Reconstructed from three independently-confirmed fragments (祭血术 =
  // "Blood Magic" per tree_dn.csv; "未连结至天赋树的情况下配置" = "without
  // being connected to your tree" per statDescriptions.csv id 4557; 通途 =
  // "Passage", the notable name used by the structurally-identical
  // "Intuitive Leap" jewel.lua entry). The exact unique isn't in this local
  // PoB source snapshot, so unlike the other entries here this one hasn't
  // been checked against one single complete source string - worth an
  // extra look after importing.
  "祭血术范围内的核心天赋技能可以在\n未连结至天赋树的情况下配置\n通途":
    "Notable Passive Skills in Blood Magic's Radius can be Allocated without being connected to your tree\nPassage",
};

function lookupTemplate(template) {
  let hit = MOD_DICT[template];
  if (hit !== undefined) return hit;
  for (const [from, to] of SYNONYM_SWAPS) {
    if (template.includes(from)) {
      hit = MOD_DICT[template.split(from).join(to)];
      if (hit !== undefined) return hit;
    }
  }
  hit = EXTRA_MOD_DICT[template];
  if (hit !== undefined) return hit;
  // Some statDescriptions.csv rows number their {0}/{1} placeholders to
  // match the English argument order, which isn't always the order the
  // numbers appear in the Chinese text (e.g. "每 {1}% 品质使效果区域扩大
  // {0}%" <-> "Grants {0}% increased Area of Effect per {1}% Quality" -
  // Quality comes first in the Chinese sentence but is argument {1} in
  // English). Our template always numbers by first-appearance order, so as
  // a last resort, try the swapped form and swap the match back so it lines
  // up with our own values array.
  if (template.includes("{0}") && template.includes("{1}") && !template.includes("{2}")) {
    const swap01 = (s) => s.replace(/\{0\}/g, "\x00").replace(/\{1\}/g, "{0}").replace(/\x00/g, "{1}");
    hit = MOD_DICT[swap01(template)];
    if (hit !== undefined) return swap01(hit);
  }
  return undefined;
}

function translateModLine(rawLine) {
  const line = rawLine.trim();
  if (!line) return { ok: true, text: "" };
  const { template, values } = normalizeLine(line);
  let enTemplate = lookupTemplate(template);
  if (enTemplate === undefined) enTemplate = lookupTemplate(line);
  if (enTemplate === undefined) return { ok: false, text: line };
  const out = enTemplate.replace(/\{(\d+)\}/g, (m, idx) => {
    const i = Number(idx);
    return i < values.length ? values[i] : m;
  });
  return { ok: true, text: out };
}

function isBracketLine(line) {
  const t = line.trim();
  if (t.startsWith("{") && t.endsWith("}")) return true;
  // The client's own text isn't always consistent about half-width vs
  // full-width parens on the same line (e.g. "(...)" opened half-width but
  // closed full-width "\uFF09") - accept either width on either side.
  const opensParen = t.startsWith("(") || t.startsWith("\uFF08");
  const closesParen = t.endsWith(")") || t.endsWith("\uFF09");
  return opensParen && closesParen;
}

function stripLabelSpaces(s) {
  return s.replace(/\s+/g, "");
}

// Splits a line on the first colon (half- or full-width), returning
// [label-with-internal-whitespace-stripped, value-from-original-text].
// Using the original text for the value preserves real spacing (e.g. "196 (augmented)").
function splitLabel(line) {
  const idx = line.search(/[:\uff1a]/);
  if (idx === -1) return [stripLabelSpaces(line), null];
  return [stripLabelSpaces(line.slice(0, idx)), line.slice(idx + 1).trim()];
}

const LABEL_MAP = {
  "\u54c1\u8d28": "Quality", "\u62a4\u7532": "Armour", "\u95ea\u907f\u503c": "Evasion Rating",
  "\u80fd\u91cf\u62a4\u76fe": "Energy Shield", "\u865a\u5316": "Ward", "\u7ed3\u754c": "Ward", "\u7b49\u7ea7": "Level", "\u529b\u91cf": "Strength",
  "\u654f\u6377": "Dexterity", "\u667a\u6167": "Intelligence", "\u7269\u54c1\u7b49\u7ea7": "Item Level",
  "\u4ec5\u9650": "Limited to", "\u8303\u56f4": "Radius", "\u683c\u6321\u51e0\u7387": "Chance to Block",
  "\u7269\u7406\u4f24\u5bb3": "Physical Damage", "\u653b\u51fb\u66b4\u51fb\u7387": "Critical Strike Chance",
  "\u6bcf\u79d2\u653b\u51fb\u6b21\u6570": "Attacks per Second", "\u6b66\u5668\u8303\u56f4": "Weapon Range",
  "\u706b\u7130\uff0c\u51b0\u971c\uff0c\u95ea\u7535\u4f24\u5bb3": "Elemental Damage", "\u706b\u7130\u4f24\u5bb3": "Fire Damage",
  "\u51b0\u971c\u4f24\u5bb3": "Cold Damage", "\u95ea\u7535\u4f24\u5bb3": "Lightning Damage",
};
const FIXED_LINES = {
  "\u9700\u6c42:": "Requirements:", "\u5df2\u8150\u5316": "Corrupted", "\u5df2\u590d\u5236": "Mirrored",
  "\u672a\u9274\u5b9a": "Unidentified", "\u5df2\u5206\u88c2": "Split", "\u5206\u88c2\u4e4b\u7269": "Fractured Item",
  "\u711a\u754c\u8005\u7269\u54c1": "Searing Exarch Item", "\u706d\u754c\u8005\u7269\u54c1": "Eater of Worlds Item",
};
// Value-side word substitutions for LABEL_MAP fields whose value also
// contains untranslated Chinese (e.g. "Limited to: 1 \u53f2\u5b9e", "Radius: \u5c0f").
// Scoped per label so a substitution for one field can't leak into another.
const VALUE_WORD_MAPS = {
  "\u4ec5\u9650": { "\u53f2\u5b9e": "Historic" },
  "\u8303\u56f4": { "\u5c0f": "Small", "\u4e2d": "Medium", "\u5927": "Large" },
};
// Fixed UI/instruction text that has no effect on any PoB calculation
// (confirmed absent from PoB's own Item.lua field parser and its bundled
// Uniques database) - safe to drop, same rationale as bracket/reminder lines.
const DROP_LINES = new Set([
  "\u653e\u7f6e\u5230\u4e00\u4e2a\u5929\u8d4b\u6811\u7684\u73e0\u5b9d\u63d2\u69fd\u4e2d\u4ee5\u4ea7\u751f\u6548\u679c\u3002\u53f3\u952e\u70b9\u51fb\u4ee5\u79fb\u51fa\u63d2\u69fd\u3002",
  "\u653e\u5165\u4e00\u4e2a\u7269\u54c1\u7684\u6df1\u6e0a\u63d2\u69fd\u6216\u5929\u8d4b\u6811\u4e0a\u7684\u73e0\u5b9d\u63d2\u69fd\u4e2d\u4ee5\u751f\u6548\u3002\u53f3\u952e\u70b9\u51fb\u4ee5\u79fb\u51fa\u63d2\u69fd\u3002",
  "\u653e\u5165\u5929\u8d4b\u6811\u4e0a\u914d\u7f6e\u597d\u7684\u5927\u578b\u73e0\u5b9d\u69fd\u3002\u589e\u52a0\u7684\u5929\u8d4b\u8ddf\u73e0\u5b9d\u8303\u56f4\u65e0\u5173\u3002\u53ef\u4ee5\u53f3\u952e\u70b9\u51fb\u4ece\u63d2\u69fd\u4e2d\u79fb\u9664\u3002",
  "\u51fa\u552e\u83b7\u5f97\u901a\u8d27:\u975e\u7ed1\u5b9a",
  "\u53f3\u952e\u70b9\u51fb\u996e\u7528\u3002\u53ea\u6709\u5728\u8170\u5e26\u91cc\u624d\u6062\u590d\u4f7f\u7528\u6b21\u6570\u3002\u51fb\u8d25\u654c\u4eba\u65f6\u5145\u6ee1\u3002",
  "\u70b9\u51fb\u53f3\u952e\u4ee5\u559d\u4e0b\u836f\u5242\u3002\u53ea\u6709\u88c5\u5907\u4e8e\u8170\u5e26\u4e0a\u65f6\u624d\u4f1a\u5145\u80fd\u3002\u51fb\u8d25\u602a\u7269\u65f6\u4f1a\u56de\u590d\u5145\u80fd\u6b21\u6570\u3002",
  // Abyss-league Historic Eye Jewels (Festering Vengeance etc, confirmed
  // earlier via jewel.lua) show "\u6df1\u6e0a" as a bare category tag (a property
  // with an empty values array - no ":" field at all) and repeat "\u53f2\u5b9e"
  // as a bare mod-list entry alongside the already-handled "\u4ec5\u9650: 1 \u53f2\u5b9e"
  // property. Neither has any PoB field or database entry - same rationale
  // as the other drops above.
  "\u6df1\u6e0a",
  "\u53f2\u5b9e",
]);
// Flask duration/charge state lines. These aren't dictionary mod
// templates - PoB's own parser recognises and no-ops them by an exact
// regex match (Item.lua: line:match("^Lasts .+ Seconds$") etc.), so the
// English wording below is taken directly from that source, not guessed.
function translateFlaskStateLine(line) {
  let m;
  if ((m = line.match(/^\u6301\u7eed\s*(.+?)\s*\u79d2$/))) return "Lasts " + m[1] + " Seconds";
  if ((m = line.match(/^\u6bcf\u6b21\u4f7f\u7528\u4f1a\u4ece\s*(\d+)\s*\u5145\u80fd\u6b21\u6570\u4e2d\u6d88\u8017\s*(\d+)\s*\u6b21$/)))
    return "Consumes " + m[2] + " of " + m[1] + " Charges on use";
  if ((m = line.match(/^\u76ee\u524d\u6709\s*(\d+)\s*\u5145\u80fd\u6b21\u6570$/))) return "Currently has " + m[1] + " Charges";
  return null;
}
// Cluster Jewel enchant-granted small-passive lines are wrapped as
// "\u589e\u52a0\u7684\u5c0f\u5929\u8d4b\u83b7\u5f97\uff1a<stat>" in the client, but statDescriptions.csv only
// stores the bare <stat> template plus the *also*-grant ("\u8fd8\u83b7\u5f97") wrapped
// form used for affix lines. Confirmed via statDescriptions.csv that
// "\u8fd8" is the only difference between the "\u83b7\u5f97"/"\u8fd8\u83b7\u5f97" wrappers, so the
// English wrapper below is derived directly from the "\u8fd8\u83b7\u5f97" rows
// (e.g. "Added Small Passive Skills also grant: {0} to Armour" <->
// "\u589e\u52a0\u7684\u5c0f\u5929\u8d4b\u8fd8\u83b7\u5f97\uff1a{0} \u62a4\u7532\u503c"), dropping "also " the same way the
// source drops "\u8fd8".
const ENCHANT_GRANT_PREFIX_ZH = "\u589e\u52a0\u7684\u5c0f\u5929\u8d4b\u83b7\u5f97\uff1a";
const ENCHANT_GRANT_PREFIX_EN = "Added Small Passive Skills grant: ";

// Anoint enchants ("\u914d\u7f6e <Notable Name> (enchant)") name a passive tree
// node, not a number, so they can't go through the usual digit-placeholder
// template lookup - the template is "Allocates {0}" (statDescriptions.csv,
// confirmed) with {0} being the node's own display name (tree_dn.csv,
// e.g. "Testudo" <-> "\u9f9f\u7532\u76fe").
const ANOINT_PREFIX_ZH = "\u914d\u7f6e ";
const ANOINT_PREFIX_EN = "Allocates ";

// When an item's quality came from a Catalyst, PoB expects the label
// "Quality (<Descriptor> Modifiers)" - confirmed via Item.lua:653-659
// (`specName:match("Quality %([%a%s]+ Modifiers%)")` matched against the 12
// catalyst descriptors at Item.lua:15) and the CN descriptor word via
// ItemsTab.csv's Catalyst names (e.g. "Intrinsic (Attribute)" <->
// "\u5185\u5728\u50ac\u5316\u5242(\u5c5e\u6027)"). Only descriptors seen in a real item go in this map;
// extend as further catalyst types come up (Attack/Speed/Suffix/Life and
// Mana/Caster/Physical and Chaos/Resistance/Prefix/Defence/Elemental/Critical).
const QUALITY_CATALYST_DESCRIPTORS = { "\u5c5e\u6027": "Attribute" };

// Translate a single logical line (already stripped of any trailing
// " (enchant)" tag and any "X \u2014 \u6570\u503c\u4e0d\u53ef\u8c03\u6574" annotation suffix).
function translateLine(line) {
  if (isBracketLine(line)) return { drop: true };

  const flaskState = translateFlaskStateLine(line);
  if (flaskState !== null) return { text: flaskState };

  const [label, value] = splitLabel(line);
  const compact = stripLabelSpaces(line);

  if (DROP_LINES.has(compact)) return { drop: true };

  // Weapons repeat their own base type as a bare line (no colon) inside
  // the attack-stats block (e.g. a Staff's tooltip literally has a lone
  // "Staff" line before "Physical Damage: ..."). PoB's parser explicitly
  // recognises and ignores this line when it matches the item's base type
  // (Item.lua:1322) rather than treating it as an unrecognised mod, so
  // translate it via the same CLASS_MAP used for "Item Class:".
  if (value === null && compact in CLASS_MAP) {
    return { text: CLASS_MAP[compact] };
  }

  if (label === "\u63d2\u69fd" && value !== null) {
    return { text: "Sockets: " + value };
  }
  if (line.startsWith(ANOINT_PREFIX_ZH)) {
    const nodeNameZh = line.slice(ANOINT_PREFIX_ZH.length);
    const nodeNameEn = NOTABLE_DICT[nodeNameZh];
    if (nodeNameEn) return { text: ANOINT_PREFIX_EN + nodeNameEn };
    return { miss: line };
  }
  const qualityCatalystMatch = value !== null && label.match(/^\u54c1\u8d28\uff08(.+)\u8bcd\u7f00\uff09$/);
  if (qualityCatalystMatch) {
    const descriptor = QUALITY_CATALYST_DESCRIPTORS[qualityCatalystMatch[1]];
    if (descriptor) return { text: "Quality (" + descriptor + " Modifiers): " + value };
  }
  if (label in LABEL_MAP && value !== null) {
    let mappedValue = value;
    const wordMap = VALUE_WORD_MAPS[label];
    if (wordMap) {
      for (const [zh, en] of Object.entries(wordMap)) {
        mappedValue = mappedValue.split(zh).join(en);
      }
    }
    return { text: LABEL_MAP[label] + ": " + mappedValue };
  }
  if (compact in FIXED_LINES) {
    return { text: FIXED_LINES[compact] };
  }
  if (line.startsWith(ENCHANT_GRANT_PREFIX_ZH)) {
    const core = line.slice(ENCHANT_GRANT_PREFIX_ZH.length);
    const res = translateModLine(core);
    if (res.ok && res.text) return { text: ENCHANT_GRANT_PREFIX_EN + res.text };
    return { miss: line };
  }

  const res = translateModLine(line);
  if (res.ok) return { text: res.text };
  return { miss: res.text };
}

// Wraps translateLine() with the enchant-tag / value-locked-annotation
// stripping that every raw item line needs (used by both convertItem()'s
// line loop and the batch build-code item builder).
function translateItemLine(rawLine) {
  let line = rawLine;
  let enchantSuffix = "";
  const enchantMatch = line.match(/^(.*)\s\(enchant\)$/);
  if (enchantMatch) {
    line = enchantMatch[1];
    enchantSuffix = " (enchant)";
  }
  const annotationMatch = line.match(/^(.*?)\s*\u2014\s*\u6570\u503c\u4e0d\u53ef\u8c03\u6574\s*$/);
  if (annotationMatch) line = annotationMatch[1];
  if (!line) return { drop: true };

  const result = translateLine(line);
  if (result.drop) return { drop: true };
  if (result.text !== undefined) return { text: result.text ? result.text + enchantSuffix : "" };
  return { miss: result.miss, enchantSuffix };
}

function convertItem(raw) {
  const lines = raw.split(/\r?\n/).map((l) => l.trim()).filter((l) => l.length > 0);
  const out = [];
  const misses = [];
  let rarity = null;
  let i = 0;

  // Item class (optional, best-effort, safe to omit if unrecognised)
  if (i < lines.length) {
    const [label, value] = splitLabel(lines[i]);
    if (label === "\u7269\u54c1\u7c7b\u522b" && value !== null) {
      const enClass = CLASS_MAP[value];
      if (enClass) out.push("Item Class: " + enClass);
      i++;
    }
  }

  // Rarity
  if (i < lines.length) {
    const [label, value] = splitLabel(lines[i]);
    if (label === "\u7a00\u6709\u5ea6" && value !== null) {
      rarity = RARITY_MAP[value] || "Rare";
      out.push("Rarity: " + rarity);
      i++;
    }
  }
  if (!rarity) rarity = "Rare";

  // Name lines: fancy name (optional 2nd line) + base name
  if (i < lines.length) {
    let baseNameZh = lines[i];
    let nameLineCount = 1;
    if (rarity === "Rare" || rarity === "Unique") {
      if (i + 1 < lines.length && lines[i + 1] !== "--------") {
        baseNameZh = lines[i + 1];
        nameLineCount = 2;
      }
    }
    const baseNameEn = BASE_DICT[baseNameZh] || baseNameZh;
    if (nameLineCount === 2) {
      out.push(baseNameEn);
      out.push(baseNameEn);
    } else {
      out.push(baseNameEn);
    }
    i += nameLineCount;
  }

  // Remaining lines
  for (; i < lines.length; i++) {
    const line = lines[i];
    if (line === "--------") { out.push(line); continue; }

    const result = translateItemLine(line);
    if (result.drop) continue;
    if (result.text !== undefined) {
      if (result.text) out.push(result.text);
      continue;
    }
    out.push("# UNTRANSLATED: " + result.miss + (result.enchantSuffix || ""));
    misses.push(result.miss);
  }

  return { text: out.join("\n"), misses, rarity };
}

const inputEl = document.getElementById("input");
const outputEl = document.getElementById("output");
const convertBtn = document.getElementById("convertBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");
const inStatus = document.getElementById("inStatus");
const outStatus = document.getElementById("outStatus");
const reportEl = document.getElementById("report");
const reportList = document.getElementById("reportList");
const rarityIn = document.getElementById("rarityIn");
const rarityOut = document.getElementById("rarityOut");

function setRarityChip(el, rarity) {
  el.className = "rarity-chip";
  if (!rarity) { el.classList.remove("show"); el.textContent = ""; return; }
  const cls = { Normal: "rarity-normal", Magic: "rarity-magic", Rare: "rarity-rare", Unique: "rarity-unique" }[rarity] || "rarity-normal";
  el.classList.add("show", cls);
  el.textContent = rarity;
}

function runConvert() {
  const raw = inputEl.value;
  if (!raw.trim()) {
    outputEl.textContent = "";
    inStatus.textContent = "";
    outStatus.textContent = "";
    reportEl.classList.remove("show");
    copyBtn.disabled = true;
    setRarityChip(rarityIn, null);
    setRarityChip(rarityOut, null);
    return;
  }
  const { text, misses, rarity } = convertItem(raw);
  outputEl.textContent = text;
  copyBtn.disabled = false;
  setRarityChip(rarityIn, rarity);
  setRarityChip(rarityOut, rarity);

  const lineCount = raw.split(/\r?\n/).filter((l) => l.trim()).length;
  inStatus.textContent = lineCount + " \u884c\u8f93\u5165";

  if (misses.length) {
    outStatus.textContent = misses.length + " \u6761\u672a\u5339\u914d";
    outStatus.className = "status-line warn";
    reportList.innerHTML = "";
    misses.forEach((m) => {
      const li = document.createElement("li");
      li.className = "miss-line";
      li.textContent = m;
      reportList.appendChild(li);
    });
    reportEl.classList.add("show");
  } else {
    outStatus.textContent = "\u5168\u90e8\u5339\u914d";
    outStatus.className = "status-line ok";
    reportEl.classList.remove("show");
  }
}

convertBtn.addEventListener("click", runConvert);
inputEl.addEventListener("input", () => {
  clearTimeout(window.__debounce);
  window.__debounce = setTimeout(runConvert, 250);
});
clearBtn.addEventListener("click", () => {
  inputEl.value = "";
  runConvert();
  inputEl.focus();
});
copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(outputEl.textContent);
    const original = copyBtn.textContent;
    copyBtn.textContent = "\u5df2\u590d\u5236 \u2713";
    setTimeout(() => { copyBtn.textContent = original; }, 1400);
  } catch (e) {
    outStatus.textContent = "\u590d\u5236\u5931\u8d25\uff0c\u8bf7\u624b\u52a8\u9009\u4e2d\u590d\u5236";
  }
});

// ============================================================
// Full-build transcoder: CN character JSON -> PoB build code
// ============================================================

// ImportTab.lua:1494 (slotMap)
const SLOT_MAP = {
  Weapon: "Weapon 1", Offhand: "Weapon 2", Weapon2: "Weapon 1 Swap", Offhand2: "Weapon 2 Swap",
  Helm: "Helmet", BodyArmour: "Body Armour", Gloves: "Gloves", Boots: "Boots",
  Amulet: "Amulet", Ring: "Ring 1", Ring2: "Ring 2", Ring3: "Ring 3", Belt: "Belt",
  BrequelGrafts: "Graft 1", BrequelGrafts2: "Graft 2",
};

function xmlEscape(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function xmlAttrs(attrib) {
  return Object.entries(attrib)
    .filter(([, v]) => v !== undefined && v !== null)
    .map(([k, v]) => ` ${k}="${xmlEscape(v)}"`)
    .join("");
}

// { name: "[Intangibility|\u865a\u5316]", ... } -> "\u865a\u5316"
function propertyDisplayName(name) {
  const m = name.match(/^\[.+\|(.+)\]$/);
  return m ? m[1] : name;
}

// Reconstructs a single "\u54c1\u8d28: {0} (augmented)"-style property line
// from a properties[] entry, substituting {n} placeholders (displayMode 3,
// e.g. flask duration/charge lines) with their values in order.
function propertyLineText(property) {
  const name = propertyDisplayName(property.name);
  const values = property.values || [];
  if (name.includes("{")) {
    // "武器范围：{0} 米" -> label "武器范围" + bare value "1.4": PoB's
    // Weapon Range (and similar single-value fields) expects a bare number,
    // not the CN unit suffix baked into the display template.
    const labelMatch = name.match(/^(.+?)[:：]\s*\{0\}/);
    if (labelMatch && values.length === 1) {
      return labelMatch[1] + ": " + values[0][0];
    }
    return name.replace(/\{(\d+)\}/g, (m, i) => {
      const v = values[Number(i)];
      return v ? v[0] : m;
    });
  }
  if (values.length === 0) return name;
  return name + ": " + values.map((v) => v[0]).join(", ");
}

// sockets: [{group, sColour}] -> "B-W B" (Item.lua Sockets format: '-' links
// within a group, ' ' separates groups)
function formatSockets(sockets) {
  const groups = [];
  let curGroup = null;
  let curParts = [];
  for (const s of sockets) {
    if (curGroup !== null && s.group !== curGroup) {
      groups.push(curParts.join("-"));
      curParts = [];
    }
    curGroup = s.group;
    curParts.push(s.sColour);
  }
  if (curParts.length) groups.push(curParts.join("-"));
  return groups.join(" ");
}

// Builds one <Item id="N">...</Item> element (English raw text as content)
// directly from a JSON item's structured fields, reusing the same
// translateItemLine()/translateModLine() helpers convertItem() uses for
// pasted single-item text - but calling them per already-known field/mod
// instead of reconstructing then re-splitting fake CN clipboard text. This
// matters for mod descriptions specifically: a JSON description can itself
// contain embedded newlines (multi-line stats, e.g. Timeless Jewel notables),
// and statDescriptions.csv stores those multi-line stats as a single
// template with the newlines embedded - splitting them into separate lines
// first (as re-parsing reconstructed text would) breaks that lookup.
function buildItemElement(itemData, id) {
  const out = [];
  const misses = [];

  out.push("Rarity: " + (itemData.rarity || "Rare"));
  const baseNameEn = BASE_DICT[itemData.typeLine] || itemData.typeLine;
  out.push(baseNameEn);
  if (itemData.name) out.push(baseNameEn);

  const pushLine = (cnLine) => {
    const result = translateItemLine(cnLine);
    if (result.drop) return;
    if (result.text !== undefined) { if (result.text) out.push(result.text); return; }
    out.push("# UNTRANSLATED: " + result.miss + (result.enchantSuffix || ""));
    misses.push(result.miss);
  };
  // Mod descriptions may be multi-line (embedded \n) - try the whole
  // description as one template lookup first (matches how multi-line
  // stats are stored in statDescriptions.csv), then fall back to
  // translating each physical line separately.
  const pushModLine = (desc, enchantSuffix) => {
    const res = translateModLine(desc);
    if (res.ok) { if (res.text) out.push(res.text + enchantSuffix); return; }
    for (const singleLine of desc.split(/\r?\n/)) {
      if (singleLine.trim()) pushLine(singleLine.trim() + enchantSuffix);
    }
  };

  if (itemData.properties && itemData.properties.length) {
    out.push("--------");
    for (const p of itemData.properties) pushLine(propertyLineText(p));
  }
  if (itemData.requirements && itemData.requirements.length) {
    out.push("--------");
    out.push("Requirements:");
    for (const r of itemData.requirements) {
      if (r.values && r.values[0]) pushLine(r.name + ": " + r.values[0][0]);
    }
  }
  if (itemData.sockets && itemData.sockets.length) {
    out.push("--------");
    out.push("Sockets: " + formatSockets(itemData.sockets));
  }
  if (itemData.ilvl) {
    out.push("--------");
    out.push("Item Level: " + itemData.ilvl);
  }
  if (itemData.enchantMods && itemData.enchantMods.length) {
    out.push("--------");
    for (const m of itemData.enchantMods) pushModLine(m, " (enchant)");
  }
  if (itemData.implicitMods && itemData.implicitMods.length) {
    out.push("--------");
    for (const m of itemData.implicitMods) pushModLine(m.description || m, "");
  }
  const explicitDescs = (itemData.explicitMods || []).map((m) => m.description || m);
  const flags = [];
  if (itemData.corrupted) flags.push("Corrupted");
  if (itemData.fractured) flags.push("Fractured Item");
  if (itemData.duplicated || itemData.mirrored) flags.push("Mirrored");
  if (explicitDescs.length || flags.length) {
    out.push("--------");
    for (const m of explicitDescs) pushModLine(m, "");
    for (const f of flags) out.push(f);
  }

  const displayName = itemData.name || itemData.typeLine;
  const xml = `<Item id="${id}">\n${xmlEscape(out.join("\n"))}\n</Item>`;
  return { xml, misses, displayName, id };
}

function normaliseParens(s) {
  return s.replace(/\uff08/g, "(").replace(/\uff09/g, ")");
}

// typeLine (or hybrid.baseTypeName for transfigured/dual gems) -> English
// gem display name PoB's gemForBaseName expects, with " Support" appended
// for support gems (Data.lua:1099-1101: PoB stores support gems under
// "<name> Support" except SupportBarrage).
function lookupGemName(gemTypeLine, isSupport) {
  const key = normaliseParens(gemTypeLine).replace(/\s*\(\u8f85\)\s*$/, "").trim();
  let en = GEM_DICT[normaliseParens(gemTypeLine)] || GEM_DICT[key];
  if (!en) return null;
  if (isSupport && !/ Support$/.test(en) && en !== "Barrage") en += " Support";
  return en;
}

// Walks one item's socketedItems[], returning gem <Gem> XML per (colour)
// socket group and any abyss jewels as separate importable items.
function collectSocketedGems(itemData, slotName, state) {
  if (!itemData.sockets || !itemData.socketedItems) return;
  const groupOf = {};
  itemData.sockets.forEach((s, i) => { groupOf[i] = s.group; });
  const gemsByGroup = {};
  for (const socketedItem of itemData.socketedItems) {
    if (socketedItem.abyssJewel) {
      state.itemCounter++;
      const el = buildItemElement(socketedItem, state.itemCounter);
      state.itemXmls.push(el.xml);
      state.misses.push(...el.misses.map((m) => `[${el.displayName}] ${m}`));
      state.slots.push({ name: `${slotName} Abyssal Socket ${state.abyssalCount++}`, itemId: el.id });
      continue;
    }
    const typeLine = socketedItem.hybrid ? socketedItem.hybrid.baseTypeName : socketedItem.typeLine;
    const gemName = lookupGemName(typeLine, !!socketedItem.support);
    if (!gemName) {
      state.misses.push(`[\u6280\u80fd\u77f3] ${typeLine} \uff08\u672a\u80fd\u8bc6\u522b\uff0c\u8bf7\u624b\u52a8\u6dfb\u52a0\uff09`);
      continue;
    }
    let level = 20, quality = 0;
    for (const p of socketedItem.properties || []) {
      const name = propertyDisplayName(p.name);
      if (name === "\u7b49\u7ea7" && p.values && p.values[0]) level = parseInt(p.values[0][0], 10) || level;
      else if (name === "\u54c1\u8d28" && p.values && p.values[0]) quality = parseInt(p.values[0][0], 10) || 0;
    }
    const group = groupOf[socketedItem.socket];
    const key = slotName + "#" + group;
    if (!gemsByGroup[key]) gemsByGroup[key] = { slot: slotName, gems: [] };
    gemsByGroup[key].gems.push({ nameSpec: gemName, level, quality });
  }
  for (const g of Object.values(gemsByGroup)) state.skillGroups.push(g);
}

// Parses the CN character-export JSON and assembles a PoB build code
// (Deflate + base64url, matching ImportTab.lua:505's encode).
function generateBuildCode(jsonText) {
  const data = JSON.parse(jsonText);
  const mainItems = (data.items && data.items.items) || [];
  const passives = data.passiveSkills || {};
  const treeItems = passives.items || [];

  const state = { itemCounter: 0, itemXmls: [], slots: [], misses: [], skillGroups: [], abyssalCount: 1 };

  for (const itemData of mainItems) {
    let slotName = null;
    if (itemData.inventoryId === "Flask") slotName = "Flask " + (itemData.x + 1);
    else slotName = SLOT_MAP[itemData.inventoryId];
    if (!slotName) continue; // not an equipped/known slot (e.g. inventory clutter)

    state.itemCounter++;
    const el = buildItemElement(itemData, state.itemCounter);
    state.itemXmls.push(el.xml);
    state.misses.push(...el.misses.map((m) => `[${el.displayName}] ${m}`));
    state.slots.push({ name: slotName, itemId: el.id });
    state.abyssalCount = 1;
    collectSocketedGems(itemData, slotName, state);
  }

  // Tree jewels: imported as items but not auto-socketed (see bd-caveat note).
  const looseJewelNote = [];
  for (const itemData of treeItems) {
    state.itemCounter++;
    const el = buildItemElement(itemData, state.itemCounter);
    state.itemXmls.push(el.xml);
    state.misses.push(...el.misses.map((m) => `[${el.displayName}] ${m}`));
    looseJewelNote.push(el.displayName);
  }

  // --- Skills ---
  let skillsXml = `<Skills activeSkillSet="1" sortGemsByDPS="true" defaultGemLevel="20" defaultGemQuality="0">\n<SkillSet id="1" title="Default">\n`;
  for (const group of state.skillGroups) {
    skillsXml += `<Skill enabled="true" slot="${xmlEscape(group.slot)}" mainActiveSkill="1">\n`;
    for (const gem of group.gems) {
      skillsXml += `<Gem nameSpec="${xmlEscape(gem.nameSpec)}" level="${gem.level}" quality="${gem.quality}" enabled="true"/>\n`;
    }
    skillsXml += `</Skill>\n`;
  }
  skillsXml += `</SkillSet>\n</Skills>`;

  // --- Tree (PassiveSpec.lua:200-210; classId/ascendClassId are the raw
  // numeric codes already, confirmed to match PoB's own 0-indexed scheme) ---
  const masteryEffects = Object.entries(passives.mastery_effects || {})
    .map(([node, effect]) => `{${node},${effect}}`).join(",");
  const nodes = (passives.hashes || []).join(",");
  const treeXml = `<Tree activeSpec="1">\n<Spec title="Default" classId="${passives.character}" ascendClassId="${passives.ascendancy}" nodes="${nodes}" masteryEffects="${xmlEscape(masteryEffects)}">\n<Sockets/>\n</Spec>\n</Tree>`;

  // --- Items ---
  let itemsXml = `<Items activeItemSet="1">\n` + state.itemXmls.join("\n") + `\n<ItemSet id="1" title="Default">\n`;
  for (const slot of state.slots) itemsXml += `<Slot name="${xmlEscape(slot.name)}" itemId="${slot.itemId}"/>\n`;
  itemsXml += `</ItemSet>\n</Items>`;

  // --- Build ---
  const buildXml = `<Build level="1" mainSocketGroup="1" targetVersion="3_29" bandit="None" pantheonMajorGod="None" pantheonMinorGod="None"/>`;

  const fullXml = `<PathOfBuilding>\n${buildXml}\n${skillsXml}\n${treeXml}\n${itemsXml}\n<Config/>\n</PathOfBuilding>`;

  const compressed = pako.deflate(fullXml);
  let binary = "";
  const chunkSize = 0x8000;
  for (let i = 0; i < compressed.length; i += chunkSize) {
    binary += String.fromCharCode.apply(null, compressed.subarray(i, i + chunkSize));
  }
  let b64 = btoa(binary).replace(/\+/g, "-").replace(/\//g, "_");

  return { code: b64, misses: state.misses, itemCount: state.itemXmls.length, gemCount: state.skillGroups.reduce((a, g) => a + g.gems.length, 0), looseJewels: looseJewelNote, xml: fullXml };
}

const bdInputEl = document.getElementById("bdInput");
const bdOutputEl = document.getElementById("bdOutput");
const bdConvertBtn = document.getElementById("bdConvertBtn");
const bdCopyBtn = document.getElementById("bdCopyBtn");
const bdStatus = document.getElementById("bdStatus");
const bdReport = document.getElementById("bdReport");
const bdReportTitle = document.getElementById("bdReportTitle");
const bdReportList = document.getElementById("bdReportList");

bdConvertBtn.addEventListener("click", () => {
  bdReport.classList.remove("show");
  bdOutputEl.value = "";
  bdCopyBtn.disabled = true;
  try {
    const result = generateBuildCode(bdInputEl.value);
    bdOutputEl.value = result.code;
    bdCopyBtn.disabled = false;
    bdStatus.textContent = `${result.itemCount} \u4ef6\u88c5\u5907\uff0c${result.gemCount} \u9897\u6280\u80fd\u77f3` + (result.misses.length ? `\uff0c${result.misses.length} \u5904\u672a\u5339\u914d` : "\uff0c\u5168\u90e8\u5339\u914d");
    bdStatus.className = result.misses.length ? "status-line warn" : "status-line ok";
    if (result.misses.length || result.looseJewels.length) {
      bdReportTitle.textContent = "\u9700\u8981\u624b\u52a8\u6838\u5bf9\u7684\u5185\u5bb9";
      bdReportList.innerHTML = "";
      result.misses.forEach((m) => {
        const li = document.createElement("li");
        li.className = "miss-line";
        li.textContent = m;
        bdReportList.appendChild(li);
      });
      result.looseJewels.forEach((name) => {
        const li = document.createElement("li");
        li.textContent = `\u5929\u8d4b\u6811\u73e0\u5b9d\u9700\u8981\u624b\u52a8\u62d6\u5165\u63d2\u69fd: ${name}`;
        bdReportList.appendChild(li);
      });
      bdReport.classList.add("show");
    }
  } catch (e) {
    bdStatus.textContent = "\u751f\u6210\u5931\u8d25: " + e.message;
    bdStatus.className = "status-line warn";
  }
});
bdCopyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(bdOutputEl.value);
    const original = bdCopyBtn.textContent;
    bdCopyBtn.textContent = "\u5df2\u590d\u5236 \u2713";
    setTimeout(() => { bdCopyBtn.textContent = original; }, 1400);
  } catch (e) {
    bdStatus.textContent = "\u590d\u5236\u5931\u8d25\uff0c\u8bf7\u624b\u52a8\u9009\u4e2d\u590d\u5236";
  }
});
</script>
"""

html = (
    TEMPLATE.replace("MOD_DICT_PLACEHOLDER", mod_dict_json)
    .replace("BASE_DICT_PLACEHOLDER", base_dict_json)
    .replace("NOTABLE_DICT_PLACEHOLDER", notable_dict_json)
    .replace("GEM_DICT_PLACEHOLDER", gem_dict_json)
    .replace("PAKO_SOURCE_PLACEHOLDER", pako_source)
)

os.makedirs(DIST_DIR, exist_ok=True)
out_path = os.path.join(DIST_DIR, "poe_item_decoder.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("written", out_path, "size bytes", os.path.getsize(out_path))
