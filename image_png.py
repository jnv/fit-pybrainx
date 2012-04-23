#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import struct
import zlib

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

        if bytes:
            self.file = io.BytesIO(filepath)
        else:
            self.file = open(filepath, 'rb') # @type io.BufferedReader

    #
    # hlavní načítací funkce
    #
    def load(self):
        """Načtení PNG-obrázku do pracovní (RGB-datové) struktury."""

        signature = self.file.read(8)
        if signature != self._signature:
            raise IOError("Invalid PNG signature")

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


    def __ihdr(self, data):
        pass

    def __idat(self, data):
        pass


