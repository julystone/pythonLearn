import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class DynamicRebalanceStrategy:
    def __init__(self, initial_capital=3000, target_range=(20000, 40000), stop_loss=0.05):
        """
        初始化策略参数
        :param initial_capital: 初始投入金额
        :param target_range: 目标仓位范围（元）
        :param stop_loss: 总止损比例（如5%）
        """
        self.initial_capital = initial_capital
        self.target_min, self.target_max = target_range
        self.stop_loss = stop_loss

        # 持仓状态
        self.holding = {
            'initial_investment': 0,
            'current_price': None,
            'current_shares': 0,
            'total_investment': 0,
            'available_funds': 0
        }

        # 补仓参数
        self.rebalance_points = []  # 补仓触发点（跌幅百分比）
        self.rebalance_amounts = []  # 对应补仓金额

    def calculate_rebalance_levels(self, initial_drop=0.03, step=0.03, max_steps=10):
        """
        计算动态补仓档位（基于初始跌幅和步长）
        :param initial_drop: 首次补仓触发跌幅（默认3%）
        :param step: 每档跌幅增量（默认3%）
        :param max_steps: 最大档位数
        """
        self.rebalance_points = [initial_drop + i * step for i in range(max_steps)]
        self.rebalance_amounts = self._calculate_rebalance_amounts()

    def _calculate_rebalance_amounts(self):
        """
        根据剩余可承受亏损计算每档补仓金额
        :return: 补仓金额列表
        """
        remaining_loss = self.target_max * self.stop_loss - self.initial_capital * (1 - self.stop_loss)
        amounts = []
        for i, drop in enumerate(self.rebalance_points):
            # 剩余资金按指数衰减分配（越低档补仓越少）
            amount = (self.target_max - self.target_min) * (0.5 ** i)
            amounts.append(min(amount, remaining_loss))
        return amounts

    def simulate_price_changes(self, price_series):
        """
        模拟价格波动并执行补仓策略
        :param price_series: 价格序列（如[100, 98, 95, ...]）
        :return: 补仓记录、最终持仓状态
        """
        records = []
        current_price = self.holding['current_price'] = price_series[0]
        self.holding['initial_investment'] = self.initial_capital
        self.holding['current_shares'] = self.initial_capital / current_price
        self.holding['total_investment'] = self.initial_capital
        self.holding['available_funds'] = self.target_max - self.initial_capital

        for price in price_series[1:]:
            records.append(self._update_state(price))
            if self._check_stop_loss():
                break
        return pd.DataFrame(records), self.holding

    def _update_state(self, new_price):
        """
        更新持仓状态并触发补仓
        :param new_price: 新价格
        :return: 操作记录字典
        """
        record = {
            'step': len(self.holding['rebalance_points']) + 1,
            'price': new_price,
            'action': 'hold',
            'amount': 0
        }

        # 检查是否触发补仓
        drop_percent = (self.holding['current_price'] - new_price) / self.holding['current_price']
        if drop_percent >= self.rebalance_points[0] and len(self.rebalance_points) > 0:
            # 执行补仓
            rebalance_idx = np.argmin([abs(drop_percent - p) for p in self.rebalance_points])
            amount = self.rebalance_amounts[rebalance_idx]
            shares = amount / new_price
            self.holding['current_shares'] += shares
            self.holding['total_investment'] += amount
            self.holding['available_funds'] -= amount
            self.holding['current_price'] = new_price
            record.update({
                'action': 'rebalance',
                'amount': amount,
                'rebalance_level': self.rebalance_points[rebalance_idx]
            })
            self.rebalance_points.pop(rebalance_idx)  # 移除已触发档位

        return record

    def _check_stop_loss(self):
        """
        检查是否触发总止损
        :return: 布尔值
        """
        current_value = self.holding['current_shares'] * self.holding['current_price']
        total_loss = (self.holding['total_investment'] - current_value) / self.holding['total_investment']
        return total_loss >= self.stop_loss


# 示例使用
if __name__ == "__main__":
    # 初始化策略（以恒生科技ETF为例）
    strategy = DynamicRebalanceStrategy(
        initial_capital=3000,
        target_range=(20000, 40000),
        stop_loss=0.05
    )
    strategy.calculate_rebalance_levels(initial_drop=0.03, step=0.03, max_steps=10)

    # 模拟价格波动（示例数据）
    price_data = [200, 150, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 0] # 假设价格从200跌至150

    # 运行模拟
    df_records, final_state = strategy.simulate_price_changes(price_data)

    # 输出结果
    print("=== 补仓记录 ===")
    print(df_records[['step', 'price', 'action', 'amount', 'rebalance_level']])
    print(f"最终持仓价值：{final_state['current_shares'] * final_state['current_price']: .2f}元")

    # 绘制盈亏曲线
    plt.figure(figsize=(10, 6))
    plt.plot(price_data, label='ETF价格')
    rebalance_points = [200, 150, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 0]
    for p in rebalance_points:
        plt.axvline(x=rebalance_points.index(p), color='red', linestyle='--', label=f'补仓点 {p}%')
    plt.title('ETF价格与补仓触发点')
    plt.xlabel('时间步')
    plt.ylabel('价格')
    plt.legend()
    plt.show()
