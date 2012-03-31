#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', output='', instruction_pointer=0, memory_pointer=0, show_output=True):
        """Inicializace překladače."""
        
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
    
    #
    # prováděcí metoda interpretru
    #
    def run(self):
        """Spustí načtený brainfuckovský program."""
    
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
