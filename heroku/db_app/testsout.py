"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# -------
# imports
# -------

import sys
import StringIO
import unittest
import datetime

import xml.etree.ElementTree as ET

from models import Crisis, Person, Organization

#from importXML import make_common, eval_crises, eval_people, eval_organizations, listings, import_xml_solve

import importXML as ixml

#from exportXML import eval_links, eval_textfield, eval_common, eval_crises, eval_organizations, eval_people, export_xml_solve 

import exportXML as exml
# Global node_height

ixml.import_xml_solve("Tests.in")

node_height = 0

"""
To test the program:
    % python tests.py >& tests.py.out
    % chmod ugo+x tests.py
    % tests.py >& tests.py.out
"""

from django.test import TestCase


class SimpleTest(TestCase): 
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


"""
eval_links(str_field, node, common)
eval_textfield(str_field, node, main)
eval_common(m, main)
eval_crises(crisis, root)
eval_organizations(org, root)
eval_people(people, root)
export_xml_solve(c, o, p)
"""

    def test_eval_links_1(self):
        child = ET.fromstring('<Organization ID="' + o.wcdb_id + '" Name="' + o.name + '" />')
        
        eval_links(str_history, history, child)


    def test_eval_links_2(self):

    def test_eval_links_3(self):


    def test_eval_textfield_1(self):

    def test_eval_textfield_2(self):

    def test_eval_textfield_3(self):


    def test_eval_common_1(self):

    def test_eval_common_2(self):

    def test_eval_common_3(self):


    def test_eval_crises_1(self):
        test = Crisis.objects.all()
        self.assert_(test[0].wcdb_id ==  "CRI_KATRIN")
    def test_eval_crises_2(self):

    def test_eval_crises_3(self):


    def test_eval_organizations_1(self):

    def test_eval_organizations_2(self):

    def test_eval_organizations_3(self):


    def test_eval_people_1(self):

    def test_eval_people_2(self):

    def test_eval_people_3(self):


    def test_export_xml_solve_1(self):

    def test_export_xml_solve_2(self):

    def test_export_xml_solve_3(self):
        

    # -----------
    # make_common
    # -----------
    
    # Make sure tags inside the <Common> tag match (Only one test could be made?)
    def test_make_common_1 (self) :
        model_instance = ContentType.objects.get(app_label=u'someapp', model=modelNameStr).model_class()(**{fieldNameStr: ForeignModelInstance})
        r = StringIO.StringIO("<Citations></Citations><ExternalLinks></ExternalLinks><Images></Images><Videos></Videos><Maps></Maps><Feeds></Feeds><Summary></Summary>");
        root = make_common(r)
        self.assert_(root.tag == "Citations")

"""
    # Will this fail?
    # Testing outer tag by itself
"""
    def test_make_common_2 (self) :
        r = StringIO.StringIO("<Citations></Citations>");
        root = make_common(r)
        self.assert_(root.tag == "Citations")

"""
    # Will this fail?
    # Testing last tag by itself
"""
    def test_make_common_3 (self) :
        r = StringIO.StringIO("<Summary></Summary>");
        root = make_common(r)
        self.assert_(root.tag == "Summary")

"""
    # Will this fail?
    # Testing middle tag by itself
"""
    def test_make_common_4 (self) :
        r = StringIO.StringIO("<Summary></Summary>");
        root = make_common(r)
        self.assert_(root.tag == "Summary")    

    # Will this fail?
    # Testing a an empty tag
    def test_make_common_5 (self) :
        r = StringIO.StringIO("");
        root = make_common(r)
        self.assert_(root.tag == "")


"""
# (For these I guess we just have to run each test with a particular input and copy and paste the result to be our "resulting string")

    # ---------
    # cris_eval    
    # ---------
"""

"""
    # empty 'crisis' input
"""
    def test_cris_eval_1 (self) :
        crisis_name = ""        
        result = cris_eval(crisis_name)
        print "result: ",result
        self.assert_(result == "")          

