import random
import string

with open("data.in", "w") as f:
    out = ""
    words = []
    for i in range(500):
        words.append(''.join(random.choices(string.ascii_lowercase, k = random.choice([2, 3, 4, 5, 6, 7]))))
    for i in range(50000):
        out = out + random.choice(words) + " "
    out = out.strip()
    f.write(out)