"""
从 PoeCharm 的汉化数据集里编译出两份精简字典：
  build/mod_dict.json  —— 词条文本模板 中文->英文（数据源：statDescriptions.csv）
  build/base_dict.json —— 基底物品名 中文->英文（数据源：Items_*.txt.csv）

用法：
  python build_dict.py --poecharm-data "D:\\PoeCharm\\Data\\Translate\\zh-rCN"

不传 --poecharm-data 的话，默认尝试同目录下的 poecharm_data/（需要自己把
PoeCharm 安装目录里的 Data/Translate/zh-rCN 整个文件夹复制/软链到这里）。
生成的 JSON 不提交进仓库，是 gen_html.py 的中间产物。
"""
import argparse
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "build")

ITEM_BASE_FILES = [
    "Items_Armour.txt.csv", "Items_Weapons.txt.csv", "Items_Accessories.txt.csv",
    "Items_Jewels.txt.csv", "Items_Flasks.txt.csv", "Items_Gems.txt.csv",
]


def load_csv_pairs(base_dir, fname):
    pairs = []
    path = os.path.join(base_dir, fname)
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                pairs.append((row[0].strip(), row[1].strip()))
    return pairs


def build_mod_dict(base_dir):
    sd_pairs = load_csv_pairs(base_dir, "statDescriptions.csv")
    print("statDescriptions rows:", len(sd_pairs))

    mod_dict = {}
    ambiguous = 0
    for en, zh in sd_pairs:
        zh_norm = zh.replace("\\n", "\n")
        en_norm = en.replace("\\n", "\n")
        if zh_norm not in mod_dict:
            mod_dict[zh_norm] = en_norm
        elif mod_dict[zh_norm] != en_norm:
            ambiguous += 1
            # 同一句中文对应多条不同英文时，优先保留带{N}占位符的模板版本
            has_ph_existing = "{0}" in mod_dict[zh_norm]
            has_ph_new = "{0}" in en_norm
            if has_ph_new and not has_ph_existing:
                mod_dict[zh_norm] = en_norm

    print("unique CN templates:", len(mod_dict))
    print("ambiguous collisions seen (kept the placeholder version):", ambiguous)
    return mod_dict


def build_base_dict(base_dir):
    base_dict = {}
    for fn in ITEM_BASE_FILES:
        try:
            for en, zh in load_csv_pairs(base_dir, fn):
                base_dict.setdefault(zh, en)
        except FileNotFoundError:
            print("missing (skipped):", fn)
    print("base type names:", len(base_dict))
    return base_dict


def build_notable_dict(base_dir):
    # Passive tree node display names (notables/keystones/etc) - needed to
    # translate anoint enchant lines ("Allocates <Notable Name>").
    notable_dict = {}
    for en, zh in load_csv_pairs(base_dir, "tree_dn.csv"):
        notable_dict.setdefault(zh, en)
    print("tree node display names:", len(notable_dict))
    return notable_dict


def _normalise_parens(s):
    return s.replace("（", "(").replace("）", ")")


def build_gem_dict(base_dir):
    # Gem base names (incl. transfigured variants and " Support" gems) -
    # needed for the full-build importer to identify gems by their JSON
    # typeLine/hybrid.baseTypeName. Paren width is normalised because the
    # game client's typeLine uses half-width "(辅)" while some CSV rows use
    # full-width "（辅）".
    gem_dict = {}
    for fn in ("Gems_data.txt.csv", "Items_Gems.txt.csv"):
        try:
            for en, zh in load_csv_pairs(base_dir, fn):
                gem_dict.setdefault(_normalise_parens(zh), en)
        except FileNotFoundError:
            print("missing (skipped):", fn)
    print("gem names:", len(gem_dict))
    return gem_dict


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--poecharm-data",
        default=os.path.join(HERE, "poecharm_data"),
        help="PoeCharm 的 Data/Translate/zh-rCN 目录路径",
    )
    args = parser.parse_args()

    base_dir = args.poecharm_data
    if not os.path.isdir(base_dir):
        raise SystemExit(
            "找不到 PoeCharm 汉化数据目录: {}\n"
            "请用 --poecharm-data 指定你本机 PoeCharm 安装目录下的 "
            "Data/Translate/zh-rCN 完整路径。".format(base_dir)
        )

    os.makedirs(BUILD_DIR, exist_ok=True)

    mod_dict = build_mod_dict(base_dir)
    base_dict = build_base_dict(base_dir)
    notable_dict = build_notable_dict(base_dir)
    gem_dict = build_gem_dict(base_dir)

    mod_path = os.path.join(BUILD_DIR, "mod_dict.json")
    base_path = os.path.join(BUILD_DIR, "base_dict.json")
    notable_path = os.path.join(BUILD_DIR, "notable_dict.json")
    gem_path = os.path.join(BUILD_DIR, "gem_dict.json")
    with open(mod_path, "w", encoding="utf-8") as f:
        json.dump(mod_dict, f, ensure_ascii=False)
    with open(base_path, "w", encoding="utf-8") as f:
        json.dump(base_dict, f, ensure_ascii=False)
    with open(notable_path, "w", encoding="utf-8") as f:
        json.dump(notable_dict, f, ensure_ascii=False)
    with open(gem_path, "w", encoding="utf-8") as f:
        json.dump(gem_dict, f, ensure_ascii=False)

    print("mod_dict.json:", os.path.getsize(mod_path), "bytes ->", mod_path)
    print("base_dict.json:", os.path.getsize(base_path), "bytes ->", base_path)
    print("notable_dict.json:", os.path.getsize(notable_path), "bytes ->", notable_path)
    print("gem_dict.json:", os.path.getsize(gem_path), "bytes ->", gem_path)


if __name__ == "__main__":
    main()
