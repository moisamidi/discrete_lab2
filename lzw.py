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

    def compress(self, inform):
        '''
        Compresses the information
        '''
        res = []
        number = 1
        cur_el = inform[0]

        while number < len(inform):
            if cur_el + inform[number] in self.saver:
                cur_el = cur_el + inform[number]
                number += 1
            else:
                res.append(self.saver[cur_el])
                self.saver[cur_el + inform[number]] = self.num
                self.num += 1
                cur_el = inform[number]
                number += 1
        res.append(self.saver[cur_el])
        return res

    def decompress(self, res):
        '''
        Decompresses the compressed info
        '''
        new_saver = {value: key for key, value in self.saver.items()}
        string = ''
        for element in res:
            string += new_saver[element]
        return string


if __name__ == '__main__':
    INPUT_FILE = 'test_short.txt'
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        contents = f.read()
    lzw = LZW()
    encoded_contents = lzw.compress(contents)
    # print(encoded_contents)
    decoded_contents = lzw.decompress(encoded_contents)
    # print(decoded_contents)
    assert decoded_contents == contents
