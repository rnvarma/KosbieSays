import string, bisect, random



def get_start():
    x = random.random()
    idx = bisect.bisect(start_vals, x)
    result =  start_words[idx]
    if result == "**s** **s**":
        return get_start()
    return result

def get_next_word(gram):
    if gram not in nexts:
        print "----", gram
        return "**s**"
    (vals, words) = nexts[gram]
    x = random.random()
    idx = bisect.bisect(vals, x)
    return words[idx]

result = ""
gram = get_start()
first_word = gram.split()[1]
first_word = first_word[0].upper() + first_word[1:]
result = first_word
next_word = ""
while  True:
    try:
        w1, w2 = gram.split()
    except:
        print "sasdddd",  gram
        break
    w3 = get_next_word(gram)
    if w3 == "**s**":
        result += "."
        break
    result += " " + w3
    gram = "%s %s" % (w2, w3)

print result
