from collections import defaultdict


def main():
    # ====================== 1. 自定义数据（需用户修改） ======================
    # 精灵属性：key=精灵名，value=属性集合（单属性1个元素，双属性2个元素）
    spirits = {
        "月牙雪熊": {"冰", "幻"},
        "燃薪虫": {"火", "草"},
        "空空颅": {"幽"},
        "粉星仔": {"幻"},
        "窃光蚊": {"恶", "光"},
        "双灯鱼": {"水", "电"},
        "贝瑟": {"钢", "火"},
        "粉粉星": {"电", "幻"},
        # 以下非稀有
        "恶魔狼": {"恶"},
        "治愈兔": {"火", "萌"},
        "奇丽花": {"草"},
        "格兰球": {"草"},
        "机械方方": {"钢"},
        "酷拉": {"电"},
        "大耳兜兜": {"冰", "萌"},
        "呼呼猪": {"冰", "地"},
        "犀角鸟": {"光"},
        "丹雅鬃": {"火"},
    }

    spirits_tree = {
        "小翼龙": {"龙", "翼"},
        "噼啪鸟": {"电", "翼"},
        "水一水蓝蓝": {"水"},
        "草二松仔": {"草", "武"},
        "深蓝鲸": {"水"},
        "裘洛": {"毒"},
        "多西": {"钢", "地"},
        "咔咔羽毛": {"翼", "普"},
        "伊雷龙": {"龙"},
        "厉毒小萝": {"毒", "恶"},
        "墨鱿士": {"幽"},
        "布鲁斯": {"冰"},
        "小黑猫": {"普"},
        "可爱猿": {"火"},
        "圣剑侍从": {"钢"},
        "仪使者": {"地", "幻"},
        "罗隐": {"地"},
        "春团": {"草"},
        "忽幽狸": {"幽", "毒"},
        "脆筒甜甜": {"冰"},
        "小星光": {"电", "光"},
        "闪电环": {"电"},
        "哭哭菇": {"幻"},
        "海枝枝": {"水", "幽"},
        "兽花蕾": {"草", "光"},
        "毛头小蛛": {"地", "虫"},
        "画精灵": {"普"},
        "书卷魔": {"普"},
        "绿草精灵": {"草", "幻"},
        "小夜": {"恶"},
        "呆小路": {"草", "萌"},
        "雪娃娃": {"冰"},
        "小箱怪": {"幻", "钢"},
        "棋棋": {"地", "武"},
        "小狮鹫": {"翼"},
    }
    spirits_new = {}
    for key, value in spirits.items():
        # if key in ["月牙雪熊", "燃薪虫", "空空颅", "粉星仔", "窃光蚊", "双灯鱼", "贝瑟", "粉粉星"]:
        #     spirits_new[key] = {"属性": value, "稀有性": "稀有", "赛季": "本赛季"}
        #     pass
        # else:
        spirits_new[key] = {"属性": value, "稀有性": "非稀有", "赛季": "本赛季"}

    for key, value in spirits_tree.items():
        spirits_new[key] = {"属性": value, "稀有性": "非稀有", "赛季": "非本赛季"}

    # print(spirits_new)
    spirits = spirits_new

    # 相宜规则：用frozenset存储无序对（如"冰+火"等价于"火+冰"）
    compatibility_rules = {
        frozenset({"冰", "火"}),
        frozenset({"草", "光"}),
        frozenset({"地", "虫"}),
        frozenset({"水", "翼"}),
        frozenset({"萌", "普"}),
        frozenset({"龙", "武"}),
        frozenset({"幽", "恶"}),
        frozenset({"幻", "钢"}),
        frozenset({"电", "毒"}),
        # ... 补充其他规则
    }

    max_habitat_size = 2  # 容量约束（≤2）
    prioritize_rare_type = "非稀有"  # 稀有性优先类型（软目标）
    # ====================== 2. 计算所有精灵对的相宜规则计数 ======================
    spirit_list = list(spirits.keys())
    comp_count = defaultdict(dict)  # comp_count[u][v] = 计数

    for i in range(len(spirit_list)):
        u = spirit_list[i]
        u_attrs = spirits[u]["属性"]
        for j in range(i + 1, len(spirit_list)):
            v = spirit_list[j]
            v_attrs = spirits[v]["属性"]

            count = 0
            for s in u_attrs:
                for t in v_attrs:
                    if s == t or frozenset({s, t}) in compatibility_rules:
                        count += 1
            comp_count[u][v] = count
            comp_count[v][u] = count

    # ====================== 3. 贪心配对（新增“本赛季优先”） ======================
    # 节点排序：本赛季→非本赛季 → 非稀有→稀有 → 高计数→低计数
    def sort_key(spirit):
        season_priority = 0 if spirits[spirit]["赛季"] == "本赛季" else 1
        rare_priority = 0 if spirits[spirit]["稀有性"] == prioritize_rare_type else 1
        max_count = max(comp_count[spirit].values()) if comp_count[spirit] else 0
        return (season_priority, rare_priority, -max_count)

    sorted_spirits = sorted(spirit_list, key=sort_key)
    matched = set()
    habitats = []

    for i in range(len(sorted_spirits)):
        u = sorted_spirits[i]
        if u in matched:
            continue

        best_partner = None
        best_priority = None
        best_count = -1

        # 寻找最佳伙伴（同赛季→同稀有性→高计数）
        for j in range(i + 1, len(sorted_spirits)):
            v = sorted_spirits[j]
            if v in matched:
                continue

            current_count = comp_count[u][v]
            if current_count == 0:
                continue  # 不相宜，跳过

            is_same_season = (spirits[u]["赛季"] == spirits[v]["赛季"])
            is_same_rare = (spirits[u]["稀有性"] == spirits[v]["稀有性"])
            priority = (not is_same_season, not is_same_rare, -current_count)

            if best_partner is None or priority < best_priority:
                best_partner = v
                best_priority = priority
                best_count = current_count

        # 配对或单只成栖息地
        if best_partner is not None:
            habitats.append([u, best_partner])
            matched.add(u)
            matched.add(best_partner)
        else:
            habitats.append([u])
            matched.add(u)

    # ====================== 4. 输出结果（含赛季分布） ======================
    total_count = 0
    print(f"=== 栖息地数量：{len(habitats)}（容量≤{max_habitat_size}） ===")
    print(f"=== 优先规则：本赛季配对＞{prioritize_rare_type}聚集＞高相宜计数 ===")

    for idx, members in enumerate(habitats, 1):
        if len(members) == 2:
            u, v = members
            count = comp_count[u][v]
            total_count += count
            season_types = f"{spirits[u]['赛季']}+{spirits[v]['赛季']}"
            rare_types = f"{spirits[u]['稀有性']}+{spirits[v]['稀有性']}"
            print(f"\n--- 栖息地{idx}（2只精灵，计数：{count}，赛季：{season_types}，稀有性：{rare_types}） ---")
            print(f"精灵列表：{u}（{spirits[u]['属性']}）、{v}（{spirits[v]['属性']}）")
        else:
            member = members[0]
            print(f"\n--- 栖息地{idx}（1只精灵，赛季：{spirits[member]['赛季']}，稀有性：{spirits[member]['稀有性']}） ---")
            print(f"精灵列表：{member}（{spirits[member]['属性']}）")

    print(f"\n=== 总相宜规则计数：{total_count} ===")

    return habitats, total_count


if __name__ == "__main__":
    main()