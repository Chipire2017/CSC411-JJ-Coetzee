#!/usr/bin/env python

import unittest
import solverc

class TarjanTest(unittest.TestCase):
    def testRead(self):
        eqns, inequ, unkn = solverc.readeqns('eqns.txt')
        self.assertEqual(len(eqns), 4)
        self.assertEqual(len(inequ), 1)
        self.assertEqual(len(unkn), 5)
        
    def testInsert(self):
        eqns, inequ, unkn = solverc.readeqns('eqns.txt')
        eqns, unkn = solverc.InsertKnowns(specV, cnst, eqns, unkn)
        
        
        
        
        


        # TODO: Add tests for different components in solverc
        
if __name__ == '__main__':
    unittest.main()
