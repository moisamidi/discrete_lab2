"""
Implements Huffman algorithm
"""


class Node:
    '''
    A node class for the Huffman tree
    '''

    def __init__(self, frequency, letter=None, left=None, right=None):
        self.frequency = frequency
        self.letter = letter
        self.code = ''
        self.left = left
        self.right = right


class Huffman:
    '''
    Implements the Huffman algorithm
    '''

    def __init__(self):
        self.tree_root = None
        self.codes = {}

    def probabilities(self, text: str) -> list:
        '''
        Returns a list of leaf nodes
        '''
        probs = {}
        for symbol in text:
            if symbol not in probs:
                probs[symbol] = 1
            else:
                probs[symbol] += 1
        return sorted([Node(letter=letter, frequency=amount/len(text))
                       for letter, amount in probs.items()],
                      key=lambda node: node.frequency, reverse=True)

    def make_tree(self, probs) -> None:
        '''
        Makes a Huffman tree
        '''
        while len(probs) > 2:
            probs.sort(key=lambda node: node.frequency, reverse=True)
            first = probs[-1]
            second = probs[-2]
            probs = probs[:-2]
            probs.append(
                Node(frequency=first.frequency+second.frequency, left=first, right=second),)
        probs.sort(key=lambda node: node.frequency, reverse=True)
        first = probs[-1]
        second = probs[-2]
        self.tree_root = Node(frequency=first.frequency +
                              second.frequency, left=first, right=second)

    def create_codes(self, node: Node, code: str = '') -> None:
        '''
        Creates a codes dict for the given tree
        '''
        if node.left and node.right:
            self.create_codes(node.left, code+'0')
            self.create_codes(node.right, code+'1')
        else:
            self.codes[node.letter] = code
            node.code = code

    def encode(self, text: str) -> str:
        '''
        Encodes text
        '''
        self.tree_root = None
        self.codes = {}
        probs = self.probabilities(text)
        if len(probs) == 1:
            self.tree_root = probs[0]
            self.tree_root.code = '0'
            self.codes[self.tree_root.letter] = '0'
        else:
            self.make_tree(probs)
            self.create_codes(self.tree_root)
        code_table = text.maketrans(self.codes)
        return text.translate(code_table)

    def decode(self, code: str) -> str:
        '''
        Decodes a string
        '''
        decoded_text = ''
        node = self.tree_root
        for bit in code:
            if not (node.right and node.left):  # single letter string case
                decoded_text += node.letter
                node = self.tree_root
                continue
            if bit == '1':
                node = node.right
            else:
                node = node.left
            if not (node.right and node.left):
                decoded_text += node.letter
                node = self.tree_root
        return decoded_text

    def canonical_code(self):
        '''
        Returns the size of the dict as canonical codes
        '''
        size = 0
        for code in self.codes.values():
            size += len(bin(len(code))[2:])+len(str(code))
        return size


if __name__ == '__main__':
    with open('test_short.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    huffman = Huffman()
    encoded = huffman.encode(data)
    with open('compressed_huffman.txt', 'w', encoding='utf-8') as file:
        file.write(encoded)
    print('Original: ', len(data))
    print('Compressed: ', len(encoded)/8+huffman.canonical_code())
    assert huffman.decode(encoded) == data
