#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import modulu zodpovědného za testy jednotek
import unittest
import os
# import testovaných modulů
import brainx
import image_png
#import image_pnm


# třída obsahující testy
class KnownOutputs(unittest.TestCase):
    def setUp(self):
        self.BF = brainx.BrainFuck
        #self.BC = brainx.BrainCopter
        self.BL = brainx.BrainLoller
        self.PngReader = image_png.PngReader
        #self.PnmWriter = image_pnm.PnmWriter()

    def test_bf_1(self):
        """HelloWorld s \n"""
        with open('test_data/hello1.b', encoding='ascii') as stream:
            data = stream.read()
        program = self.BF(data, memory=b'\x00', output='', show_output=False)
        program.run()
        self.assertEqual(program.output, 'Hello World!\n')

    def test_bf_2(self):
        """HelloWorld bez \n"""
        with open('test_data/hello2.b', encoding='ascii') as stream:
            data = stream.read()
        program = self.BF(data, memory=b'\x00', output='', show_output=False)
        program.run()
        self.assertEqual(program.output, 'Hello World!')

    def test_bf_3(self):
        """vynulování aktuální, ale pouze aktuální, buňky"""
        program = self.BF('[-]', memory=b'\x03\x02', memory_pointer=1, output='', show_output=False)
        program.run()
        self.assertEqual(program.get_memory(), b'\x03\x00')

    def test_bf_4(self):
        """vynulování všech nenulových buněk doleva"""
        program = self.BF('[[-]<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4, output='', show_output=False)
        program.run()
        self.assertEqual(program.get_memory(), b'\x03\x03\x00\x00\x00')

    def test_bf_5(self):
        """přesun na první nenulovou buňku doleva"""
        program = self.BF('[<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4, output='', show_output=False)
        program.run()
        self.assertEqual(program.memory_pointer, 2)

    def test_bf_6(self):
        """přesun na první nenulovou buňku doprava"""
        program = self.BF('[>]', memory=b'\x03\x03\x00\x02\x02', output='', show_output=False)
        program.run()
        self.assertEqual(program.memory_pointer, 2)

    def test_bf_7(self):
        """destruktivní přičtení aktuální buňky k buňce následující"""
        program = self.BF('[>+<-]', memory=b'\x03\x03', output='', show_output=False)
        program.run()
        self.assertEqual(program.get_memory(), b'\x00\x06')

    def test_bf_8(self):
        """nedestruktivní přičtení aktuální buňky k buňce následující"""
        program = self.BF('[>+>+<<-]>>[<<+>>-]', memory=b'\x03\x03', output='', show_output=False)
        program.run()
        self.assertEqual(program.get_memory(), b'\x03\x06\x00')

    def test_bf_9(self):
        """destruktivní odečtení aktuální buňky od buňky následující"""
        program = self.BF('[>-<-]', memory=b'\x03\x05', output='', show_output=False)
        program.run()
        self.assertEqual(program.get_memory(), b'\x00\x02')

    def test_bl_1(self):
        """načtení dat z obrázku"""
        img = self.BL('test_data/HelloWorld.png')
        data = img.load()
        self.assertEqual(data,
            '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.')

    def test_bl_2(self):
        """načtení dat z obrázku"""
        img = self.BL('test_data/HelloWorld.png')
        data = img.load()
        program = self.BF(data, memory=b'\x00', output='', show_output=False)
        program.run()
        self.assertEqual(program.output, 'Hello World!')


class KnownOutputs2(unittest.TestCase):
    def setUp(self):
        self.PngReader = image_png.PngReader

    def test_png_1(self):
        """load standard PNG file"""
        img = self.PngReader('test_data/sachovnice.png')
        img.load()
        self.assertEqual(img.width, 3)
        self.assertEqual(img.height, 3)
        self.assertEqual(img.colour_type, 2) #RGB
        self.assertEqual(img.bit_depth, 8)
        self.assertEqual(img.interlace, 0)
        self.assertEqual(img.line_bytes, 3 * 3)
        self.assertEqual(img.idat_decomp,
            b'\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\xff\xff\xff\x7f\x7f\x7f\x00\x00\x00\x00\xff\xff\x00\xff\x00\xff\x00\xff\xff')


    def test_png_2(self):
        """load broken signature"""
        img = self.PngReader(filepath=b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0d\x0a', bytes=True)
        self.assertRaises(IOError, img.load)

    def test_png_filters(self):
        """test filters"""
        files = ('f00n2c08.png', 'f01n2c08.png', 'f02n2c08.png', 'f03n2c08.png', 'f04n2c08.png')
        for file in files:
            path = os.path.join('test_data', file)
            img = self.PngReader(path)
            img.load()
            self.assertEqual(img.width, 32)
            self.assertEqual(img.height, 32)
            self.assertEqual(len(img.idat_decomp), (32 * 32 * 3) + 32)

            nonf_path = os.path.join('test_data', 'nonf', file)
            nonf_img = self.PngReader(nonf_path)
            nonf_img.load()

            #assert img.lines == nonf_img.lines, "{}: Non-filtered image doesn't match unfiltered one".format(file)
            self.assertEquals(img.lines, nonf_img.lines,
                "{}: Non-filtered image doesn't match unfiltered one".format(file))

    def test_png_get_pixel(self):
        img = self.PngReader('test_data/sachovnice.png')
        img.load()

        assert img.get_pixel(0,0) == b'\xff\x00\x00'
        assert img.get_pixel(1,0) == b'\x00\xff\x00'
        assert img.get_pixel(2,0) == b'\x00\x00\xff'
        assert img.get_pixel(0,1) == b'\xff\xff\xff'
        assert img.get_pixel(1,1) == b'\x7f\x7f\x7f'
        assert img.get_pixel(2,1) == b'\x00\x00\x00'

# zajištění spuštění testů při zavolání souboru z příkazové řádky
if __name__ == '__main__':
    unittest.main()
