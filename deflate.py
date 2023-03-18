'''
Implements the Deflate (and Inflate) algorithm
'''
import sys
from lz77 import LZ77


class Inflate:
    '''
    Implements Inflate and Deflate
    '''

    def __init__(self) -> None:
        self.offset_and_letter_code = None
        self.length_code = None

    def encode(self, text):
        '''
        Encodes the data
        '''
        lz77 = LZ77()
        code = lz77.encode(text)
        offsets = [str(elem[0]) for elem in code]
        lengths = [str(elem[1]) for elem in code]
        letters = [elem[2] for elem in code]
        self.offset_and_letter_code = Huffman(offsets+letters)
        self.length_code = Huffman(lengths)
        new_code = ''
        for offset, length, letter in code:
            new_code += f'{self.offset_and_letter_code.encode(str(offset))} \
{self.length_code.encode(str(length))} \
{self.offset_and_letter_code.encode(letter)} '
        return new_code[:-1]

    def decode(self, code):
        '''
        Decodes the data
        '''
        code = code.split(' ')
        buffer = []
        lz77_code = []
        lz77 = LZ77()
        while code:
            buffer.append(int(self.offset_and_letter_code.decode(code[0])))
            buffer.append(int(self.length_code.decode(code[1])))
            letter = self.offset_and_letter_code.decode(code[2])
            if letter==' ':
                buffer.append(letter)
            elif letter:
                buffer.append(letter[0])
            else:
                buffer.append('')
            lz77_code.append(tuple(buffer))
            buffer = []
            code = code[3:]
        return lz77.decode(lz77_code)


class Huffman:
    '''
    Implements Huffman algorithm
    '''

    def __init__(self, list_of_letters):
        self.list_of_letters = list_of_letters
        self.dict_letters = {}
        self.probabil_list = []
        self.help_list = []
        self.create_dict()

    def create_dict(self):
        '''
        Creates a dictionary to encode the string
        '''
        for letter in self.list_of_letters:
            if letter in self.dict_letters:
                self.dict_letters[letter][0] += 1
            else:
                self.dict_letters[letter] = [1, 0, [], False]
        for letter, code in self.dict_letters.items():
            code[1] = code[0] / len(
                self.list_of_letters
            )
            self.probabil_list.append((code[1], letter))
        while len(self.probabil_list) > 1:
            self.probabil_list.sort()
            new_elem = (
                self.probabil_list[0][0] + self.probabil_list[1][0],
                self.probabil_list[0][1] + ' ' + self.probabil_list[1][1],
            )
            for elem in self.probabil_list[0][1].split(' '):
                for letter, code in self.dict_letters.items():
                    if elem == letter:
                        code[2].append(1)
            for elem in self.probabil_list[1][1].split(' '):
                for letter, code in self.dict_letters.items():
                    if elem == letter:
                        code[2].append(0)
            self.probabil_list = self.probabil_list[2:]
            self.probabil_list.append(new_elem)
        for letter, value in self.dict_letters.items():
            code = value[2]
            code.reverse()
            encode_val = ""
            for i in code:
                encode_val += str(i)
            self.dict_letters[letter][2] = encode_val
        return self.dict_letters

    def encode(self, char):
        '''
        Encodes a character
        '''
        return self.dict_letters[char][2]

    def decode(self, encoded_string):
        '''
        Decodes a compressed string
        '''
        decoded_string = ""
        saver = []
        for letter in list(self.dict_letters.keys()):
            saver.append(self.dict_letters[letter][2])
        saver.sort(reverse=True)
        while encoded_string:
            for elem in saver:
                if encoded_string.startswith(elem):
                    decoded_string += dict(
                        (value[2], key) for (key, value) in self.dict_letters.items()
                    )[elem]
                    encoded_string = encoded_string.removeprefix(elem)
        return decoded_string


lz77 = LZ77()
inflate = Inflate()
with open('test_short.txt', 'r', encoding='utf-8') as file:
    text = file.read()
code = lz77.code_to_bytes(lz77.encode(text))
new_code = inflate.encode(text)
print('Original: ', sys.getsizeof(code))
print('Compressed: ', sys.getsizeof(new_code))
decoded = inflate.decode(new_code)
