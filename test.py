# import modulu zodpovědného za testy jednotek
import unittest
# import testovaných modulů
import brainx
import image_png
#import image_pnm
 
 
# třída obsahující testy
class KnownOutputs(unittest.TestCase):
     
    def setUp(self):
        self.BF = brainx.BrainFuck
        self.BC = brainx.BrainCopter
        self.BL = brainx.BrainLoller
        self.PngReader = image_png.PngReader
        #self.PnmWriter = image_pnm.PnmWriter()
    
    def test_bf_1(self):
        """HelloWorld s \n"""
        with open( 'test_data/hello1.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data, memory=b'\x00', output='', show_output=False)
        program.run()
        self.assertEqual(program.output, 'Hello World!\n')
    
    def test_bf_2(self):
        """HelloWorld bez \n"""
        with open( 'test_data/hello2.b', encoding='ascii' ) as stream:
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
        self.assertEqual(data, '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.')
    
    def test_bl_2(self):
        """načtení dat z obrázku"""
        img = self.BL('test_data/HelloWorld.png')
        data = img.load()
        program = self.BF(data, memory=b'\x00', output='', show_output=False)
        program.run()
        self.assertEqual(program.output, 'Hello World!')


# zajištění spuštění testů při zavolání souboru z příkazové řádky
if __name__ == '__main__':
    unittest.main()
