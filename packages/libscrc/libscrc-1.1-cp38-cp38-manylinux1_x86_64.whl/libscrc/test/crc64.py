# -*- coding:utf-8 -*-
""" Test library for CRC64 """
# !/usr/bin/python
# Python:   3.5.2+
# Platform: Windows/Linux/MacOS/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test library CRC64 Module.
# Package:  pip install libscrc.
# History:  2017-08-19 Wheel Ver:0.0.5 [Heyn] Initialize
#           2020-03-16 Wheel Ver:0.1.6 [Heyn] New add libscrc.hacker64()

import unittest

import libscrc
from libscrc import _crc64

class TestCRC64( unittest.TestCase ):
    """ Test CRC64 IOS&ECMA182 variant.
    """

    def do_basics( self, module ):
        """ Test basic functionality.
        """
        self.assertEqual( module.iso(b'123456789'), 0x46A5A9388A5BEFFE )
        self.assertNotEqual( module.iso(b'123456'), 0x288A5BEFFE4CB001 )

        self.assertEqual( module.ecma182(b'123456789'), 0x62EC59E3F1A4F00A )
        self.assertNotEqual( module.ecma182(b'123456'), 0x3DBD4712E4D9E786 )

        self.assertEqual( module.hacker64(b'123456789', poly=0xD800000000000000, init=0 ), 0x46A5A9388A5BEFFE )

        # the same in two steps
        crc = module.iso( b'12345' )
        crc = module.iso( b'6789', crc )
        self.assertEqual( crc, 0x46A5A9388A5BEFFE )

        crc = module.ecma182( b'12345' )
        crc = module.ecma182( b'6789', crc^0xFFFFFFFFFFFFFFFF )
        self.assertEqual( crc, 0x62EC59E3F1A4F00A )

    def test_basics( self ):
        """Test basic functionality.
        """
        self.do_basics( libscrc )


    def test_basics_c( self ):
        """ Test basic functionality of the extension module.
        """
        self.do_basics( _crc64 )

    def test_big_chunks(self):
        """ Test calculation of CRC on big chunks of data.
        """
        self.assertEqual( _crc64.iso(b'A' * 16 * 1024 * 1024),     0x9936C796B73DEB69 )
        self.assertEqual( _crc64.ecma182(b'A' * 16 * 1024 * 1024), 0x856716C3B2F186A2 )


if __name__ == '__main__':
    unittest.main()
