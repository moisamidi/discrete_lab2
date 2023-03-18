"""
Implements the LZW algotithm
"""


class LZW:
    """
    Implements the LZW algotithm
    """

    def __init__(self):
        self.saver = {chr(i): i for i in range(256)}
        self.num = 256

    def encode(self, text: str) -> str:
        '''
        Compresses the information
        '''
        compressed_data = []
        number = 1
        cur_el = text[0]

        while number < len(text):
            if cur_el + text[number] in self.saver:
                cur_el = cur_el + text[number]
                number += 1
            else:
                compressed_data.append(self.saver[cur_el])
                self.saver[cur_el + text[number]] = self.num
                self.num += 1
                cur_el = text[number]
                number += 1
        compressed_data.append(self.saver[cur_el])
        return ' '.join([str(code) for code in compressed_data])

    def decode(self, code: str) -> str:
        '''
        Decompresses the compressed information
        '''
        new_saver = {value: key for key, value in self.saver.items()}
        decoded_text = ''
        for element in code.split(' '):
            decoded_text += new_saver[int(element)]
        return decoded_text


if __name__ == '__main__':
    with open('test_short.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    lzw = LZW()
    encoded = lzw.encode(data)
    with open('compressed_LZW.txt', 'w', encoding='utf-8') as file:
        file.write(str(encoded))
    print('Original: ', len(data))
    print('Compressed: ', len(encoded))
    assert lzw.decode(encoded) == data
