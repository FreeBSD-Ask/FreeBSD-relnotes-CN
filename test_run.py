from fix_md060_final import rebuild_table, find_tables_in_file, process_file
import os

# 测试
test_path = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\test_table.md'
with open(test_path, 'r', encoding='utf-8') as f:
    lines = [l.rstrip('\r\n') for l in f.readlines()]

print("Original:")
for i, l in enumerate(lines):
    print(f"  [{i}] {l}")

tables, _ = find_tables_in_file(test_path)
for (start, end) in tables:
    new_rows = rebuild_table(lines[start], lines[start+1], lines[start+2:end])
    print("Rebuilt:")
    for r in new_rows:
        print(f"  {r}")
