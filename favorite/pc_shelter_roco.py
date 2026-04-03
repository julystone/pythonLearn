from collections import defaultdict


def main():
    # ====================== 1. 自定义数据（需用户修改） ======================
    # 精灵属性：key=精灵名，value=属性集合（单属性1个元素，双属性2个元素）
    spirits = {
        "月牙雪熊": {"冰", "幻"},
        "燃薪虫": {"火", "幻"},
        "空空颅": {"幽"},
        "粉星仔": {"幻"},
        "窃光蚊": {"恶", "光"},
        "陨星虫": {"虫"},
        "利灯鱼": {"水", "电"},
        "贝瑟": {"钢", "火"},
        "小皮球": {"电", "幻"},
        "丹雅鬃": {"火"},
        "恶魔狼": {"恶"},
        "治愈兔": {"火", "萌"},
        "奇丽花": {"草"},
        "格兰球": {"草"},
        "立方人": {"钢"},
        "酷拉": {"电"},
        "雪影娃娃": {"冰", "萌"},
        "呼呼猪": {"冰", "地"},
        "犀角鸟": {"光"},
    }
    spirits_new = {}
    for key, value in spirits.items():
        if key in ["月牙雪熊", "燃薪虫", "空空颅", "粉星仔", "窃光蚊", "陨星虫", "利灯鱼", "贝瑟", "小皮球"]:
            spirits_new[key] = {"属性": value, "稀有性": "稀有"}
        else:
            spirits_new[key] = {"属性": value, "稀有性": "非稀有"}

    print(spirits_new)
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

    max_habitat_size = 2  # 每个栖息地最多2只精灵（容量约束）
    prioritize_rare_type = "非稀有"  # 优先聚集的类型（可改为"稀有"）

    # ====================== 2. 构建相宜图与冲突图（不变，含同属性相宜） ======================
    comp_graph = defaultdict(set)  # 相宜图：精灵→相宜精灵集合
    conflict_graph = defaultdict(set)  # 冲突图：精灵→冲突精灵集合
    spirit_list = list(spirits.keys())

    for i in range(len(spirit_list)):
        u = spirit_list[i]
        u_attrs = spirits[u]["属性"]
        u_rare = spirits[u]["稀有性"]  # 新增：获取稀有性
        for j in range(i+1, len(spirit_list)):
            v = spirit_list[j]
            v_attrs = spirits[v]["属性"]
            v_rare = spirits[v]["稀有性"]  # 新增：获取稀有性

            # 相宜性判断（含同属性相宜：s==t 或 符合规则）
            is_compatible = False
            for s in u_attrs:
                for t in v_attrs:
                    if s == t or frozenset({s, t}) in compatibility_rules:
                        is_compatible = True
                        break
                if is_compatible:
                    break

            # 更新相宜图/冲突图（不变）
            if is_compatible:
                comp_graph[u].add(v)
                comp_graph[v].add(u)
            else:
                conflict_graph[u].add(v)
                conflict_graph[v].add(u)

    # ====================== 3. 带“非稀有优先聚集”的贪心着色算法（核心修改） ======================
    # ---------------------- 修改1：节点排序（非稀有优先，再按冲突度数降序） ----------------------
    def sort_key(spirit):
        # 非稀有优先（优先级0 < 1）
        rare_priority = 0 if spirits[spirit]["稀有性"] == prioritize_rare_type else 1
        conflict_degree = len(conflict_graph[spirit])  # 冲突度数（不相宜精灵数量）
        return (rare_priority, -conflict_degree)  # 先按稀有性升序（非稀有在前），再按冲突度数降序

    sorted_spirits = sorted(spirit_list, key=sort_key)

    # ---------------------- 修改2：颜色分配（优先同类型聚集） ----------------------
    color_assignments = {}  # 精灵→栖息地编号（颜色）
    color_info = defaultdict(
        lambda: {"members": [], "rare_type": None})  # 栖息地信息：成员列表、主要稀有类型

    for spirit in sorted_spirits:
        s_rare = spirits[spirit]["稀有性"]  # 当前精灵稀有性
        s_conflicts = conflict_graph[spirit]  # 当前精灵的冲突精灵

        # 步骤1：筛选可用栖息地（排除冲突精灵所在栖息地 + 容量已满栖息地）
        available_colors = []
        for color, info in color_info.items():
            if len(info["members"]) >= max_habitat_size:
                continue  # 容量已满，跳过
            if any(neighbor in info["members"] for neighbor in s_conflicts):
                continue  # 栖息地有冲突精灵，跳过
            available_colors.append(color)

        # 步骤2：优先选择“同稀有类型”的栖息地（核心优化）
        preferred_colors = []
        other_colors = []
        for color in available_colors:
            if color_info[color]["rare_type"] == s_rare:  # 同稀有类型的栖息地
                preferred_colors.append(color)
            else:
                other_colors.append(color)

        # 优先选同类型栖息地（若有），否则选其他可用栖息地
        candidate_colors = preferred_colors if preferred_colors else other_colors

        # 步骤3：选最小编号的候选颜色（保持栖息地编号简洁）
        chosen_color = None
        if candidate_colors:
            chosen_color = min(candidate_colors)  # 选最小编号的候选栖息地
        else:
            # 无可用栖息地，新建栖息地（编号从1开始递增）
            chosen_color = max(color_info.keys(), default=0) + 1

        # 步骤4：分配栖息地并更新信息
        color_assignments[spirit] = chosen_color
        color_info[chosen_color]["members"].append(spirit)
        # 更新栖息地主要稀有类型（若为空则设为当前精灵类型）
        if color_info[chosen_color]["rare_type"] is None:
            color_info[chosen_color]["rare_type"] = s_rare

    # ====================== 4. 输出结果（含稀有性分布） ======================
    num_habitats = len(color_info)
    print(f"=== 栖息地数量：{num_habitats}（每个栖息地最多{max_habitat_size}只精灵） ===")
    print(f"=== 优先聚集类型：{prioritize_rare_type} ===")

    # 按栖息地分组并打印
    for color in sorted(color_info.keys()):
        info = color_info[color]
        members = info["members"]
        rare_types = [spirits[m]["稀有性"] for m in members]
        print(f"\n--- 栖息地{color}（{len(members)}只精灵，稀有性分布：{rare_types}） ---")
        print(f"精灵列表：{[m for m in members]}")
        print(
            f"内部相宜性：{'全相宜' if all(comp_graph[u].issuperset({v}) for u, v in zip(members, members[1:])) else '冲突'}（算法保证无冲突）")
        print(f"聚集效果：{'同类型优先' if len(set(rare_types)) == 1 else '混合类型'}")

    return color_assignments, color_info


if __name__ == "__main__":
    main()
