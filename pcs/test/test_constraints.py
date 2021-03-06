import os,sys
import shutil
import unittest
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
import utils
from pcs_test_functions import pcs,ac

empty_cib = "empty.xml"
temp_cib = "temp.xml"

class ConstraintTest(unittest.TestCase):
    def setUp(self):
        shutil.copy(empty_cib, temp_cib)
        self.setupClusterA(temp_cib)

    # Setups up a cluster with Resources, groups, master/slave resource and clones
    def setupClusterA(self,temp_cib):
        line = "resource create D1 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D2 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D3 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D4 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D5 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D6 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource clone D3"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource master Master D4"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

    def testConstraintRules(self):
        output, returnVal = pcs(temp_cib, "constraint location D1 rule score=222 '#uname' eq c00n03")
        assert output == "", [output]
        assert returnVal == 0

        output, returnVal = pcs(temp_cib, "constraint location D2 rule score=-INFINITY '#uname' eq c00n04")
        assert returnVal == 0
        assert output == "", [output]

        o, r = pcs(temp_cib, "resource create C1 Dummy --group C1-group")
        assert r == 0 and o == "", o

        output, returnVal = pcs(temp_cib, "constraint location C1-group rule score=pingd defined pingd")
        assert returnVal == 0
        assert output == "", [output]

        output, returnVal = pcs(temp_cib, "constraint location D3 rule score=pingd defined pingd")
        assert returnVal == 0
        assert output == "", [output]

        output, returnVal = pcs(temp_cib, "constraint location D4 rule score=INFINITY date start=2005-001 gt")
        assert returnVal == 0
        assert output == "", [output]

        output, returnVal = pcs(temp_cib, "constraint location D5 rule score=INFINITY date start=2005-001 end=2006-001 in_range")
        assert returnVal == 0
        assert output == "", [output]

        output, returnVal = pcs(temp_cib, "constraint location D6 rule score=INFINITY date-spec operation=date_spec years=2005")
        assert output == "", [output]
        assert returnVal == 0

        output, returnVal = pcs(temp_cib, "constraint location D3 rule score=-INFINITY not_defined pingd or pingd lte 0")
        assert returnVal == 0
        assert output == "", [output]

        output, returnVal = pcs(temp_cib, "constraint location D3 rule score=-INFINITY not_defined pingd and pingd lte 0")
        assert returnVal == 0
        assert output == "", [output]

        output, returnVal = pcs(temp_cib, "constraint --full")
        assert returnVal == 0
        ac (output,'Location Constraints:\n  Resource: C1-group\n    Constraint: location-C1-group\n      Rule: score-attribute=pingd  (id:location-C1-group-rule) \n        Expression: defined pingd  (id:location-C1-group-rule-expr-1) \n  Resource: D1\n    Constraint: location-D1\n      Rule: score=222  (id:location-D1-rule) \n        Expression: #uname eq c00n03  (id:location-D1-rule-expr-1) \n  Resource: D2\n    Constraint: location-D2\n      Rule: score=-INFINITY  (id:location-D2-rule) \n        Expression: #uname eq c00n04  (id:location-D2-rule-expr-1) \n  Resource: D3\n    Constraint: location-D3-2\n      Rule: score=-INFINITY boolean-op=and  (id:location-D3-2-rule) \n        Expression: not_defined pingd  (id:location-D3-2-rule-expr-1) \n        Expression: pingd lte 0  (id:location-D3-2-rule-expr-2) \n    Constraint: location-D3-1\n      Rule: score=-INFINITY boolean-op=or  (id:location-D3-1-rule) \n        Expression: not_defined pingd  (id:location-D3-1-rule-expr-1) \n        Expression: pingd lte 0  (id:location-D3-1-rule-expr-2) \n    Constraint: location-D3\n      Rule: score-attribute=pingd  (id:location-D3-rule) \n        Expression: defined pingd  (id:location-D3-rule-expr-1) \n  Resource: D4\n    Constraint: location-D4\n      Rule: score=INFINITY  (id:location-D4-rule) \n        Expression: start=2005-001 operation=gt  (id:location-D4-rule-expr-1) \n  Resource: D5\n    Constraint: location-D5\n      Rule: score=INFINITY  (id:location-D5-rule) \n        Expression: start=2005-001 operation=in_range end=2006-001  (id:location-D5-rule-expr-1) \n  Resource: D6\n    Constraint: location-D6\n      Rule: score=INFINITY  (id:location-D6-rule) \n        Expression:  (id:location-D6-rule-expr-1) \n          Date Spec: years=2005  (id:location-D6-rule-expr-1-datespec) \nOrdering Constraints:\nColocation Constraints:\n')

        o,r = pcs("constraint remove location-C1-group")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint remove location-D4-rule")
        ac(o,"")
        assert r == 0

        output, returnVal = pcs(temp_cib, "constraint --full")
        assert returnVal == 0
        ac (output,'Location Constraints:\n  Resource: D1\n    Constraint: location-D1\n      Rule: score=222  (id:location-D1-rule) \n        Expression: #uname eq c00n03  (id:location-D1-rule-expr-1) \n  Resource: D2\n    Constraint: location-D2\n      Rule: score=-INFINITY  (id:location-D2-rule) \n        Expression: #uname eq c00n04  (id:location-D2-rule-expr-1) \n  Resource: D3\n    Constraint: location-D3-2\n      Rule: score=-INFINITY boolean-op=and  (id:location-D3-2-rule) \n        Expression: not_defined pingd  (id:location-D3-2-rule-expr-1) \n        Expression: pingd lte 0  (id:location-D3-2-rule-expr-2) \n    Constraint: location-D3-1\n      Rule: score=-INFINITY boolean-op=or  (id:location-D3-1-rule) \n        Expression: not_defined pingd  (id:location-D3-1-rule-expr-1) \n        Expression: pingd lte 0  (id:location-D3-1-rule-expr-2) \n    Constraint: location-D3\n      Rule: score-attribute=pingd  (id:location-D3-rule) \n        Expression: defined pingd  (id:location-D3-rule-expr-1) \n  Resource: D5\n    Constraint: location-D5\n      Rule: score=INFINITY  (id:location-D5-rule) \n        Expression: start=2005-001 operation=in_range end=2006-001  (id:location-D5-rule-expr-1) \n  Resource: D6\n    Constraint: location-D6\n      Rule: score=INFINITY  (id:location-D6-rule) \n        Expression:  (id:location-D6-rule-expr-1) \n          Date Spec: years=2005  (id:location-D6-rule-expr-1-datespec) \nOrdering Constraints:\nColocation Constraints:\n')

    def testAdvancedConstraintRule(self):
        o,r = pcs(temp_cib, "constraint location D1 rule score=INFINITY not_defined pingd or pingd lte 0")
        ac(o,"")
        assert r == 0

        output, returnVal = pcs(temp_cib, "constraint --full")
        assert returnVal == 0
        ac (output,'Location Constraints:\n  Resource: D1\n    Constraint: location-D1\n      Rule: score=INFINITY boolean-op=or  (id:location-D1-rule) \n        Expression: not_defined pingd  (id:location-D1-rule-expr-1) \n        Expression: pingd lte 0  (id:location-D1-rule-expr-2) \nOrdering Constraints:\nColocation Constraints:\n')

    def testEmptyConstraints(self):
        output, returnVal = pcs(temp_cib, "constraint")
        assert returnVal == 0 and output == "Location Constraints:\nOrdering Constraints:\nColocation Constraints:\n", output

    def testMultipleOrderConstraints(self):
        o,r = pcs("constraint order stop D1 then stop D2")
        ac(o,"Adding D1 D2 (kind: Mandatory) (Options: first-action=stop then-action=stop)\n")
        assert r == 0

        o,r = pcs("constraint order start D1 then start D2")
        ac(o,"Adding D1 D2 (kind: Mandatory) (Options: first-action=start then-action=start)\n")
        assert r == 0

        o,r = pcs("constraint --full")
        ac(o,"Location Constraints:\nOrdering Constraints:\n  stop D1 then stop D2 (Mandatory) (id:order-D1-D2-mandatory)\n  start D1 then start D2 (Mandatory) (id:order-D1-D2-mandatory-1)\nColocation Constraints:\n")
        assert r == 0

    def testAllConstraints(self):
        output, returnVal = pcs(temp_cib, "constraint location D5 prefers node1")
        assert returnVal == 0 and output == "", output

        output, returnVal = pcs(temp_cib, "constraint order Master then D5")
        assert returnVal == 0 and output == "Adding Master D5 (kind: Mandatory) (Options: first-action=start then-action=start)\n", output

        output, returnVal = pcs(temp_cib, "constraint colocation add Master with D5")
        assert returnVal == 0 and output == "", output

        output, returnVal = pcs(temp_cib, "constraint --full")
        assert returnVal == 0
        ac (output,"Location Constraints:\n  Resource: D5\n    Enabled on: node1 (score:INFINITY) (id:location-D5-node1-INFINITY)\nOrdering Constraints:\n  start Master then start D5 (Mandatory) (id:order-Master-D5-mandatory)\nColocation Constraints:\n  Master with D5 (INFINITY) (id:colocation-Master-D5-INFINITY)\n")

        output, returnVal = pcs(temp_cib, "constraint show --full")
        assert returnVal == 0
        ac(output,"Location Constraints:\n  Resource: D5\n    Enabled on: node1 (score:INFINITY) (id:location-D5-node1-INFINITY)\nOrdering Constraints:\n  start Master then start D5 (Mandatory) (id:order-Master-D5-mandatory)\nColocation Constraints:\n  Master with D5 (INFINITY) (id:colocation-Master-D5-INFINITY)\n")

    def testLocationConstraints(self):
        output, returnVal = pcs(temp_cib, "constraint location D5 prefers node1")
        assert returnVal == 0 and output == "", output
        
        output, returnVal = pcs(temp_cib, "constraint location D5 avoids node1")
        assert returnVal == 0 and output == "", output
        
        output, returnVal = pcs(temp_cib, "constraint location D5 prefers node1")
        assert returnVal == 0 and output == "", output
        
        output, returnVal = pcs(temp_cib, "constraint location D5 avoids node2")
        assert returnVal == 0 and output == "", output

        output, returnVal = pcs(temp_cib, "constraint location add location-D5-node1-INFINITY ")
        assert returnVal == 1
        assert output.startswith("\nUsage: pcs constraint"), output

    def testConstraintRemoval(self):
        output, returnVal = pcs(temp_cib, "constraint location D5 prefers node1")
        assert returnVal == 0 and output == "", output
        
        output, returnVal = pcs(temp_cib, "constraint remove blahblah")
        assert returnVal == 1 and output.startswith("Error: Unable to find constraint - 'blahblah'"), output

    def testColocationConstraints(self):
        line = "resource create M1 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create M2 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create M3 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M4 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M5 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M6 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M7 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M8 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M9 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == "",[returnVal, output]

        line = "resource create M10 Dummy --master"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        o, r = pcs(temp_cib, "constraint colocation add D1 D3")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add D1 D2 100")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add D1 D2 -100")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add Master with D5 100")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add master M1-master with master M2-master")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add M3-master with M4-master")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add slave M5-master with started M6-master 500")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add M7-master with Master M8-master")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint colocation add Slave M9-master with M10-master")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint")
        assert r == 0
        ac(o,'Location Constraints:\nOrdering Constraints:\nColocation Constraints:\n  D1 with D3\n  D1 with D2 (100)\n  D1 with D2 (-100)\n  Master with D5 (100)\n  M1-master with M2-master (rsc-role:Master) (with-rsc-role:Master)\n  M3-master with M4-master\n  M5-master with M6-master (500) (rsc-role:Slave) (with-rsc-role:Started)\n  M7-master with M8-master (rsc-role:Started) (with-rsc-role:Master)\n  M9-master with M10-master (rsc-role:Slave) (with-rsc-role:Started)\n')
        
    def testColocationSets(self):
        line = "resource create D7 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D8 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D9 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        o, r = pcs(temp_cib, "constraint colocation set D5 D6 D7 sequential=false set D8 D9 sequential=true setoptions score=INFINITY ")
        ac(o,"")
        assert r == 0

        o, r = pcs(temp_cib, "constraint colocation set D5 D6")
        assert r == 0
        ac(o,"")

        o, r = pcs(temp_cib, "constraint colocation set D5 D6 set D7 D8 set D8 D9")
        assert r == 0
        ac(o,"")

        o, r = pcs(temp_cib, "constraint colocation --full")
        ac(o,"Colocation Constraints:\n  Resource Sets:\n    set D5 D6 D7 sequential=false (id:pcs_rsc_set_D5_D6_D7-1) set D8 D9 sequential=true (id:pcs_rsc_set_D8_D9-1) setoptions score=INFINITY (id:pcs_rsc_colocation_D5_D6_D7_set_D8_D9)\n    set D5 D6 (id:pcs_rsc_set_D5_D6) setoptions score=INFINITY (id:pcs_rsc_colocation_D5_D6)\n    set D5 D6 (id:pcs_rsc_set_D5_D6-1) set D7 D8 (id:pcs_rsc_set_D7_D8) set D8 D9 (id:pcs_rsc_set_D8_D9) setoptions score=INFINITY (id:pcs_rsc_colocation_D5_D6_set_D7_D8_set_D8_D9)\n")
        assert r == 0

        o, r = pcs(temp_cib, "constraint remove pcs_rsc_colocation_D5_D6")
        ac(o,"")
        assert r == 0

        o, r = pcs(temp_cib, "constraint colocation --full")
        ac(o,"Colocation Constraints:\n  Resource Sets:\n    set D5 D6 D7 sequential=false (id:pcs_rsc_set_D5_D6_D7-1) set D8 D9 sequential=true (id:pcs_rsc_set_D8_D9-1) setoptions score=INFINITY (id:pcs_rsc_colocation_D5_D6_D7_set_D8_D9)\n    set D5 D6 (id:pcs_rsc_set_D5_D6-1) set D7 D8 (id:pcs_rsc_set_D7_D8) set D8 D9 (id:pcs_rsc_set_D8_D9) setoptions score=INFINITY (id:pcs_rsc_colocation_D5_D6_set_D7_D8_set_D8_D9)\n")
        assert r == 0

        o, r = pcs(temp_cib, "resource delete D5")
        ac(o,"Removing D5 from set pcs_rsc_set_D5_D6_D7-1\nRemoving D5 from set pcs_rsc_set_D5_D6-1\nDeleting Resource - D5\n")
        assert r == 0
        
        o, r = pcs(temp_cib, "resource delete D6")
        ac(o,"Removing D6 from set pcs_rsc_set_D5_D6_D7-1\nRemoving D6 from set pcs_rsc_set_D5_D6-1\nRemoving set pcs_rsc_set_D5_D6-1\nDeleting Resource - D6\n")
        assert r == 0
        
        o, r = pcs(temp_cib, "constraint ref D7")
        ac(o,"Resource: D7\n  pcs_rsc_colocation_D5_D6_D7_set_D8_D9\n  pcs_rsc_colocation_D5_D6_set_D7_D8_set_D8_D9\n")
        assert r == 0
        
        o, r = pcs(temp_cib, "constraint ref D8")
        ac(o,"Resource: D8\n  pcs_rsc_colocation_D5_D6_D7_set_D8_D9\n  pcs_rsc_colocation_D5_D6_set_D7_D8_set_D8_D9\n")
        assert r == 0
        
    def testOrderSetsRemoval(self):
        o,r = pcs("resource create T0 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T1 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T2 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T3 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T4 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T5 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T6 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T7 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("resource create T8 Dummy")
        ac(o,"")
        assert r == 0
        o,r = pcs("constraint order set T0 T1 T2")
        ac(o,"")
        assert r == 0
        o,r = pcs("constraint order set T2 T3")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint order remove T1")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint order remove T1")
        ac(o,"Error: No matching resources found in ordering list\n")
        assert r == 1

        o,r = pcs("constraint order")
        ac(o,"Ordering Constraints:\n  Resource Sets:\n    set T0 T2\n    set T2 T3\n")
        assert r == 0

        o,r = pcs("constraint order remove T2")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint order")
        ac(o,"Ordering Constraints:\n  Resource Sets:\n    set T0\n    set T3\n")
        assert r == 0

        o,r = pcs("constraint order remove T0")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint order")
        ac(o,"Ordering Constraints:\n  Resource Sets:\n    set T3\n")
        assert r == 0

        o,r = pcs("constraint order remove T3")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint order")
        ac(o,"Ordering Constraints:\n")
        assert r == 0

    def testOrderSets(self):
        line = "resource create D7 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D8 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        line = "resource create D9 Dummy"
        output, returnVal = pcs(temp_cib, line)
        assert returnVal == 0 and output == ""

        o, r = pcs(temp_cib, "constraint order set D5 D6 D7 sequential=false set D8 D9 sequential=true")
        ac(o,"")
        assert r == 0

        o, r = pcs(temp_cib, "constraint order set D5 D6")
        assert r == 0
        ac(o,"")

        o, r = pcs(temp_cib, "constraint order set D5 D6 set D7 D8 set D8 D9")
        assert r == 0
        ac(o,"")

        o, r = pcs(temp_cib, "constraint order --full")
        assert r == 0
        ac(o,"Ordering Constraints:\n  Resource Sets:\n    set D5 D6 D7 sequential=false (id:pcs_rsc_set_D5_D6_D7-1) set D8 D9 sequential=true (id:pcs_rsc_set_D8_D9-1) (id:pcs_rsc_order_D5_D6_D7_set_D8_D9)\n    set D5 D6 (id:pcs_rsc_set_D5_D6) (id:pcs_rsc_order_D5_D6)\n    set D5 D6 (id:pcs_rsc_set_D5_D6-1) set D7 D8 (id:pcs_rsc_set_D7_D8) set D8 D9 (id:pcs_rsc_set_D8_D9) (id:pcs_rsc_order_D5_D6_set_D7_D8_set_D8_D9)\n")

        o, r = pcs(temp_cib, "constraint remove pcs_rsc_order_D5_D6")
        assert r == 0
        ac(o,"")

        o, r = pcs(temp_cib, "constraint order --full")
        assert r == 0
        ac(o,"Ordering Constraints:\n  Resource Sets:\n    set D5 D6 D7 sequential=false (id:pcs_rsc_set_D5_D6_D7-1) set D8 D9 sequential=true (id:pcs_rsc_set_D8_D9-1) (id:pcs_rsc_order_D5_D6_D7_set_D8_D9)\n    set D5 D6 (id:pcs_rsc_set_D5_D6-1) set D7 D8 (id:pcs_rsc_set_D7_D8) set D8 D9 (id:pcs_rsc_set_D8_D9) (id:pcs_rsc_order_D5_D6_set_D7_D8_set_D8_D9)\n")
        
        o, r = pcs(temp_cib, "resource delete D5")
        ac(o,"Removing D5 from set pcs_rsc_set_D5_D6_D7-1\nRemoving D5 from set pcs_rsc_set_D5_D6-1\nDeleting Resource - D5\n")
        assert r == 0
        
        o, r = pcs(temp_cib, "resource delete D6")
        ac(o,"Removing D6 from set pcs_rsc_set_D5_D6_D7-1\nRemoving D6 from set pcs_rsc_set_D5_D6-1\nRemoving set pcs_rsc_set_D5_D6-1\nDeleting Resource - D6\n")
        assert r == 0

    def testLocationConstraintRule(self):
        o, r = pcs(temp_cib, "constraint location D1 prefers rh7-1")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint location D2 prefers rh7-2")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint rule add location-D1-rh7-1-INFINITY #uname eq rh7-1")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint rule add location-D1-rh7-1-INFINITY #uname eq rh7-1")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint rule add location-D1-rh7-1-INFINITY #uname eq rh7-1")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint rule add location-D2-rh7-2-INFINITY date-spec hours=9-16 weekdays=1-5")
        assert r == 0 and o == "", o

        o, r = pcs(temp_cib, "constraint --full")
        assert r == 0
        ac(o,'Location Constraints:\n  Resource: D1\n    Constraint: location-D1-rh7-1-INFINITY\n      Rule: score=INFINITY  (id:location-D1-rh7-1-INFINITY-rule) \n        Expression: #uname eq rh7-1  (id:location-D1-rh7-1-INFINITY-rule-expr-1) \n      Rule: score=INFINITY  (id:location-D1-rh7-1-INFINITY-rule-1) \n        Expression: #uname eq rh7-1  (id:location-D1-rh7-1-INFINITY-rule-1-expr-1) \n      Rule: score=INFINITY  (id:location-D1-rh7-1-INFINITY-rule-2) \n        Expression: #uname eq rh7-1  (id:location-D1-rh7-1-INFINITY-rule-2-expr-1) \n  Resource: D2\n    Constraint: location-D2-rh7-2-INFINITY\n      Rule: score=INFINITY  (id:location-D2-rh7-2-INFINITY-rule) \n        Expression:  (id:location-D2-rh7-2-INFINITY-rule-expr-1) \n          Date Spec: hours=9-16 weekdays=1-5  (id:location-D2-rh7-2-INFINITY-rule-expr-1-datespec) \nOrdering Constraints:\nColocation Constraints:\n')
        
        o, r = pcs(temp_cib, "constraint rule remove location-D1-rh7-1-INFINITY-rule-1")
        ac(o,"Removing Rule: location-D1-rh7-1-INFINITY-rule-1\n")
        assert r == 0
        
        o, r = pcs(temp_cib, "constraint rule remove location-D1-rh7-1-INFINITY-rule-2")
        assert r == 0 and o == "Removing Rule: location-D1-rh7-1-INFINITY-rule-2\n", o

        o, r = pcs(temp_cib, "constraint --full")
        assert r == 0
        ac (o,'Location Constraints:\n  Resource: D1\n    Constraint: location-D1-rh7-1-INFINITY\n      Rule: score=INFINITY  (id:location-D1-rh7-1-INFINITY-rule) \n        Expression: #uname eq rh7-1  (id:location-D1-rh7-1-INFINITY-rule-expr-1) \n  Resource: D2\n    Constraint: location-D2-rh7-2-INFINITY\n      Rule: score=INFINITY  (id:location-D2-rh7-2-INFINITY-rule) \n        Expression:  (id:location-D2-rh7-2-INFINITY-rule-expr-1) \n          Date Spec: hours=9-16 weekdays=1-5  (id:location-D2-rh7-2-INFINITY-rule-expr-1-datespec) \nOrdering Constraints:\nColocation Constraints:\n')

        o, r = pcs(temp_cib, "constraint rule remove location-D1-rh7-1-INFINITY-rule")
        assert r == 0 and o == "Removing Constraint: location-D1-rh7-1-INFINITY\n", o

        o, r = pcs(temp_cib, "constraint --full")
        assert r == 0
        ac (o,'Location Constraints:\n  Resource: D2\n    Constraint: location-D2-rh7-2-INFINITY\n      Rule: score=INFINITY  (id:location-D2-rh7-2-INFINITY-rule) \n        Expression:  (id:location-D2-rh7-2-INFINITY-rule-expr-1) \n          Date Spec: hours=9-16 weekdays=1-5  (id:location-D2-rh7-2-INFINITY-rule-expr-1-datespec) \nOrdering Constraints:\nColocation Constraints:\n')

        o,r = pcs("constraint location D1 rule role=master")
        ac (o,"Error: no rule expression was specified\n")
        assert r == 1

        o,r = pcs("constraint location non-existant-resource rule role=master '#uname' eq rh7-1")
        ac (o,"Error: 'non-existant-resource' is not a resource\n")
        assert r == 1

    def testLocationBadRules(self):
        o,r = pcs("resource create stateful0 Dummy --master")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint location stateful0 rule role=master '#uname' eq rh7-1")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint --full")
        ac(o,"Location Constraints:\n  Resource: stateful0\n    Constraint: location-stateful0\n      Rule: score=INFINITY role=master  (id:location-stateful0-rule) \n        Expression: #uname eq rh7-1  (id:location-stateful0-rule-expr-1) \nOrdering Constraints:\nColocation Constraints:\n")
        assert r == 0

        o,r = pcs("resource create stateful1 Dummy --master")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint location stateful1 rule rulename '#uname' eq rh7-1")
        ac(o,"Error: 'rulename #uname eq rh7-1' is not a valid rule expression\n")
        assert r == 1

        o,r = pcs("constraint location stateful1 rule role=master rulename '#uname' eq rh7-1")
        ac(o,"Error: 'rulename #uname eq rh7-1' is not a valid rule expression\n")
        assert r == 1

        o,r = pcs("constraint location stateful1 rule role=master 25")
        ac(o,"Error: '25' is not a valid rule expression\n")
        assert r == 1

    def testMasterSlaveConstraint(self):
        os.system("CIB_file="+temp_cib+" cibadmin -R --scope nodes --xml-text '<nodes><node id=\"1\" uname=\"rh7-1\"/><node id=\"2\" uname=\"rh7-2\"/></nodes>'")

        o,r = pcs("resource create dummy1 dummy")
        ac(o,"")
        assert r == 0

        o,r = pcs("resource create stateful1 stateful --master")
        ac(o,"")
        assert r == 0

        o,r = pcs("constraint order stateful1 then dummy1")
        ac(o,"Error: stateful1 is a master/slave resource, you must use the master id: stateful1-master when adding constraints\n")
        assert r == 1

        o,r = pcs("constraint order dummy1 then stateful1")
        ac(o,"Error: stateful1 is a master/slave resource, you must use the master id: stateful1-master when adding constraints\n")
        assert r == 1

        o,r = pcs("constraint colocation add stateful1 with dummy1")
        ac(o,"Error: stateful1 is a master/slave resource, you must use the master id: stateful1-master when adding constraints\n")
        assert r == 1

        o,r = pcs("constraint colocation add dummy1 with stateful1")
        ac(o,"Error: stateful1 is a master/slave resource, you must use the master id: stateful1-master when adding constraints\n")
        assert r == 1

        o,r = pcs("constraint order dummy1 then stateful1")
        ac(o,"Error: stateful1 is a master/slave resource, you must use the master id: stateful1-master when adding constraints\n")
        assert r == 1

        o,r = pcs("constraint --full")
        ac(o,"Location Constraints:\nOrdering Constraints:\nColocation Constraints:\n")
        assert r == 0

    def testMissingRole(self):
        os.system("CIB_file="+temp_cib+" cibadmin -R --scope nodes --xml-text '<nodes><node id=\"1\" uname=\"rh7-1\"/><node id=\"2\" uname=\"rh7-2\"/></nodes>'")
        o,r = pcs("resource create stateful0 Stateful --master")
        os.system("CIB_file="+temp_cib+" cibadmin -R --scope constraints --xml-text '<constraints><rsc_location id=\"cli-prefer-stateful0-master\" role=\"Master\" rsc=\"stateful0-master\" node=\"rh7-1\" score=\"INFINITY\"/><rsc_location id=\"cli-ban-stateful0-master-on-rh7-1\" rsc=\"stateful0-master\" role=\"Slave\" node=\"rh7-1\" score=\"-INFINITY\"/></constraints>'")

        o,r = pcs("constraint")
        ac(o,"Location Constraints:\n  Resource: stateful0-master\n    Enabled on: rh7-1 (role: Master)\n    Disabled on: rh7-1 (role: Slave)\nOrdering Constraints:\nColocation Constraints:\n")
        assert r == 0

if __name__ == "__main__":
    unittest.main()

