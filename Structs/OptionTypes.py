from enum import Enum


class OptionType(Enum):
    Call = 0
    Put = 1

    def ToString(self) -> str:
        if self == OptionType.Call:
            return "CE"
        return "PE"
