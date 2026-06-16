import re

with open(r'C:\Users\ykla\AppData\Local\Temp\relnotes_15_1.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for any mention of "Ports" near heading tags
for m in re.finditer(r'<h[1-6][^>]*>.*?(?:[Pp]ort).*?</h[1-6]>', content, re.DOTALL):
    print(f'Found at {m.start()}: {m.group()[:200]}')

print()
# Search for the section after "Man Pages"
man_pages_idx = content.find('Man Pages')
if man_pages_idx != -1:
    print(f'"Man Pages" found at index {man_pages_idx}')
    # Print the next 5000 chars after "Man Pages"
    print(content[man_pages_idx:man_pages_idx+5000])
