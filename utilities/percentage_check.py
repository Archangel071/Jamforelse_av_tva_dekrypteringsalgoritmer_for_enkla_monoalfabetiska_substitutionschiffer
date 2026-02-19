import string

with open('../utilities/klartext_input.txt', encoding='utf-8') as f:
    txt = f.read().lower()

# Clean the text
txt = txt.replace('\n', ' ')
txt = txt.replace('-', ' ')
txt = txt.replace('—', ' ')
for char in txt:
    if not char.isalpha() and char != ' ':
        txt = txt.replace(char, '')

txt_stripped = txt.replace(' ', '')

    # Count amount of ocurrances & sort them in decending order
counts = {}
for l in string.ascii_lowercase:
    counts.update({l:txt_stripped.count(l)})
counts_sorted = dict(sorted(counts.items(), reverse=True, key=lambda x: x[1]))

    # Calculate the frequencies
freqs = {}
freqs.update(counts_sorted.copy())
for k, v in counts.items():
    freqs.update({k : (v / len(txt_stripped))})
print(freqs)

s = input()
solved = [x for x in s]

ans = 0
for l in solved:
    if l in freqs.keys():
        ans += freqs[l]

print(ans)