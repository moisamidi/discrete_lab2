"""Implements Huffman algorithm"""
class Huffman:
    'implements Huffman algorithm'
    def __init__(self, string):
        self.string = string
        self.dict_letters = {}
        self.probabil_list = []
        self.help_list = []

    def create_dict(self):
        'create dictionary to encode'
        for letter in self.string:
            if letter in self.dict_letters:
                self.dict_letters[letter][0] += 1
            else:
                self.dict_letters[letter] = [1, 0, [], False]
        for letter in self.dict_letters:
            self.dict_letters[letter][1] = self.dict_letters[letter][0] / len(
                self.string
            )
            self.probabil_list.append((self.dict_letters[letter][1], letter))
            if not isinstance(self.dict_letters[letter][2], list): # check if it is a list
                self.dict_letters[letter][2] = []  # initialize as empty list
            self.probabil_list.append((self.dict_letters[letter][1], letter))

        while len(self.probabil_list) > 1:
            self.probabil_list.sort()
            new_elem = (
                self.probabil_list[0][0] + self.probabil_list[1][0],
                self.probabil_list[0][1] + self.probabil_list[1][1],
            )
            for elem in self.probabil_list[0][1]:
                for letter in self.dict_letters:
                    if elem == letter:
                        self.dict_letters[letter][2].append(1)
            for elem in self.probabil_list[1][1]:
                for letter in self.dict_letters:
                    if elem == letter:
                        self.dict_letters[letter][2].append(0)
            self.probabil_list = self.probabil_list[2:]
            self.probabil_list.append(new_elem)
        return self.dict_letters

    def encode(self):
        'encode a sstring'
        for letter in self.dict_letters:
            code = self.dict_letters[letter][2]
            code.reverse()
            encode_val = ""
            for i in code:
                encode_val += str(i)
            self.dict_letters[letter][2] = encode_val
            # print(f"{letter}: {encode_val}")
        encoded_string = self.string
        for key in list(self.dict_letters.keys()):
            encoded_string = encoded_string.replace(key, self.dict_letters[key][2])
        return encoded_string

    def decode(self, encoded_string):
        'decode a compressed string'
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



input_file = 'input.txt'
with open(input_file, 'r', encoding='utf-8') as f:
    contents = f.read()
huff = Huffman(contents)
huff.create_dict()
encoded_contents = huff.encode()
# print(encoded_contents)
decoded_contents = huff.decode(encoded_contents)
# print(decoded_contents)
assert decoded_contents == contents