"""
    # crisis with info in it
"""
    def test_cris_eval_2 (self) :
        crisis_name = "Katrina"      # Hurricane Katrina  
        result = cris_eval(crisis_name)
        print "result: ",result
        self.assert_(result == "??")

    # non-existen crisis name in our database
    def test_cris_eval_3 (self) :
        crisis_name = "Hurrican Sandy"        
        result = cris_eval(crisis_name)
        print "result: ",result
        self.assert_(result == "??")



"""
    # -----------
    # person_eval
    # -----------

    # empty 'person' input
"""

    def test_person_eval_1 (self) :
        person_name = ""        
        result = person_eval(person_name)
        print "result: ",result
        self.assert_(result == "")          
        
    # person name existent in our database
    def test_person_eval_2 (self) :
        person_name = "George W. Bush"       
        result = person_eval(person_name)
        print "result: ",result
        self.assert_(result == "George W. Bush")        

    # person name non-existent in our database
    def test_person_eval_3 (self) :
        person_name = "Bill Clinton"        
        result = person_eval(person_name)
        print "result: ",result
        self.assert_(result == "")         


"""
    # --------
    # org_eval
    # --------

    # empty 'organization' input
"""
    def test_org_eval_1 (self) :
        org_name = ""        
        result = org_eval(org_name)
        print "result: ",result
        self.assert_(result == "")          

    # organization name existent in our database
    def test_org_eval_2 (self) :
        org_name = ""        
        result = org_eval(org_name)
        print "result: ",result
        self.assert_(result == "??")          

    # organization name non-existent in our database
    def test_org_eval_3 (self) :
        org_name = ""        
        result = org_eval(org_name)
        print "result: ",result
        self.assert_(result == "??")          

        
