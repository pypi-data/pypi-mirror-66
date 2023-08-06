# Farm GHG calculation based on Penn State University "FEAT" model.
# python3.7+ code by Pasquale Papparella
#
# Contact: pasquale.papparella@pm.me
# see LICENSE file.
    
def recursive_items(dictionary):

    '''
    
    Rapid un-packing of dictionary in (key, value) pair; use in class 
    or with list(recursive_items(dictionary)) to print results in console.
    Valid for 1-to-Infinite levels dict.
    
    :param dict dictionary: dict to execute unpacking on
    :rtype: tuple
    
    '''

    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)
            
        
def multireplace(string, replacements):
    
    import re
    
    '''
    
    Given a string and a replacement map, it returns the replaced string.

    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :rtype: str

    '''
    
    # Place longer ones first to keep shorter substrings from matching
    # where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against 
    # the string 'hey abc', it should produce 'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)
