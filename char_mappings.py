
chars = {
'a': ['0110',
      '1001',
      '1111',
      '1001',
      '1001'],
'b': ['1110',
      '1001',
      '1111',
      '1001',
      '1110'],
'c': ['0111',
      '1000',
      '1000',
      '1000',
      '0111'],
'd': ['1110',
      '1001',
      '1001',
      '1001',
      '1110'],
'e': ['1111',
      '1000',
      '1111',
      '1000',
      '1111'],
'f': ['1111',
      '1000',
      '1111',
      '1000',
      '1000'],
'g': ['0111',
      '1000',
      '1011',
      '1001',
      '0110'],
'h': ['1001',
      '1001',
      '1111',
      '1001',
      '1001'],
'i': ['111',
      '010',
      '010',
      '010',
      '111'],
'j': ['1111',
      '0010',
      '0010',
      '0010',
      '1110'],
'k': ['1001',
      '1010',
      '1100',
      '1010',
      '1001'],
'l': ['100',
      '100',
      '100',
      '100',
      '111'],
'm': ['1001',
      '1111',
      '1001',
      '1001',
      '1001'],
'n': ['1001',
      '1101',
      '1111',
      '1011',
      '1001'],
'o': ['0110',
      '1001',
      '1001',
      '1001',
      '0110'],
'p': ['1110',
      '1001',
      '1110',
      '1000',
      '1000'],
'q': ['0110',
      '1001',
      '1001',
      '1011',
      '0111'],
'r': ['1110',
      '1001',
      '1110',
      '1001',
      '1001'],
's': ['0111',
      '1000',
      '0111',
      '0001',
      '1110'],
't': ['11111',
      '00100',
      '00100',
      '00100',
      '00100'],
'u': ['1001',
      '1001',
      '1001',
      '1001',
      '0110'],
'v': ['101',
      '101',
      '101',
      '101',
      '010'],
'w': ['10001',
      '10001',
      '10101',
      '11011',
      '10001'],
'x': ['1001',
      '0110',
      '0110',
      '0110',
      '1001'],
'y': ['10001',
      '01010',
      '00100',
      '00100',
      '00100'],
'z': ['1111',
      '0011',
      '0110',
      '1100',
      '1111'],
'.': ['00',
      '00',
      '00',
      '00',
      '11'],
':': ['0',
      '1',
      '0',
      '1',
      '0'],
'?': ['011110',
      '100011',
      '001110',
      '00100',
      '00100'],
'\'': ['11',
      '11',
      '00',
      '00',
      '00'],
' ': ['0',
      '0',
      '0',
      '0',
      '0'],
'0': ['010',
      '101',
      '101',
      '101',
      '010'],
'1': ['01',
      '11',
      '01',
      '01',
      '01'],
'2': ['011',
      '101',
      '010',
      '100',
      '111'],
'3': ['111',
      '001',
      '111',
      '001',
      '111'],
'4': ['011',
      '101',
      '111',
      '001',
      '001'],
'5': ['111',
      '100',
      '111',
      '001',
      '111'],
'6': ['011',
      '100',
      '111',
      '101',
      '010'],
'7': ['111',
      '001',
      '010',
      '100',
      '100'],
'8': ['111',
      '101',
      '111',
      '101',
      '111'],
'9': ['111',
      '101',
      '111',
      '001',
      '111']
}

def get_mapping(string):
  global chars
  string = string.lower() 

  mapping = ['','','','','']

  for char in string:
    if char in chars:
      char_mapping = chars[char]
    else:
      char_mapping = ['0','0','0','0','0']
    mapping = [
      mapping[0] + char_mapping[0] + '0',
      mapping[1] + char_mapping[1] + '0',
      mapping[2] + char_mapping[2] + '0',
      mapping[3] + char_mapping[3] + '0',
      mapping[4] + char_mapping[4] + '0'
    ]

  return mapping
