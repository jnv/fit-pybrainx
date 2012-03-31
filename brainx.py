#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
        """Execute the program"""



    
    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return self.memory


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
