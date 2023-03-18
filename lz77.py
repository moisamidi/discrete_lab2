'''
Implements four compression algorithms
'''


class LZ77:
    '''
    Implements the LZ77 algorithm'''

    def encode(self, text: str, window_length: int = 32768, max_offset: int = 255) -> list:
        '''
        Encodes the text as a list of tuples
        '''
        compressed_data = []
        window = ''
        while text:
            window = window[-window_length:]
            length, offset = 1, 0
            for i in range(min(len(window)-1, max_offset), -1, -1):
                if window[i] == text[0]:
                    found_length = self.repetition_length(
                        window[i:], text
                    )
                    if found_length > length:
                        offset = len(window)-i
                        length = found_length
            if offset == 0:
                compressed_data.append((0, 1, text[0]))
            else:
                compressed_data.append((offset, length, ''))
            window += text[:length]
            text = text[length:]
        return compressed_data

    def repetition_length(self, window, text):
        '''
        Finds how long the window repeats for
        '''
        length = 0
        while text:
            if window[0] == text[0]:
                length += 1
                window = window[1:] + text[0]
                text = text[1:]
            else:
                break
        return length

    def code_to_bytes(self, code: list) -> str:
        '''
        Compresses the code to bytes
        '''
        optimized_code = ''
        for offset, length, letter in code:
            if offset > 0:
                optimized_code += f'{offset}/{length}|'
            else:
                optimized_code += f'{letter}|'
        return optimized_code[:-1]

    def code_from_bytes(self, bytes_str: str) -> list:
        '''
        Compresses the code from bytes
        '''
        code = []
        for line in bytes_str.split('|'):
            if '/' not in line:
                if line == '':
                    if code[-1] != (0, 1, '|'):
                        code.append((0, 1, '|'))
                else:
                    code.append((0, 1, line))
            else:
                offset, length = line.split('/')
                if offset == '':
                    code.append((0, 1, '/'))
                else:
                    code.append((int(offset), int(length), ''))
        return code

    def decode(self, code: list) -> str:
        '''
        Decodes the text from a list of tuples
        '''
        decoded_text = ""
        index = 0
        for offset, length, letter in code:
            if offset == 0:
                index += 1
                decoded_text += letter
                continue
            while length > 0:
                decoded_text += decoded_text[index-offset]
                index += 1
                length -= 1
        return decoded_text


if __name__ == '__main__':
    lz77 = LZ77()
    with open('test_short.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    encoded = lz77.encode(data)
    encoded_compressed = lz77.code_to_bytes(encoded)
    with open('compressed_lz77.txt', 'w', encoding='utf-8') as file:
        file.write(encoded_compressed)
    print('Original: ', len(data))
    print('Compressed: ', len(encoded_compressed))
    assert lz77.decode(encoded) == data
    assert lz77.decode(lz77.code_from_bytes(encoded_compressed)) == data
