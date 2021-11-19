
from django.shortcuts import render
from .db import *
from .functions import *

def home(req):

    try:
        word = req.GET['word']
        if word:
            word = word.lower()
            jobs = get_jobs(word)
            amount = len(jobs)
            db[word] = jobs
            Word = word.capitalize()
            return render(req, "result.html", {'jobs': jobs, 'word': Word, 'amount': amount})
            fromdB = db.get(word)
            if fromdB:
                jobs = fromdB
                amount = len(jobs)
                Word = word.capitalize()
                return render(req, "result.html", {'jobs' : jobs, 'word' : Word, 'amount' : amount})
            else:
                jobs = get_jobs(word)
                amount = len(jobs)
                db[word] = jobs
                Word = word.capitalize()
                return render(req, "result.html", {'jobs' : jobs, 'word' : Word, 'amount' : amount})

    except:
        pass

    return render(req, "home.html", {'keywords': keywords})
