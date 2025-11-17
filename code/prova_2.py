from collections import Counter

from collections import Counter

def top_char_sequences(text, length=5, top_k=20):
    seqs = [text[i:i+length] for i in range(len(text)-length+1)]
    counter = Counter(seqs)
    return counter.most_common(top_k)

def repeated_substrings_by_freq_and_length(s):
    # Create suffix array
    suffixes = sorted([s[i:] for i in range(len(s))])

    # LCP function
    def lcp(a, b):
        i = 0
        while i < len(a) and i < len(b) and a[i] == b[i]:
            i += 1
        return a[:i]

    substrings = []

    # Extract repeated substrings (LCP of adjacent suffixes)
    for i in range(len(suffixes) - 1):
        common = lcp(suffixes[i], suffixes[i + 1])
        if len(common) > 1:   # Consider only substrings longer than 1 char
            substrings.append(common)

    # Count occurrences in the full text
    counts = {sub: s.count(sub) for sub in substrings}

    # Sort:
    # 1️⃣ prima per numero di occorrenze (desc)
    # 2️⃣ poi per lunghezza della sottostringa (desc)
    sorted_substrings = sorted(
        counts.items(),
        key=lambda x: (x[1], len(x[0])),
        reverse=True
    )

    return sorted_substrings

def top_ngrams(text, n=3, top_k=20):
    words = text.split()
    ngrams = [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]
    counter = Counter(ngrams)
    return counter.most_common(top_k)

with open ("../corpus_tesi/siciliano/output.txt", "r", encoding="utf-8") as f:
    testo = f.read()

results = top_ngrams(testo)
print(results)
#for sub, freq in results[:20]:
#    print(f"{repr(sub)} → {freq} occorrenze, {len(sub)} caratteri")
