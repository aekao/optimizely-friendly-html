import re
import sys
from bs4 import BeautifulSoup


# Via https://gist.github.com/carlsmith/b2e6ba538ca6f58689b4c18f46fef11c
def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    # Compiles regex pattern into a regex object
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


try:    
    filename = sys.argv[1]
    # If user does not specify a CSS class, then this will format
    # the entire .html file
    try:
        class_to_format = sys.argv[2]
    except:
        class_to_format = None 

    # The following allows the user to specify how many preceding spaces
    # should go in each line. The default is 4.
    try:
        num_preceding_spaces = int(sys.argv[3])
    except: 
        num_preceding_spaces = 4
except:
    print 'python ' + sys.argv[0] + ' [ .html filename ]',
    print '\n\t[ (optional) element class to format ]',
    print '\n\t[ (optional) number of preceding spaces in each line ]'
    sys.exit()

with open(filename) as file:
    soup = BeautifulSoup(file, 'html.parser')

if (class_to_format != None): 
    element = soup.select('.'+class_to_format)
    element_prettified = element[0].prettify()
else:
    element = soup
    element_prettified = element.prettify()

lines = element_prettified.split('\n')
# 122 is the max # of chars that will show on one line in the Optimizely app 
# on my laptop.
# 4 accounts for single quotes, +, and a space.
max_chars = 122 - num_preceding_spaces - 4
glue = ' +\n' + ' ' * num_preceding_spaces
substitutions = {
    "'": r"\'", # Escaping single quotes
    '{': "' + ", # Converting curly braces into JS variables
    '}': " + '"
}

quoted_lines = []
for l in lines:
    if (l.strip()): # Getting rid of empty lines
        l = replace(l, substitutions)
        if (len(l) <= max_chars): 
            l = "'" + l + "'"
            quoted_lines.append(l)
        else:
            # If line is > max chars, then split line by space
            words = l.split(' ')
            char_counter = 0
            tmp_line = ''
            tmp_lines = []
            for w in words:
                char_counter = char_counter + len(w) + 1
                if (char_counter <= max_chars):
                    tmp_line = tmp_line + ' ' + w
                else: 
                    tmp_lines.append("'" + tmp_line + " '")
                    tmp_line = w
                    char_counter = len(w)

            # Append last line from for loop
            tmp_lines.append("'" + tmp_line + "'")
            quoted_lines.append(glue.join(tmp_lines))

output = glue.join(quoted_lines)
# Edge case: if line ends with a JS variable, it will have an extra '' +
output = output.replace("'' +\n", '\n')
print output + ';'

