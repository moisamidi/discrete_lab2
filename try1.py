'''
Plots graphs for testing
'''
import time
import random
import matplotlib.pyplot as plt
from huffman import Huffman
from lz77 import LZ77
from lzw import LZW

# initialize Huffman and LZW classes
huffman = Huffman()
lzw = LZW()
lz77 = LZ77()

input_sizes = [10**i for i in range(1, 5)]

huffman_times = []
lzw_times = []
lz77_times = []


def generate_string(length: int) -> str:
    '''
    Generates a string for testing
    '''
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))


for size in input_sizes:
    print(size)
    input_string = generate_string(size)

    start_time = time.time()
    huffman.encode(input_string)
    huffman_times.append(time.time() - start_time)

    start_time = time.time()
    lzw.encode(input_string)
    lzw_times.append(time.time() - start_time)

    start_time = time.time()
    lz77.code_to_bytes(lz77.encode(input_string))
    lz77_times.append(time.time() - start_time)

plt.plot(input_sizes, huffman_times, label='Huffman')
plt.plot(input_sizes, lzw_times, label='LZW')
plt.plot(input_sizes, lz77_times, label='LZ77')
plt.xscale('log')
plt.xlabel('Input size')
plt.ylabel('Execution time (s)')
plt.legend()
plt.show()
