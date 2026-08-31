# -*- coding: utf-8 -*-
"""
把 build_dict.py 生成的两份字典内嵌进单文件 HTML 页面。
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

mod_dict_json = json.dumps(mod_dict, ensure_ascii=False, separators=(",", ":"))
base_dict_json = json.dumps(base_dict, ensure_ascii=False, separators=(",", ":"))

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
</div>

<script>
const MOD_DICT = MOD_DICT_PLACEHOLDER;
const BASE_DICT = BASE_DICT_PLACEHOLDER;

const CLASS_MAP = {
  "头盔":"Helmet","胸甲":"Body Armour","护手":"Gloves","手套":"Gloves","鞋子":"Boots","靴子":"Boots",
  "盾牌":"Shield","腰带":"Belt","项链":"Amulet","戒指":"Ring","箭袋":"Quiver",
  "匕首":"Dagger","短剑":"Dagger","单手剑":"One Hand Sword","双手剑":"Two Hand Sword",
  "细剑":"Thrusting One Hand Sword","单手斧":"One Hand Axe","双手斧":"Two Hand Axe",
  "单手锤":"One Hand Mace","双手锤":"Two Hand Mace","权杖":"Sceptre","法杖":"Staff",
  "长杖":"Warstaff","弓":"Bow","法器":"Wand","鱼竿":"Fishing Rod",
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

function lookupTemplate(template) {
  let hit = MOD_DICT[template];
  if (hit !== undefined) return hit;
  for (const [from, to] of SYNONYM_SWAPS) {
    if (template.includes(from)) {
      hit = MOD_DICT[template.split(from).join(to)];
      if (hit !== undefined) return hit;
    }
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
  return (t.startsWith("{") && t.endsWith("}")) ||
         (t.startsWith("(") && t.endsWith(")")) ||
         (t.startsWith("\uFF08") && t.endsWith("\uFF09"));
}

function stripLabelSpaces(s) {
  return s.replace(/\s+/g, "");
}

function convertItem(raw) {
  const lines = raw.split(/\r?\n/).map((l) => l.trim()).filter((l) => l.length > 0);
  const out = [];
  const misses = [];
  let rarity = null;
  let i = 0;

  // Splits a line on the first colon (half- or full-width), returning
  // [label-with-internal-whitespace-stripped, value-from-original-text].
  // Using the original text for the value preserves real spacing (e.g. "196 (augmented)").
  const splitLabel = (line) => {
    const idx = line.search(/[:\uff1a]/);
    if (idx === -1) return [stripLabelSpaces(line), null];
    return [stripLabelSpaces(line.slice(0, idx)), line.slice(idx + 1).trim()];
  };

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

  const LABEL_MAP = {
    "\u54c1\u8d28": "Quality", "\u62a4\u7532": "Armour", "\u95ea\u907f\u503c": "Evasion Rating",
    "\u80fd\u91cf\u62a4\u76fe": "Energy Shield", "\u865a\u5316": "Ward", "\u7b49\u7ea7": "Level", "\u529b\u91cf": "Strength",
    "\u654f\u6377": "Dexterity", "\u667a\u6167": "Intelligence", "\u7269\u54c1\u7b49\u7ea7": "Item Level",
    "\u4ec5\u9650": "Limited to", "\u8303\u56f4": "Radius",
  };
  const FIXED_LINES = {
    "\u9700\u6c42:": "Requirements:", "\u5df2\u8150\u5316": "Corrupted", "\u5df2\u590d\u5236": "Mirrored",
    "\u672a\u9274\u5b9a": "Unidentified", "\u5206\u88c2": "Split", "\u711a\u754c\u8005\u7269\u54c1": "Searing Exarch Item",
    "\u706d\u754c\u8005\u7269\u54c1": "Eater of Worlds Item",
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

  // Translate a single logical line (already stripped of any trailing
  // " (enchant)" tag and any "X \u2014 \u6570\u503c\u4e0d\u53ef\u8c03\u6574" annotation suffix).
  function translateLine(line) {
    if (isBracketLine(line)) return { drop: true };

    const flaskState = translateFlaskStateLine(line);
    if (flaskState !== null) return { text: flaskState };

    const [label, value] = splitLabel(line);
    const compact = stripLabelSpaces(line);

    if (DROP_LINES.has(compact)) return { drop: true };

    if (label === "\u63d2\u69fd" && value !== null) {
      return { text: "Sockets: " + value };
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

  // Remaining lines
  for (; i < lines.length; i++) {
    let line = lines[i];
    if (line === "--------") { out.push(line); continue; }

    // Cluster Jewel lines granted "by the jewel itself" carry a literal
    // " (enchant)" tag (kept in English even in the CN client) - strip it
    // before matching, then reattach it to whatever the line translates to.
    let enchantSuffix = "";
    const enchantMatch = line.match(/^(.*)\s\(enchant\)$/);
    if (enchantMatch) {
      line = enchantMatch[1];
      enchantSuffix = " (enchant)";
    }

    // "X \u2014 \u6570\u503c\u4e0d\u53ef\u8c03\u6574": a client-side annotation noting a value can't be
    // modified by quality/catalysts. Not a field PoB's parser or unique
    // database recognises - strip the annotation, keep translating the rest.
    const annotationMatch = line.match(/^(.*?)\s*\u2014\s*\u6570\u503c\u4e0d\u53ef\u8c03\u6574\s*$/);
    if (annotationMatch) line = annotationMatch[1];
    if (!line) continue;

    const result = translateLine(line);
    if (result.drop) continue;
    if (result.text !== undefined) {
      if (result.text) out.push(result.text + enchantSuffix);
      continue;
    }
    out.push("# UNTRANSLATED: " + result.miss + enchantSuffix);
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
</script>
"""

html = TEMPLATE.replace("MOD_DICT_PLACEHOLDER", mod_dict_json).replace("BASE_DICT_PLACEHOLDER", base_dict_json)

os.makedirs(DIST_DIR, exist_ok=True)
out_path = os.path.join(DIST_DIR, "poe_item_decoder.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("written", out_path, "size bytes", os.path.getsize(out_path))
