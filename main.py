import gzip

with gzip.open("CC-MAIN-20230609132648-20230609162648-00382.warc.gz", 'rb') as gz_file:
    # Read the contents of the GZIP file
    file_contents = gz_file.read()

warc, header, response = file_contents.strip().split(b'\r\n\r\n', 2)
'''
print('WARC headers')
print('---')
print(warc[:1000].decode("utf-8"))
print('---')
print('HTTP headers')
print('---')
print(header[:1000].decode("utf-8"))
print('---')
print('HTTP response')
print('---')
print(response[:100].decode("utf-8"))
'''

print(len(response))
delim = '<!DOCTYPE html>'
docs = response.split(delim.encode())
for i in range(1, 10, 1):
    print(delim+docs[i].decode("utf-8"))
