# -*- coding: utf-8 -*-

from ida_parse_trace_line_helper.trace_line_info import TraceData


class TraceLine:

    def __init__(self, trace_line: str):
        self.__raw_trace_line = trace_line
        self.__data = self.__parse_trace_line_to_list()

    def get_changed_register(self) -> dict:
        return self.__data.changed_registers

    def get_source_operands(self):
        return self.get_operands()[1:]

    def get_dest_operand(self):
        return self.get_operand(0)

    def get_mnemonic(self) -> str:
        return self.__data.mnemonic

    def get_operands(self) -> str:
        return self.__data.operands

    def get_operand(self, index):
        return self.__data.operands[index] if index < len(self.__data.operands) else None

    def __parse_trace_line_to_list(self):
        if self.__raw_trace_line:
            temp_list = self.__raw_trace_line.split("\t")
            if len(temp_list) >= 4 and self.__raw_trace_line.endswith("\n"):
                return TraceData(
                    temp_list[0].strip(),
                    temp_list[1].split(":")[0].strip(),
                    temp_list[1].split(":")[1].strip() if len(temp_list[1].split(":")) >= 2 else "",
                    temp_list[2].strip(),
                    temp_list[3].strip()
                )
            return None

    def __str__(self):
        return "{module_name}:{address}\t{mnemonic} {operands}\t{changed_registers}".format(
            module_name=self.__data.module_name,
            address=self.__data.address,
            mnemonic=self.__data.mnemonic,
            operands=self.__data.operands,
            changed_registers=self.__data.changed_registers
        )
