# -*- coding: utf-8 -*-

import enum
import re


class OperandType(enum.Enum):
    REGISTER = 0
    IMMEDIATE = 1
    MEMORY = 2
    INDIRECT_VALUE = 3
    DISPLACEMENT_INSTRUCTION = 4


class Operand:
    def __init__(self, operand_str: str):
        self.type = self.parse_operand_type(operand_str)
        self.data = operand_str

    def __eq__(self, other):
        other_value = other
        if isinstance(other, Operand):
            other_value = other.data
        return str(self.data[1:]) == str(other_value[1:])

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def parse_operand_type(operand_str: str):
        if re.match(r"#0x[0-9A-F]+", operand_str):
            return OperandType.IMMEDIATE
        elif re.match(r"[X,W0-9]+", operand_str):
            return OperandType.REGISTER
        elif re.match(r"\[.*\]", operand_str):
            return OperandType.INDIRECT_VALUE
        elif "@PAGE" in operand_str:
            return OperandType.MEMORY
        elif re.match(r"[LS]+#[0-9]+", operand_str):
            return OperandType.DISPLACEMENT_INSTRUCTION
