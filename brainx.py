#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from image_png import PngReader

class BrainFuck:
    """BrainFuck Interpreter

    Attributes:
    data -- string with the program instructions
    memory -- bytearray with program's memory
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
        self.memory = bytearray(memory)
        self.instruction_pointer = instruction_pointer
        self.memory_pointer = memory_pointer

        # DEBUG a testy
        # a) paměť výstupu
        self.output = output
        # b) ukaž výstup
        self.show_output = show_output

    def run(self, end=None):
        """Execute the program stored in self.data

        Named parameters:
        end -- boundary of the current call, used for loops recursion
        """

        #TODO: Remove NOPs from data? using filter

        commands = {
            '>': self.__ptr_inc,
            '<': self.__ptr_dec,
            '+': self.__memory_inc,
            '-': self.__memory_dec,
            '.': self.__print,
            ',': self.__read,
            '[': self.__loop,
            ']': self.__loop_end,
            }

        if end is None:
            end = len(self.data)
        while self.instruction_pointer < end:
            cmd = self.data[self.instruction_pointer]
            commands.get(cmd, self.__nop)()
            self.instruction_pointer += 1

    def get_memory(self):
        return self.memory # FIXME explicitly convert to bytes -- is it needed?

    def get_current_memory(self):
        return self.memory[self.memory_pointer]

    def get_instruction(self, at=None):
        if at is None:
            at = self.instruction_pointer
        return self.data[at]

    def __nop(self):
        pass

    def __ptr_inc(self):
        """ Increment memory_pointer.
        Append new data cell if at the boundary
        """
        self.memory_pointer += 1
        if self.memory_pointer == len(self.memory):
            self.memory.append(0)

    def __ptr_dec(self):
        """Decrement memory_pointer"""
        if self.memory_pointer > 0:
            self.memory_pointer -= 1
            #TODO allow writing before the beginning of the memory?

    def __memory_inc(self):
        """Increment memory under the pointer
        If the current byte is 255, it will overflow to 0
        """
        current = self.get_current_memory()
        if current < 255:
            self.memory[self.memory_pointer] += 1
        else:
            self.memory[self.memory_pointer] = 0

    def __memory_dec(self):
        """Decrement memory under the pointer
        If the current byte is 0, it will underflow to 255
        """
        current = self.get_current_memory()
        if current > 0:
            self.memory[self.memory_pointer] -= 1
        else:
            self.memory[self.memory_pointer] = 255

    def __print(self):
        char = self.get_current_memory()
        self.output += chr(char)

        if self.show_output:
            sys.stdout.write(chr(char))

    def __read(self):
        c = sys.stdin.read(1)
        self.memory[self.memory_pointer] = ord(c)


    def __loop(self):
        """Handle an opening and closing loops"""
        #based on J. Tauber's implementation: http://speakerdeck.com/u/jtauber/p/you-used-python-for-what

        depth = 1
        start = end = self.instruction_pointer

        while depth:
            # forward seek opening and closing braces
            end += 1
            if self.get_instruction(end) == "[":
                depth += 1 # Nest deeper
            elif self.get_instruction(end) == "]":
                depth -= 1

        while self.get_current_memory() > 0:
            #nested execution until current memory != 0
            self.instruction_pointer = start + 1 # move after the opening brace
            self.run(end)
        self.instruction_pointer = end # jump to the end of loop


    def __loop_end(self):
        raise SyntaxError("Unbalanced closing brace at %d" % self.instruction_pointer)


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""

    class Coord():
        """
        Handles 2D coordinates with

        Attributes:
        DIRECTIONS -- basic directions as a list of (x,y) tuplesdefining delta for the move
        """
        DIRECTIONS = (
            (0, -1), #north
            (1, 0), #east
            (0, 1), #south
            (-1, 0)  #west
            )

        def __init__(self, direction=1, x=0, y=0):
            self.direction = direction # head to east
            self.x, self.y = x, y # top-left corner

        def get_dir(self):
            return self.DIRECTIONS[self.direction]

        def get_pos(self):
            return self.x, self.y

        def step(self):
            self.x += self.get_dir()[0]
            self.y += self.get_dir()[1]

        def turn_left(self):
            self.direction = (self.direction - 1) % 4

        def turn_right(self):
            self.direction = (self.direction + 1) % 4


    def __init__(self, filename):
        self.coord = self.Coord()
        #self.file = filename
        self.img = PngReader(filename)

    #
    # načtení dat programu z obrázku
    # ~ vrací řetězec obsahující data programu v brainfucku
    #
    def load(self):
        """
        Load and process the image
        Return BF program as string
        """

        def img_iter():
            while True:
                x, y = self.coord.get_pos()
                try:
                    pixel = self.img.get_pixel(x, y)
                except ValueError:
                    break

                if pixel == b'\x00\xff\xff':
                    self.coord.turn_right()
                elif pixel == b'\x00\x80\x80':
                    self.coord.turn_left()
                else:
                    yield pixel

                self.coord.step()


        self.img.load()
        out = []

        commands = {
            b'\xff\x00\x00': '>',
            b'\x80\x00\x00': '<',
            b'\x00\xff\x00': '+',
            b'\x00\x80\x00': '-',
            b'\x00\x00\xff': '.',
            b'\x00\x00\x80': ',',
            b'\xff\xff\x00': '[',
            b'\x80\x80\x00': ']',
            }

        for pixel in img_iter():
            c = commands.get(pixel)
            if c:
                out.append(c)

        return ''.join(out)