'''
Implements the Deflate (and Inflate) algorithm
'''
from lz77 import LZ77
from huffman import Huffman


class Inflate:
    '''
    Implements Inflate and Deflate
    '''

    def __init__(self) -> None:
        self.huffman = None

    def encode(self, text: str) -> str:
        '''
        Encodes the data
        '''
        lz77 = LZ77()
        code = lz77.code_to_bytes(lz77.encode(text))
        self.huffman = Huffman()
        return self.huffman.encode(code)

    def decode(self, code: str) -> str:
        '''
        Decodes the data
        '''
        lz77 = LZ77()
        lz77_code = self.huffman.decode(code)
        return lz77.decode(lz77.code_from_bytes(lz77_code))


if __name__ == '__main__':
    with open('test_short.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    inflate = Inflate()
    encoded = inflate.encode(data)
    with open('compressed_deflate.txt', 'w', encoding='utf-8') as file:
        file.write(encoded)
    print('Original: ', len(data))
    print('Compressed: ', len(encoded)/8+inflate.huffman.canonical_code())
    assert inflate.decode(encoded) == data
