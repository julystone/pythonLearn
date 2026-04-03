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
    spirits_new = {}
    for key, value in spirits.items():
        if key in ["月牙雪熊", "燃薪虫", "空空颅", "粉星仔", "窃光蚊", "双灯鱼", "贝瑟", "粉粉星"]:
            spirits_new[key] = {"属性": value, "稀有性": "稀有"}
        else:
            spirits_new[key] = {"属性": value, "稀有性": "非稀有"}

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
    prioritize_rare_type = "非稀有"  # 稀有性优先（软目标）

    # ====================== 2. 计算所有精灵对的相宜规则计数 ======================
    spirit_list = list(spirits.keys())
    comp_count = defaultdict(dict)  # comp_count[u][v] = 精灵u与v的相宜规则计数
    
    for i in range(len(spirit_list)):
        u = spirit_list[i]
        u_attrs = spirits[u]["属性"]
        for j in range(i+1, len(spirit_list)):
            v = spirit_list[j]
            v_attrs = spirits[v]["属性"]
            
            # 计算相宜规则计数（核心修改：从布尔值到整数计数）
            count = 0
            for s in u_attrs:
                for t in v_attrs:
                    # 条件1：同属性相宜（计数+1）
                    if s == t:
                        count += 1
                    # 条件2：不同属性符合规则（计数+1）
                    elif frozenset({s, t}) in compatibility_rules:
                        count += 1
            comp_count[u][v] = count
            comp_count[v][u] = count  # 对称矩阵

    # ====================== 3. 贪心配对（优先高计数、同稀有性） ======================
    # 步骤1：节点排序（非稀有优先，再按“潜在最大计数”降序）
    def sort_key(spirit):
        rare_priority = 0 if spirits[spirit]["稀有性"] == prioritize_rare_type else 1
        # 潜在最大计数：该精灵与其他所有精灵的最大计数
        max_count = max(comp_count[spirit].values()) if comp_count[spirit] else 0
        return (rare_priority, -max_count)  # 非稀有在前，高计数在前
    
    sorted_spirits = sorted(spirit_list, key=sort_key)
    
    # 步骤2：初始化配对状态
    matched = set()  # 已配对精灵
    habitats = []    # 栖息地列表（每个元素为[精灵1, 精灵2]或[精灵]）
    
    # 步骤3：贪心配对（优先高计数对）
    for i in range(len(sorted_spirits)):
        u = sorted_spirits[i]
        if u in matched:
            continue  # 已配对，跳过
        
        # 寻找最佳伙伴：同稀有性→高计数优先；无则异稀有性→高计数优先
        best_partner = None
        best_count = -1
        for j in range(i+1, len(sorted_spirits)):
            v = sorted_spirits[j]
            if v in matched:
                continue  # 伙伴已配对，跳过
            
            # 计算当前对的计数
            current_count = comp_count[u][v]
            # 优先级：同稀有性 > 高计数
            is_same_rare = (spirits[u]["稀有性"] == spirits[v]["稀有性"])
            # 若同稀有性且计数更高，或异稀有性但计数更高且无同稀有性选项
            if (is_same_rare and current_count > best_count) or (not is_same_rare and current_count > best_count):
                best_partner = v
                best_count = current_count
        
        # 配对成功（若找到伙伴且计数>0，或必须配对）
        if best_partner is not None and (best_count > 0 or len(matched) % 2 == 1):  # 允许计数0的配对（若无其他选择）
            habitats.append([u, best_partner])
            matched.add(u)
            matched.add(best_partner)
        else:
            # 无合适伙伴，单只成栖息地
            habitats.append([u])
            matched.add(u)

    # ====================== 4. 输出结果（含相宜规则计数） ======================
    total_count = 0  # 所有栖息地的相宜规则计数之和
    print(f"=== 栖息地数量：{len(habitats)}（容量≤{max_habitat_size}） ===")
    print(f"=== 优先聚集类型：{prioritize_rare_type} ===")
    
    for idx, members in enumerate(habitats, 1):
        if len(members) == 2:
            u, v = members
            count = comp_count[u][v]
            total_count += count
            rare_types = f"{spirits[u]['稀有性']}+{spirits[v]['稀有性']}"
            print(f"\n--- 栖息地{idx}（2只精灵，相宜规则计数：{count}，稀有性：{rare_types}） ---")
            print(f"精灵列表：{u}（{spirits[u]['属性']}）、{v}（{spirits[v]['属性']}）")
            print(f"符合的规则：{[frozenset({s,t}) for s in spirits[u]['属性'] for t in spirits[v]['属性'] if s==t or frozenset({s,t}) in compatibility_rules]}")
        else:
            member = members[0]
            print(f"\n--- 栖息地{idx}（1只精灵，稀有性：{spirits[member]['稀有性']}） ---")
            print(f"精灵列表：{member}（{spirits[member]['属性']}）")
    
    print(f"\n=== 总相宜规则计数：{total_count}（所有栖息地的规则符合数之和） ===")

    return habitats, total_count

if __name__ == "__main__":
    main()