#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
from itertools import zip_longest
import struct
import zlib
from array import array

# http://docs.python.org/py3k/library/itertools.html
def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def paeth_predict(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c


class PngReader():
    """Třída pro práci s PNG-obrázky."""

    # PNG file signature
    # hex: 89  50 4E 47 0D 0A 1A 0A
    # dec: 137 80 78 71 13 10 26 10 - http://www.w3.org/TR/PNG/#5PNG-file-signature
    _signature = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'

    def __init__(self, filepath, bytes=False):
        """
        Opens the given file for a binary reading

        Named parameters:
        filepath -- path to PNG file or bytes of file contents
        bytes -- whether the given bytes were given in filepath
        """

        # IHDR values
        self.width = None
        self.height = None
        self.bit_depth = None
        self.colour_type = None
        self.interlace = None
        self.idat_decomp = None
        self.px_bytes = 3

        self.line_bytes = None

        if bytes:
            self.file = io.BytesIO(filepath)
        else:
            self.file = open(filepath, 'rb') # @type io.BufferedReader


    def get_pixel(self, x, y):
        if not self.lines:
            return None

        if 0 > x > (self.width-1):
            raise ValueError("Invalid X position: {} for image of width {}".format(x, self.width))
        elif 0 > y > (self.height -1):
            raise ValueError("Invalid Y position: {} for image of height {}".format(y, self.height))

        byte_x =  x * self.px_bytes

        return bytes(self.lines[y][byte_x:(byte_x+self.px_bytes)])

#
    # hlavní načítací funkce
    #
    def load(self):
        """Načtení PNG-obrázku do pracovní (RGB-datové) struktury."""

        signature = self.file.read(8)
        if signature != self._signature:
            raise IOError("Invalid PNG signature")

        self.idat_decomp = bytearray()
        self.decompressobj = zlib.decompressobj()

        chunk_funcs = {
            'IHDR': self.__ihdr,
            'IDAT': self.__idat,
            }

        for type, data in self.generate_chunks():
            # End with
            if type == 'IEND':
                break
            if type not in chunk_funcs:
                # TODO: could print some warning
                continue
            chunk_funcs[type](data)

        self.idat_decomp += self.decompressobj.flush()
        self.__process_raw(self.idat_decomp)

    def read_chunk(self):
        """
        Reads next chunk of data from file
        Returns chunk type and data in tuple
        """

        # 4B unsigned int, network order
        # 4B type string
        length, type = struct.unpack('!I4s', self.file.read(8))

        data = self.file.read(length)
        crc = self.file.read(4)

        # checksum includes type and data
        # http://www.w3.org/TR/PNG/#5Chunk-layout
        checksum = zlib.crc32(type)
        checksum = zlib.crc32(data, checksum)
        if struct.pack('!I', checksum) != crc:
            raise IOError("CRC doesn't match checksum")
        return str(type, 'ascii'), data

    def generate_chunks(self):
        while True:
            type, data = self.read_chunk()
            if type and data:
                yield type, data
            else:
                break

    # Decodes IHDR chunk, see http://www.w3.org/TR/PNG/#11IHDR
    #

    def __ihdr(self, data):
        """
        Decodes IHDR chunk, see http://www.w3.org/TR/PNG/#11IHDR

        Populates instance variables:
         self.width
         self.height
         self.bit_depth
         self.colour_type
         self.interlace
         self.row_len
        """

        if len(data) != 13:
            raise ValueError("IHDR chunk is %d bytes long, 13 expected" % len(data))

        # width, height -- unsigned Int, 8 Bytes total
        # bit_depth, colour_type, compression, filter, interlace -- unsigned char
        (self.width, self.height, self.bit_depth, self.colour_type,
         compression, filter, self.interlace) = struct.unpack("!2I5B", data)

        if compression != 0:
            raise ValueError("Invalid compression method {}".format(compression))
        if filter != 0:
            raise ValueError("Invalid filter method {}".format(filter))

        if self.bit_depth != 8:
            raise NotImplementedError("Bit depth {} is not supported".format(self.colour_type))

        if self.colour_type in (0, 3, 4, 6):
            raise NotImplementedError("Colour type {} is not supported".format(self.colour_type))
        elif self.colour_type != 2:
            raise ValueError("Invalid colour type {}".format(self.colour_type))
            #TODO: do some more comprehensive checks on header

        # 3*8 = 24 b per pixel
        # 24 * width
        self.line_bytes = 3 * self.width # XXX this is wild assumption
        # * self.bit_depth / 8

    def __idat(self, data):
        """
        Decompress IDAT chunk, add it to self.idat_decomp
        """
        self.idat_decomp += self.decompressobj.decompress(data)

    def __process_raw(self, raw_data):
        """
        Process raw decompressed data
        """
        expected_len = self.width * 3 * self.height + self.height
        if len(raw_data) != expected_len:
            raise ValueError(
                "Expected length of decompressed data to be {}, got {} instead".format(expected_len, len(raw_data))
            )

        self.lines = []
        prev_line = [0] * self.line_bytes # Non-existent line is considered as zeroes
        # Iterate each line (+1 byte = filter type)
        for line in grouper(self.line_bytes + 1, raw_data):
            recon = self.__process_filter(line[0], line[1:], prev_line)
            self.lines.append(recon)
            prev_line = self.lines[-1] # Assign the unfiltered last line

        pass


    def __process_filter(self, type, line, prev_line):
        """
        Handle filters
        """
        px_bytes = 3 # True color: pixel has 3 bytes

        def sub():
            """
            Recon(x) = Filt(x) + Recon(previous_byte)
            Where previous_byte is on same position in previous pixel
            """
            prev_pos = -px_bytes
            for byte in line:
                if prev_pos >= 0:
                    byte = (byte + recon[prev_pos]) % 256
                recon.append(byte)
                prev_pos += 1

        def up():
            """
            Recon(x) = Filt(x) + Recon(prev_line)
            """
            for i, byte in enumerate(line):
                byte = (byte + prev_line[i]) % 256
                recon.append(byte)

        def average():
            """
            Filt(x) + floor((Recon(prev_byte) + Recon(prev_line)) / 2)
            """
            prev_pos = -px_bytes
            for i, byte in enumerate(line):
                prev_byte = 0
                if prev_pos >= 0:
                    prev_byte = recon[prev_pos]

                byte = (byte + (prev_line[i] + prev_byte) // 2) % 256
                recon.append(byte)
                prev_pos += 1

        def paeth():
            """
            Filt(x) + PaethPredictor(Recon(prev_byte), Recon(prev_line), Recon(prev_line_prev_byte))
            """
            prev_pos = -px_bytes
            for i, x in enumerate(line):
                a = 0
                b = prev_line[i]
                c = 0
                if prev_pos >= 0:
                    a = recon[prev_pos]
                    c = prev_line[prev_pos]

                x = (x + paeth_predict(a, b, c)) % 256
                recon.append(x)
                prev_pos += 1


        recon = bytearray()
        # 0: no filter
        if type == 0:
            recon.extend(line)
        elif type == 1:
            sub()
        elif type == 2:
            up()
        elif type == 3:
            average()
        elif type == 4:
            paeth()
        else:
            raise ValueError("Invalid filter type {}".format(type))

        return recon

