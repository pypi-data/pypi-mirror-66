# -*- coding:utf-8 -*-
""" Test library for CRC32 """
# !/usr/bin/python
# Python:   3.5.2+
# Platform: Windows/Linux/MacOS/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test library CRC32 Module.
# Package:  pip install libscrc.
# History:  2020-03-13 Wheel Ver:0.1.6 [Heyn] Initialize

import unittest

import libscrc
from libscrc import _crc32

class TestCRC32( unittest.TestCase ):
    """ Test CRC32 variant.
    """

    def do_basics( self, module ):
        """ Test basic functionality.
        """
        self.assertEqual( module.fsc(b'123456789'),     0x0376E6E7 )
        self.assertEqual( module.crc32(b'123456789'),   0xCBF43926 )
        self.assertEqual( module.mpeg2(b'123456789'),   0x0376E6E7 )

        self.assertEqual( module.crc32( b'A' * 4096),           0xFEA63440 )
        self.assertEqual( module.crc32( b'A' * 4096 * 10),      0x1521C066 )
        self.assertEqual( module.fletcher32( b'123456789' ),    0xDF09D509 )

        # test when there are no data
        self.assertEqual( module.crc32( b'' ),          0x00000000 )

    def test_basics( self ):
        """ Test basic functionality.
        """
        self.do_basics( libscrc )


    def test_basics_c( self ):
        """Test basic functionality of the extension module.
        """
        self.do_basics( _crc32 )


if __name__ == '__main__':
    unittest.main()