"""
    # -----------
    # eval_crises
    # -----------

    # evaluate empty 'crises' input
"""
    def test_eval_crises_1 (self) :
        r = StringIO.StringIO(""); # Maybe this cannot be emtpy?
        root = eval_crises (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "")          
     
    # evaluate one crisis
    def test_eval_crises_2 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>");
        root = eval_crises (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")          

    # evaluate 2 crises
    def test_eval_crises_3 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>");
        root = eval_crises (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")   

    # evaluate all crises (This is going to be a very long result string)
    def test_eval_crises_4 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>");
        root = eval_crises (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")        

    # evaluate non-existent crises in our database <--- Do we pass an invalid tree?
    def test_eval_crises_5 (self) :
        r = StringIO.StringIO("<WorldCrises><InvalidCrisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></InvalidCrisis></WorldCrises>");
        root = eval_crises (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")         

   
"""
    # -----------
    # eval_people
    # -----------

    # an empty 'people' request
"""
    def test_eval_people_1 (self) :
        r = StringIO.StringIO(""); # Maybe this cannot be emtpy?
        root = eval_people (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "")          

    # Evaluate one person
    def test_eval_people_2 (self) :
        r = StringIO.StringIO("<WorldCrises><People></People></WorldCrises>");
        root = eval_people (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "")         

    # Evaluate two people
    def test_eval_people_3 (self) :
        r = StringIO.StringIO("<WorldCrises><People></People><People></People></WorldCrises>");
        root = eval_people (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")           

    # Evaluate ALL people in our database
    def test_eval_people_4 (self) :
        r = StringIO.StringIO("<WorldCrises><People></People><People></People><People></People><People></People><People></People><People></People><People></People><People></People><People></People><People></People></WorldCrises>");
        root = eval_people (r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??") 

"""
    # ------------------
    # eval_organizations
    # ------------------

    # an empty 'organizations' request
"""

    def test_eval_organizations_1 (self) :
        r = StringIO.StringIO(""); # Maybe this cannot be emtpy?
        root = eval_organizations(r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "")        

    # Evaluate one 'organizations' request
    def test_eval_organizations_2 (self) :
        r = StringIO.StringIO("<WorldCrises><Organizations></Organizations></WorldCrises>");
        root = eval_organizations(r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "")         

    # Evaluate two 'organizations' request
    def test_eval_organizations_3 (self) :
        r = StringIO.StringIO("<WorldCrises><Organizations></Organizations><Organizations></Organizations></WorldCrises>");
        root = eval_organizations(r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")  

    # Evaluate ALL (10) 'organizations' request
    def test_eval_organizations_4 (self) :
        r = StringIO.StringIO("<WorldCrises><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations><Organizations></Organizations></WorldCrises>");
        root = eval_organizations(r)
        result = ""
        for child in root :
            print child.tag, child.attrib
            c = child.tag
            a = child.attrib
            result += c
            result += a

        print "result: ",result
        self.assert_(result == "??")       

                

"""
    # --------
    # listings
    # --------

    # Evaluate an empty 'listings' request
"""

    def test_listings_1 (self) :
        r = StringIO.StringIO(""); # Maybe this cannot be emtpy?     
        result = listings (r)       # returns a string
        print "result: ",result
        self.assert_(result == "")          

    # Evaluate one 'listings' request
    def test_listings_2 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>");
        result = listings (r)
        print "result: ",result
        self.assert_(result == "")         

    # Evaluate two 'listings' request
    def test_listings_3 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>");
        result = listings (r)
        print "result: ",result
        self.assert_(result == "??")  

    # Evaluate ALL 'listings' (This will be a very long string)
    def test_listings_4 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>");
        result = listings (r)
        print "result: ",result
        self.assert_(result == "??")        

    

"""
    # --------
    # xml_eval
    # --------

    # Test empty tree?
"""
    def test_xml_eval_1 (self) :
        s = ""
        root = ET.fromstring(s)
        result = xml_eval (root);
        print "test_xml_eval_1 -> result: ",result
        self.assert_(result    == ??)


    # Test one crisis.
    def test_xml_eval_2 (self) :
        s = "<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>"
        root = ET.fromstring(s)
        result = xml_eval (root);
        print "test_xml_eval_2 -> result: ",result
        self.assert_(result    == ??)

    # Test two crises
    def test_xml_eval_3 (self) :
        s = "<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>"
        root = ET.fromstring(s)
        o = xml_eval (root);
        print "test_xml_eval_3 -> result: ",result
        self.assert_(o == ??)

    # Test ALL crises
    def test_xml_eval_3 (self) :
        s = "<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>"
        root = ET.fromstring(s)
        o = xml_eval (root);
        print "test_xml_eval_3 -> result: ",result
        self.assert_(o == ??)


"""
    # ---------
    # xml_solve
    # ---------

    # Test with empty tree?
"""
    def test_xml_solve_1 (self) :
        r = StringIO.StringIO("")
        w = StringIO.StringIO()
        xml_solve (r, w)
        self.assert_(w.getvalue() == "") # ??
    
    # Test with one crisis
    def test_xml_solve_2 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>")
        w = StringIO.StringIO()
        xml_solve (r, w)
        self.assert_(w.getvalue() == "??")

    # Test with two crises
    def test_xml_solve_3 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>")
        w = StringIO.StringIO()
        xml_solve (r, w)
        self.assert_(w.getvalue() == "??")

    # Test with ALL crises
    def test_xml_solve_4 (self) :
        r = StringIO.StringIO("<WorldCrises><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis><Crisis><People></People><Organizations><></></Organizations><Kind></Kind><Date></Date><Time></Time><Locations></Locations><HumanImpact></HumanImpact><EconomicImpact></EconomicImpact><ResourcesNeeded></ResourcesNeeded><Common></Common></Crisis></WorldCrises>")
        w = StringIO.StringIO()
        xml_solve (r, w)
        self.assert_(w.getvalue() == "??")
      
