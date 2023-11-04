import os
import pandas as pd
import polib
import xml.etree.ElementTree as ET
from polib import POFile, POEntry

def file_conversion(input_file, output_format, output_file_name):
    if output_format == 'po':
        if input_file.endswith('.xlsx'):
            return xlsx_to_po(input_file, output_file_name)
        elif input_file.endswith('.xml'):
            return xml_to_po(input_file, output_file_name)
    elif output_format == 'xml':
        if input_file.endswith('.xlsx'):
            return xlsx_to_xml(input_file, output_file_name)
        elif input_file.endswith('.po'):
            return po_to_xml(input_file, output_file_name)
    elif output_format == 'xlsx':
        if input_file.endswith('.po'):
            return po_to_xlsx(input_file, output_file_name)
        elif input_file.endswith('.xml'):
            return xml_to_xlsx(input_file, output_file_name)

def xlsx_to_po(input_xlsx, output_po):
    df = pd.read_excel(input_xlsx)
    po = POFile()

    for index, row in df.iterrows():
        msgid = str(row['Original Text'])  # Convert to string
        msgstr = str(row['Translation'])    # Convert to string

        entry = POEntry(msgid=msgid, msgstr=msgstr)
        po.append(entry)

    output_po = os.path.join('converted', output_po + ".po")
    po.save(output_po)

    return output_po

def xlsx_to_xml(input_xlsx, output_xml):
    df = pd.read_excel(input_xlsx)
    root = ET.Element("resources")

    for index, row in df.iterrows():
        string_element = ET.Element("string")
        string_element.text = str(row['Translation'])
        string_element.set("name", str(row['Original Text']))
        root.append(string_element)

    output_xml = os.path.join('converted', output_xml + ".xml")
    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding='utf-8', xml_declaration=True)

    return output_xml

def xml_to_po(input_xml, output_po):
    tree = ET.parse(input_xml)
    po = POFile()

    for string_element in tree.findall(".//string"):
        msgid = string_element.get("name")
        msgstr = string_element.text

        entry = POEntry(msgid=msgid, msgstr=msgstr)
        po.append(entry)

    output_po = os.path.join('converted', output_po + ".po")
    po.save(output_po)

    return output_po

def po_to_xml(input_po, output_xml):
    po = polib.pofile(input_po)
    root = ET.Element("resources")

    for entry in po:
        string_element = ET.Element("string")
        string_element.text = entry.msgstr
        string_element.set("name", entry.msgid)
        root.append(string_element)

    output_xml = os.path.join('converted', output_xml + ".xml")
    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding='utf-8', xml_declaration=True)

    return output_xml

def po_to_xlsx(input_po, output_xlsx):
    po = polib.pofile(input_po)
    data = {'Original Text': [], 'Translation': []}

    for entry in po:
        data['Original Text'].append(entry.msgid)
        data['Translation'].append(entry.msgstr)

    df = pd.DataFrame(data)
    output_xlsx = os.path.join('converted', output_xlsx + ".xlsx")
    df.to_excel(output_xlsx, index=False)

    return output_xlsx

def xml_to_xlsx(input_xml, output_xlsx):
    tree = ET.parse(input_xml)
    data = {'Original Text': [], 'Translation': []}

    for string_element in tree.findall(".//string"):
        data['Original Text'].append(string_element.get("name"))
        data['Translation'].append(string_element.text)

    df = pd.DataFrame(data)
    output_xlsx = os.path.join('converted', output_xlsx + ".xlsx")
    df.to_excel(output_xlsx, index=False)

    return output_xlsx
