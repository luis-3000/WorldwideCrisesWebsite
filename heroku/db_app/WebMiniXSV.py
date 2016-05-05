from minixsv import pyxsval as xsv

def check_imported_file(f_xml):
	local_xml_file = open('importXML.xml', 'w')
	local_xml_file.write(f_xml)
	local_xml_file.close()
	try:
		checkImport = xsv.parseAndValidateXmlInput(
		'importXML.xml',
		'importXML.xsd',
		xmlIfClass=xsv.XMLIF_ELEMENTTREE)
		ET = checkImport.getTree()
		root = ET.getroot()
	except xsv.XsvalError:
		return False
	return True