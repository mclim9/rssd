import argparse
import sys
import glob
import regex
import xml.etree.ElementTree as ET

# Version of script    
__version__ = "6"
# String variable to hold contents to be written to CSV file at the end
csv_output_string = ""
# Supported file types
supported_file_types = ('.rsi', '.xml')

class XmlNode():
    def __init__(self, xml_string=""):
        self.xml_string = xml_string
        
        # Print the XML string (for debugging)
        #print( "Extracted xml string:\n{0}".format( self.xml_string ) )
        
        # Transform the XML string to an Element tree for easy parsing 
        self.root = ET.fromstring(self.xml_string)

    def printToScreen(self, output_string):
        print( output_string )

    def writeToCsv(self, output_string):
        global csv_output_string
        csv_output_string += output_string

    def printNset_AttributeFromNode(self, attribute_name):
        attribute_value = self.root.get(attribute_name)
        self.printToScreen( "\t{0}:\t{1}".format(attribute_name, attribute_value))
        self.writeToCsv("{0},".format(attribute_value))

    def printNset_AttributesFromElement(self, element_name, attributes_list):
        # Find element
        element = self.root.find(element_name)
        
        # Find attributes from element
        for attribute_name in attributes_list:
            attribute_value = element.get(attribute_name)
            self.printToScreen( "\t{0}:\t{1}".format(attribute_name, attribute_value) )
            self.writeToCsv( "{0},".format(attribute_value) )
            

# Parse the input argument & retrieve a list of file paths
def parseInputArguments():
    # Retrieve optional input arguments
    parser = argparse.ArgumentParser(description='Parse RSI or XML license files.Extract some of it\'s contents, print them to screen & create a CSV file with the results')
    parser.add_argument('-f', '--file', type=str, help='name of RSI or XML file, wildcards are also accepted')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    return parser.parse_args()
    

def isFileTypeSupported(args):
    if args.file.endswith(supported_file_types):
        return True
    else:
        print ( "ERROR: Only RSI or XML file extensions are currently supported!" )
        return False


def getListOfFilesFromArgument(args):
    # Check if the file argument was specified
    if not args.file:
        return
    
    inputfiles_list = []
    
    # check the extension names 
    if isFileTypeSupported(args):
        
        inputfiles_list = glob.glob(args.file)
        num_files_found = len(inputfiles_list)
        if (num_files_found > 0):
            ext_name = args.file.split('.')[1]
            print ( "Found {0} {1} file(s)".format(num_files_found, ext_name) )
        else:
            print ( "ERROR: {0} not found".format(args.file) )
            return
        
    return inputfiles_list


def getListOfFilesFromCurrentFolder():
    inputfiles_list = []
    
    for file_type in supported_file_types:
        
        files_list = glob.glob('*' + file_type)
        print ( "Found {0} {1} file(s)".format(len(files_list), file_type) )
                
        inputfiles_list += files_list
    
    return inputfiles_list


def parseInputFile(i, inputfile):
    print ('\n{0}) Loading {1}'.format(i, inputfile) )
    
    global csv_output_string
    csv_output_string += "\n\n%s\n" % inputfile
    
    # Open the file & read the contents into memory
    with open(inputfile, mode='rb') as file: # b is important -> binary
        fileContent_bytes = file.read()
        # To be compliant with Python 3, decode the binary bytes to string
        fileContent_string = fileContent_bytes.decode('utf_8', 'ignore')
    
    # Regex search pattern
    regex_pattern = r'^(<KeyInstallation.*?</KeyInstallation>)\s*\n'
    
    # Extract all XML nodes of type KeyInstallation
    xml_string_list = regex.findall(regex_pattern, fileContent_string, regex.S | regex.M, overlapped=True)
    print ( "\tFound {0} option key XML node(s)".format(len(xml_string_list)) )
    
    #print( xml_string_list )        # Print the list of nodes found (for debugging)
    
    for j, xml_string in enumerate(xml_string_list, 1):
        node = XmlNode(xml_string)
        # List of required attributes
        attributes_list = ['option_type', 'full_name', 'key_type', 'duration']

        #Print CSV Header
        if j ==1:
            csv_output_string += "\nmodel_name,device_id,{0}\n".format(",".join(attributes_list))

        node.printToScreen(" ")
        node.writeToCsv('\n')
        node.printNset_AttributeFromNode('model_name')
        node.printNset_AttributeFromNode('rs_device_id')
        node.printNset_AttributesFromElement('OptionKeyData', attributes_list)
        node.printNset_AttributesFromElement('OptionKey', ['key'])


# Write CSV results to file
def writeResultsToCsv(output_filename):
    print ( "\nWriting results to %s" % output_filename )
    with open(output_filename, 'w') as f:
        f.write(csv_output_string)


def main():
    args = parseInputArguments()
    
    inputfiles_list = getListOfFilesFromArgument(args)
    
    # If no input arguments given, search for files in local directory
    if not (inputfiles_list):
        inputfiles_list = getListOfFilesFromCurrentFolder()
    
    # Loop through all RSI files & retrieve XML content
    for i, inputfile in enumerate(inputfiles_list, 1):
        parseInputFile(i, inputfile)
    
    writeResultsToCsv("parseRSI_results.csv")


main()
