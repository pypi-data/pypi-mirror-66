# -*- coding: utf-8 -*-
import re


class TraceData:
    def __init__(self, thread_id, module_name, address, op_code, changed_register, module_base=0):
        self.__raw_thread_id = thread_id
        self.__raw_module_name = module_name
        self.__raw_address = address
        self.__raw_op_code = op_code
        self.mnemonic, self.operands = self.parse_op_code(self.__raw_op_code)
        self.__raw_changed_register = changed_register
        self.__module_base = module_base
        self.changed_registers = self.parse_changed_register(self.__raw_changed_register)

    @staticmethod
    def parse_changed_register(changed_register_str: str):
        register_infos = changed_register_str.split(" ")
        changed_register_infos = {}
        for register_info in register_infos:
            if register_info:
                register_name = register_info.split("=")[0]
                changed_value = register_info.split("=")[1]
                changed_register_infos[register_name] = changed_value
        return changed_register_infos

    @staticmethod
    def parse_op_code(op_code_str: str):
        temp_list = []
        for temp in op_code_str.split(" "):
            if temp != "":
                temp_list.append(temp.replace(",", ""))
        return (temp_list[0], temp_list[1:]) if len(temp_list) >= 2 else ("", [])

    @property
    def module_name(self):
        return self.__raw_module_name

    @property
    def address(self):
        return self.__raw_address

    @property
    def offset(self):
        return self.__raw_address - self.__module_base

    @property
    def thread_id(self):
        return self.__raw_thread_id

    @property
    def op_code(self):
        return self.__raw_op_code
