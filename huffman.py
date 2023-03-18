"""
Implements Huffman algorithm
"""


class Huffman:
    '''
    Implements the Huffman algorithm
    '''

    def __init__(self, string):
        self.string = string
        self.dict_letters = {}
        self.probabil_list = []
        self.help_list = []

    def create_dict(self):
        '''
        Creates a dictionary for encoding
        '''
        for letter in self.string:
            if letter in self.dict_letters:
                self.dict_letters[letter][0] += 1
            else:
                self.dict_letters[letter] = [1, 0, [], False]
        for letter, value in self.dict_letters.items():
            value[1] = value[0] / len(
                self.string
            )
            self.probabil_list.append((value[1], letter))
            # check if it is a list
            if not isinstance(value[2], list):
                value[2] = []  # initialize as empty list
            self.probabil_list.append((value[1], letter))

        while len(self.probabil_list) > 1:
            self.probabil_list.sort()
            new_elem = (
                self.probabil_list[0][0] + self.probabil_list[1][0],
                self.probabil_list[0][1] + self.probabil_list[1][1],
            )
            for elem in self.probabil_list[0][1]:
                for letter, value in self.dict_letters.items():
                    if elem == letter:
                        value[2].append(1)
            for elem in self.probabil_list[1][1]:
                for letter, value in self.dict_letters.items():
                    if elem == letter:
                        value[2].append(0)
            self.probabil_list = self.probabil_list[2:]
            self.probabil_list.append(new_elem)
        return self.dict_letters

    def encode(self):
        '''
        Encodes a string
        '''
        for value in self.dict_letters.values():
            code = value[2]
            code.reverse()
            encode_val = ""
            for i in code:
                encode_val += str(i)
            value[2] = encode_val
        encoded_string = self.string
        for letter, value in self.dict_letters.items():
            encoded_string = encoded_string.replace(
                letter, value[2])
        return encoded_string

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


if __name__ == '__main__':
    INPUT_FILE = 'test_short.txt'
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        contents = f.read()
    huff = Huffman(contents)
    huff.create_dict()
    encoded_contents = huff.encode()
    # print(encoded_contents)
    decoded_contents = huff.decode(encoded_contents)
    # print(decoded_contents)
    assert decoded_contents == contents
