# from plistlib import loads, load
from __future__ import print_function
import sys
import json


file = '/Users/lizet/Code/nissan/servicio/ios/base.xcodeproj/project.pbxproj'
file = '/Users/lizet/Desktop/asopota.pbxproj'

BRACE = 0
KEY = 1
ITEM = 2
VALUE = 4
ARRAY = 5

class Node:
    def __init__(self, parent=None, value={}):
        self.parent = parent
        self.value = value

    def __setitem__(self, key, value):
        if isinstance(value, Node):
            value.parent = self
            self.value[key].value = value.value
        elif self.value is not None:
            if key in self.value:
                self.value[key].value = value
            else:
                self.value[key] = Node(parent=self, value=value)

    def __getitem__(self, key):
        return self.value[key] if isinstance(self.value, dict) else None

    def __repr__(self):
        if isinstance(self.value, int):
            return str(self.value)
        elif isinstance(self.value, str):
            return repr(self.value)
        else:
            return str(self.value)

    def append(self, value):
        if isinstance(value, Node):
            value.parent = self
        else:
            value = Node(value=value, parent=self)
        if isinstance(self.value, list):
            self.value.append(value)


LAST = -1

offset = 0
expect_eol = False
in_comment = False
comment = None
stack = [VALUE]
keyname = ''
varchars = [chr(x) for x in range(ord('a'), ord('z') + 1)] \
         + [chr(x) for x in range(ord('A'), ord('Z') + 1)] \
         + [chr(x) for x in range(ord('0'), ord('9') + 1)] \
         + ['_']
numchars = '0123456789'
tree = None
comments = []
current = None
ident = ''

with open(file, 'r') as f:
    data = f.read()
    ldata = len(data)

while True:
    try:
        if offset >= ldata:
            print('END BY DATA MISSING')
            break

        if not stack:
            print('END BY STACK EMPTY')
            break

        if stack[LAST] == BRACE: # in
            if data[offset] in varchars:
                index = offset
                while True:
                    c = data[index]
                    if c not in varchars:
                        keyname = data[offset:index]
                        if current:
                            current[keyname] = None
                            current = current[keyname]
                        stack.append(ITEM)
                        stack.append(KEY)

                        print(ident + keyname, end='')
                        break
                    index += 1

                offset = index
                
            elif data[offset] == '}':
                ident = ident[:-2]
                print(ident+'}', end='');
                stack.pop()
                offset += 1

            else:
                offset += 1
            
        elif stack[LAST] == KEY:
            if data[offset] == '=':
                print(' = ', end='')
                stack[LAST] = VALUE
            offset += 1
            
        elif stack[LAST] == ARRAY:
            stack.pop()
            print(ident+')', end='')
            offset += 1

        elif stack[LAST] == VALUE:
            if data[offset] in varchars:
                index = offset
                while True:
                    c = data[index]
                    if c not in varchars:
                        value = data[offset:index]
                        
                        if stack[-2] == ITEM and stack[-3] == ARRAY:
                            # Si el carcter despues es una coma,
                            #podría causar conflicto y nunca encontrar
                            #la coma
                            print(ident+value, end='')

                            if current:
                                node = Node(parent=current, value=value)
                                current.append(node)
                                current = node
                                stack.pop() # VALUE -> ITEM para esperar ","
  
                        else:
                            print(value, end='')
                            current.value = value
                            stack.pop() # VALUE -> ITEM
                        break
                    index += 1

                offset = index

            elif data[offset] == '{':
                if not current:
                    print('{'); ident += '  '
                    tree = Node()
                    current = tree
                else:
                    print('{'); ident += '  '
                    current.value = {}
                    
                stack[LAST] = BRACE
                offset += 1

            elif data[offset] == '(':
                print((ident if stack[-3] == ARRAY else '') + '('); ident += '  '

                stack[LAST] = ARRAY
                stack.append(ITEM)
                stack.append(VALUE)

                if current.value is None:
                    current.value = []

                elif isinstance(current.value, list):
                    node = Node(parent=current, value=[])
                    current.append(node)
                    current = node

                offset += 1

            elif data[offset] == ')':
                if stack[-2] == ITEM and stack[-3] == ARRAY:
                    ident = ident[:-2]
                    
                    stack.pop() # VALUE
                    stack.pop() # ITEM
                else:
                    offset += 1

            else:
                offset += 1
            
        elif stack[LAST] == ITEM:
            if stack[-2] == BRACE and data[offset] == ';':
                print(';')
                if current:
                    current = current.parent
                stack.pop()
            elif stack[-2] == ARRAY and data[offset] == ',':
                print(',')
                current = current.parent
                stack.append(VALUE)
            
            offset += 1
             
        else:
            offset += 1

    except AttributeError as error:
        print(error)
        raise Exception() from error
        break

    except TypeError as error:
        print(error)
        raise error
        break

print('\n')
print(stack)
print(str(tree))
