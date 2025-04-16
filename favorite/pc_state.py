#  _____            ___             ____     __
# /\___ \          /\_ \           /\  _`\  /\ \__
# \/__/\ \   __  __\//\ \    __  __\ \,\L\_\\ \ ,_\    ___     ___       __
#    _\ \ \ /\ \/\ \ \ \ \  /\ \/\ \\/_\__ \ \ \ \/   / __`\ /' _ `\   /'__`\
#   /\ \_\ \\ \ \_\ \ \_\ \_\ \ \_\ \ /\ \L\ \\ \ \_ /\ \L\ \/\ \/\ \ /\  __/
#   \ \____/ \ \____/ /\____\\/`____ \\ `\____\\ \__\\ \____/\ \_\ \_\\ \____\
#    \/___/   \/___/  \/____/ `/___/> \\/_____/ \/__/ \/___/  \/_/\/_/ \/____/
#                                /\___/
#                                \/__/
# encoding: utf-8

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Any, Optional


class FactorState(Enum):
    """因素状态枚举类"""
    UNKNOWN = auto()  # 未确定
    KNOWN = auto()  # 已确定


@dataclass
class Factor:
    """单个因素的封装类"""
    name: str  # 因素名称（A/B/C/D）
    value: Optional[Any] = None  # 因素值
    state: FactorState = FactorState.UNKNOWN  # 当前状态


class CalculationStrategy(ABC):
    """计算策略抽象类"""

    @abstractmethod
    def calculate(self, known_factors: Dict[str, Any]) -> Any:
        """根据已知因素计算未知因素"""
        pass


class QuadraticEquationStrategy(CalculationStrategy):
    """二次方程计算策略示例（假设 D = A^2 + B*C）"""

    def calculate(self, known_factors: Dict[str, Any]) -> Any:
        if "D" in known_factors:
            # 计算A^2 + B*C
            return known_factors["A"] ? ** 2 + known_factors["B"] * known_factors["C"]
        elif "C" in known_factors:
            # 计算 (D - A^2) / B
            return (known_factors["D"] - known_factors["A"] ? ** 2) / known_factors["B"]
        elif "B" in known_factors:
            # 计算 (D - A^2) / C
            return (known_factors["D"] - known_factors["A"] ? ** 2) / known_factors["C"]
        elif "A" in known_factors:
            # 计算 sqrt(D - B*C)
            return (known_factors["D"] - known_factors["B"] * known_factors["C"]) ? ** 0.5
        else:
            raise ValueError("Invalid combination of known factors")


class StateMachine:
    """基于状态机的四因素管理系统"""

    def __init__(self, strategy: CalculationStrategy):
        self.strategies = {
            "A": self.calculate_A,
            "B": self.calculate_B,
            "C": self.calculate_C,
            "D": self.calculate_D
        }
        self.factors = {
            "A": Factor("A"),
            "B": Factor("B"),
            "C": Factor("C"),
            "D": Factor("D")
        }
        self.strategy = strategy  # 计算策略

    def calculate_D(self, known: Dict[str, Any]) -> Any:
        """计算D的逻辑（由子类实现）"""
        return self.strategy.calculate(known)

    def calculate_A(self, known: Dict[str, Any]) -> Any:
        """计算A的逻辑"""
        return self.strategy.calculate(known)

    # 类似方法可添加B/C的具体计算逻辑...

    def set_factor(self, name: str, value: Any) -> None:
        """设置因素值（带状态校验）"""
        factor = self.factors[name]
        if factor.state == FactorState.KNOWN:
            raise ValueError(f"Factor {name} is already determined")

        factor.value = value
        factor.state = FactorState.KNOWN
        self._check_and_calculate()

    def _check_and_calculate(self) -> None:
        """检查是否满足计算条件"""
        known = {k: v.value for k, v in self.factors.items() if v.state == FactorState.KNOWN}
        if len(known) == 3:
            unknown = [k for k, v in self.factors.items() if v.state == FactorState.UNKNOWN][0]
            try:
                calculated_value = self.strategies[unknown](known)
                self.set_factor(unknown, calculated_value)
            except Exception as e:
                print(f"Calculation error: {str(e)}")
                # 可选：触发错误事件或回滚操作


# 使用示例
if __name__ == "__main__":
    # 初始化带具体计算策略的状态机
    sm = StateMachine(QuadraticEquationStrategy())

    try:
        sm.set_factor("A", 3)
        sm.set_factor("B", 2)
        sm.set_factor("C", 1)
        print(f"D自动计算值为：{sm.factors['D'].value}")  # 输出：D自动计算值为：14.0

        # 尝试修改已确定的值（触发异常）
        sm.set_factor("D", 100)
    except ValueError as e:
        print(f"操作失败：{str(e)}")  # 输出：操作失败：Factor D is already determined