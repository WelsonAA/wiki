from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random


def md2html(md):
    markdowner = Markdown()
    html = markdowner.convert(md)
    return html


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry_search(request, title):
    md_cont = util.get_entry(title)
    if md_cont is None:
        entries = util.list_entries()
        recommendations = []
        for ent in entries:
            if ent.lower().find(str(title).lower()) != -1:
                recommendations.append(ent)
        if len(recommendations) == 0:
            return render(request, "encyclopedia/error.html", {
                "title": title,
                "message": "does not exist"
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "recommendations": recommendations
            })
    else:
        return entry_found(request, title, md_cont)


def entry_found(request, title, md_cont):
    html_cont = md2html(md_cont)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_cont
    })


def search(request):
    if request.method == "GET":
        text = request.GET.get("q")
        return entry_search(request, text)


def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        md_cont = request.POST["content"]
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "title": str(title).lower(),
                "message": "already Exists"
            })
        else:
            util.save_entry(str(title), md_cont)
            html_cont = md2html(md_cont)
            return render(request, "encyclopedia/entry.html", {
                "title": str(title),
                "content": html_cont
            })
    else:
        return render(request, "encyclopedia/new.html")


def entry(request, title):
    md_cont = util.get_entry(title)
    if md_cont is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": "does not exist"
        })
    else:
        return entry_found(request, title, md_cont)


def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
        })


def save(request):
    if request.method == "POST":
        title = request.POST["title_edited"]
        content = request.POST["content_edited"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": md2html(content)
        })


def randomise(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "title": str(rand_entry),
        "content": md2html(util.get_entry(str(rand_entry))),
    })
