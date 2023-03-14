# this code is written in python 3, by yours truly :)
data = "Something"

# declare some variables
bytes = ""
h0 = 0x67452301
h1 = 0xEFCDAB89
h2 = 0x98BADCFE
h3 = 0x10325476
h4 = 0xC3D2E1F0
a = h0
b = h1
c = h2
d = h3
e = h4

# for every character in data, get the ascii code of said character
# then convert the ascii code to binary
# pad it with zeroes until it is 8 characters long
for char in data:
  bytes += "0"*(8-len(bin(ord(char))[2:])) + bin(ord(char))[2:]

# append a one
bits = bytes + "1"

# append zeroes until the length is 512 mod 448
while len(bits) % 512 != 448:
  bits+="0"

# take the length of the combined 8 original bytes
# then pad with zeroes until it is 64 long
bits += "0" *(64 - len(bin(len(bytes))[2:])) + bin(len(bytes))[2:]

# splits a string into chunks
# l = the string, n = bits in every chunk
def chunkify(l, n):
  return [l[i:i+n] for i in range(0, len(l), n)]

#left rotate function
def rol(n, b):
  return ((n << b) | (n >> (32 - b))) & 0xffffffff

#VVV the magic VVV
for chunk in chunkify(bits, 512):
  #split 'chunk' even more into 32 bit strings
  words = chunkify(chunk, 32)
  w = []
  # append the 16 strings in words to w
  for n in range(0, 16):
      w.append(int(words[n], 2))

  #perform bitwise operations to generate another 64 strings
  for i in range(16, 80):
      w.append(rol((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1))

  #perform a lot of bitwise operations to maipulate variables
  for i in range(0, 80):
      if i < 20:
          bAc = b & c
          nbAd = (~b) & d
          f = bAc | nbAd
          k = 0x5A827999
      elif i < 40:
          bXc = b ^ c
          f = bXc ^ d
          k = 0x6ED9EBA1
      elif i < 60:
          bAc = b & c
          bAd = b & d
          cAd = c & d
          f = bAc | bAd | cAd
          k = 0x8F1BBCDC
      else:
          f = b ^ c ^ d
          k = 0xCA62C1D6

      temp = rol(a, 5) + f + e + k + w[i] & 0xffffffff
      e = d
      d = c
      c = rol(b, 30)
      b = a
      a = temp

  h0 = h0 + a & 0xffffffff
  h1 = h1 + b & 0xffffffff
  h2 = h2 + c & 0xffffffff
  h3 = h3 + d & 0xffffffff
  h4 = h4 + e & 0xffffffff

#and just join them all together
output = '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)
print(output)