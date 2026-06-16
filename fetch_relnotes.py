import os

fpath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\15.1.md'

with open(fpath, 'rb') as f:
    raw = f.read()

# Check BOM
if raw[:3] == b'\xef\xbb\xbf':
    print('WARNING: File has UTF-8 BOM')
else:
    print('OK: No UTF-8 BOM')

# Check line endings
crlf_count = raw.count(b'\r\n')
lf_count = raw.count(b'\n') - crlf_count
cr_only = raw.count(b'\r') - crlf_count

print(f'CRLF count: {crlf_count}')
print(f'LF count: {lf_count}')
print(f'CR only count: {cr_only}')

if crlf_count > 0:
    print('WARNING: File has CRLF line endings')
    # Convert to LF
    with open(fpath, 'wb') as f:
        f.write(raw.replace(b'\r\n', b'\n'))
    print('Converted to LF line endings')
elif lf_count > 0:
    print('OK: File has LF line endings')
else:
    print('WARNING: No line endings found')

# Check last few lines
with open(fpath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'\nTotal lines: {len(lines)}')
print('\nLast 5 lines:')
for line in lines[-5:]:
    print(repr(line))
