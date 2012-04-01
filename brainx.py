#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


class BrainFuck:
    """BrainFuck Interpreter

    Attributes:
    data -- string with the program instructions
    memory -- program's data/memory
    output -- run output stored in string
    instruction_pointer -- data pointer
    memory_pointer -- memory pointer
    show_output -- whether to print program's output

    """

    def __init__(self, data, memory=b'\x00', output='', instruction_pointer=0, memory_pointer=0, show_output=True):
        """Interpreter initialization"""

        # data programu
        self.data = data

        # inicializace proměnných
        self.memory = memory
        self.instruction_pointer = instruction_pointer
        self.memory_pointer = memory_pointer

        # DEBUG a testy
        # a) paměť výstupu
        self.output = output
        # b) ukaž výstup
        self.show_output = show_output

    def run(self):
        """Execute the program stored in self.data"""

        #TODO: Remove NOPs from data? using filter

        commands = {
            '>': self.__data_inc,
            '<': self.__data_dec,
            '+': self.__memory_inc,
            '-': self.__memory_dec,
            '.': self.__print,
            ',': self.__read,
            '[': self.__jump_fwd,
            ']': self.__jump_bwd,
            }

        while self.instruction_pointer < len(self.data):
            cmd = self.data[self.instruction_pointer]
            commands.get(cmd, self.__nop)()

    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return self.memory


    def get_current_memory(self):
        return self.memory[self.memory_pointer]

    def __nop(self):
        pass

    def __data_inc(self):
        pass

    def __data_dec(self):
        pass

    def __memory_inc(self):
        pass

    def __memory_dec(self):
        pass

    def __print(self):
        char = self.get_current_memory()
        self.output += char

        if self.show_output:
            sys.stdout.write(chr(char))

    def __read(self):
        pass

    def __jump_fwd(self):
        pass

    def __jump_bwd(self):
        pass


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""

    def __init__(self, filename):
        pass

    #
    # načtení dat programu z obrázku
    # ~ vrací řetězec obsahující data programu v brainfucku
    #
    def load(self):
        pass
