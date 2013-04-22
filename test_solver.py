#!/usr/bin/env python

import unittest
import solverc

class TarjanTest(unittest.TestCase):
    def testRead(self):
        eqns, inequ = solverc.readeqns('test_eqs.txt')
        self.assertEqual(len(eqns), 4)
        self.assertEqual(len(inequ), 1)

        # TODO: Add tests for different components in solverc
        
if __name__ == '__main__':
    unittest.main()
