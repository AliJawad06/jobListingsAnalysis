def append_jsonl_to_jsonl(src, dst):
    with open(dst, 'a', encoding='utf-8') as out, open(src, 'r', encoding='utf-8') as inp:
        out.writelines(line for line in inp if line.strip())