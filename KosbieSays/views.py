from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect

import random, string, bisect

class HomePage(View):
    nexts = None
    start_vals = None
    start_words = None

    def get(self, request):
        self.get_data_cached()
        sentence = self.get_sentence()
        return render(request,  "index.html", {"text": sentence})

    def get_data_cached(self):
        if HomePage.nexts and HomePage.start_vals and HomePage.start_words: return
        f = open("KosbieSays/processed_data_clean.txt", "r")
        data = f.read()
        f.close()
        data = eval(data)
        HomePage.nexts = data["nexts"]
        HomePage.start_vals = data["start_vals"]
        HomePage.start_words = data["start_words"]

    def get_sentence(self):
        result = ""
        gram = self.get_start()
        first_word = gram.split()[1]
        first_word = first_word[0].upper() + first_word[1:]
        result = first_word
        next_word = ""
        while True:
            try:
                w1, w2 = gram.split()
            except:
                print "sasdddd",  gram
                break
            w3 = self.get_next_word(gram)
            if w3 == "**s**":
                result += "."
                break
            result += " " + w3
            gram = "%s %s" % (w2, w3)
        return result

    def get_start(self):
        x = random.random()
        idx = bisect.bisect(HomePage.start_vals, x)
        result =  HomePage.start_words[idx]
        if result == "**s** **s**" or result == "**s** ":
            return self.get_start()
        return result

    def get_next_word(self, gram):
        if gram not in HomePage.nexts:
            print "----", gram
            return "**s**"
        (vals, words) = HomePage.nexts[gram]
        x = random.random()
        idx = bisect.bisect(vals, x)
        return words[idx]
