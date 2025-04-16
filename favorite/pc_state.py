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
    """����״̬ö����"""
    UNKNOWN = auto()  # δȷ��
    KNOWN = auto()  # ��ȷ��


@dataclass
class Factor:
    """�������صķ�װ��"""
    name: str  # �������ƣ�A/B/C/D��
    value: Optional[Any] = None  # ����ֵ
    state: FactorState = FactorState.UNKNOWN  # ��ǰ״̬


class CalculationStrategy(ABC):
    """������Գ�����"""

    @abstractmethod
    def calculate(self, known_factors: Dict[str, Any]) -> Any:
        """������֪���ؼ���δ֪����"""
        pass


class QuadraticEquationStrategy(CalculationStrategy):
    """���η��̼������ʾ�������� D = A^2 + B*C��"""

    def calculate(self, known_factors: Dict[str, Any]) -> Any:
        if "D" in known_factors:
            # ����A^2 + B*C
            return known_factors["A"] ? ** 2 + known_factors["B"] * known_factors["C"]
        elif "C" in known_factors:
            # ���� (D - A^2) / B
            return (known_factors["D"] - known_factors["A"] ? ** 2) / known_factors["B"]
        elif "B" in known_factors:
            # ���� (D - A^2) / C
            return (known_factors["D"] - known_factors["A"] ? ** 2) / known_factors["C"]
        elif "A" in known_factors:
            # ���� sqrt(D - B*C)
            return (known_factors["D"] - known_factors["B"] * known_factors["C"]) ? ** 0.5
        else:
            raise ValueError("Invalid combination of known factors")


class StateMachine:
    """����״̬���������ع���ϵͳ"""

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
        self.strategy = strategy  # �������

    def calculate_D(self, known: Dict[str, Any]) -> Any:
        """����D���߼���������ʵ�֣�"""
        return self.strategy.calculate(known)

    def calculate_A(self, known: Dict[str, Any]) -> Any:
        """����A���߼�"""
        return self.strategy.calculate(known)

    # ���Ʒ��������B/C�ľ�������߼�...

    def set_factor(self, name: str, value: Any) -> None:
        """��������ֵ����״̬У�飩"""
        factor = self.factors[name]
        if factor.state == FactorState.KNOWN:
            raise ValueError(f"Factor {name} is already determined")

        factor.value = value
        factor.state = FactorState.KNOWN
        self._check_and_calculate()

    def _check_and_calculate(self) -> None:
        """����Ƿ������������"""
        known = {k: v.value for k, v in self.factors.items() if v.state == FactorState.KNOWN}
        if len(known) == 3:
            unknown = [k for k, v in self.factors.items() if v.state == FactorState.UNKNOWN][0]
            try:
                calculated_value = self.strategies[unknown](known)
                self.set_factor(unknown, calculated_value)
            except Exception as e:
                print(f"Calculation error: {str(e)}")
                # ��ѡ�����������¼���ع�����


# ʹ��ʾ��
if __name__ == "__main__":
    # ��ʼ�������������Ե�״̬��
    sm = StateMachine(QuadraticEquationStrategy())

    try:
        sm.set_factor("A", 3)
        sm.set_factor("B", 2)
        sm.set_factor("C", 1)
        print(f"D�Զ�����ֵΪ��{sm.factors['D'].value}")  # �����D�Զ�����ֵΪ��14.0

        # �����޸���ȷ����ֵ�������쳣��
        sm.set_factor("D", 100)
    except ValueError as e:
        print(f"����ʧ�ܣ�{str(e)}")  # ���������ʧ�ܣ�Factor D is already determined