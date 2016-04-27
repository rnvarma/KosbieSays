import string
import bisect
import random

data = open("kosbiesays.txt", "r")
text = data.read()
data.close()

starts = {}
total_starts = 0
start_list = []
nexts = {}
punctuations = {}

punc = string.punctuation 

# - break up everything into sentences
# - gram is 2 words
# - check if first word has punctuation:
#       put into punctuation dictionary recording num of them
# - strip both words of punctuation
# - first grap is "S word", last gram is "word S"
#       strip period/punctuation from last gram
# - put first gram into the starts dictionary
# - map gram to list of next word: "X Y Z" --> {"X + Y": {"Z": 1}}
# - next gram = "Y Z"

stuff = " ".join(text.split())
sentences = stuff.split(".")

def strip_punc(w):
    if w == "**s**": return w
    result = ""
    for l in w:
        if l not in punc: result += l
    return result

for sent in sentences:
    words = sent.split()
    words = filter(lambda s: s, words)
    words = ["**s**"] + words + ["**s**"]
    words = map(lambda s: s.lower(), words)
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        gram = "%s %s" % (strip_punc(w1), strip_punc(w2))
        if w1 == "**s**":
            starts[gram] = starts.get(gram, 0) + 1
            total_starts += 1
        if w1 != "**s**" and w1[-1] in punc:
            p = w1[-1]
            w1 = w1[:-1]
            if w1 not in punctuations: punctuations[w1] = {}
            if p not in punctuations[w1]: punctuations[w1][p] = 0
            punctuations[w1][p] += 1
        if w2 == "**s**": break
        w3 = strip_punc(words[i + 2])
        if gram not in nexts: nexts[gram] = {}
        if w3 not in nexts[gram]: nexts[gram][w3] = 0
        nexts[gram][w3] += 1

for gram in nexts:
    next_words = nexts[gram]
    total = sum(next_words.values())
    total_val = 0
    cdf = []
    for n in next_words:
        val = 1.0 * next_words[n] / total
        total_val += val
        cdf.append((total_val, n))
    cdf.sort()
    vals, words = zip(*cdf)
    nexts[gram] = (vals, words)

total_start = 0
for start in starts:
    val = 1.0 * starts[start] / total_starts
    total_start += val
    start_list.append((total_start, start))
    starts[start] = val

start_list.sort()
start_vals, start_words = zip(*start_list)

f = open("processed_data.txt", "w")
data = {"nexts": nexts, "start_vals": start_vals, "start_words": start_words}
f.write(repr(data))
f.close()








