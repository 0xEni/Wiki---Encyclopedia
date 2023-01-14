from django import forms
from django.shortcuts import render
import markdown2
import os
from random import choice

from . import util

class NewTaskForm(forms.Form):
    titleEntry = forms.CharField(label="Title")
    contentsEntry = forms.CharField(label="Contents", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    html_content = convert_md_to_html(entry)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            'entry': "Requested Page was not found.",
            'title': "Page Does Not Exist"
        })
    else:

        return render(request, "encyclopedia/entry.html", {
            "entry": html_content,
            "title": entry.capitalize()
        })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            titleEntry = form.cleaned_data["titleEntry"]
            contentsEntry = form.cleaned_data["contentsEntry"]
            if util.get_entry(titleEntry) != None:
                return render(request, "encyclopedia/error.html", {
                    'entry': "Entry with the same title was already found.",
                    'title': "Entry Page Already Exists"
                })
            else:
                util.save_entry(titleEntry, contentsEntry)
                return entry(request, titleEntry)
        else:
            return render(request, " encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewTaskForm()
    })

def search(request):
        query = request.GET.get('q')
        if util.get_entry(query) != None:
            return entry(request, query)
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": util.search_entries(query)
        })


def edit(request, entry):
    data = {'titleEntry': entry, 'contentsEntry': util.get_entry(entry)}
    return render(request, "encyclopedia/edit.html", {
        "form": NewTaskForm(initial=data)
    })

def saved(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            titleEntry = form.cleaned_data["titleEntry"]
            contentsEntry = form.cleaned_data["contentsEntry"]
            util.save_entry(titleEntry, contentsEntry)
            return entry(request, titleEntry)
        else:
            return render(request, " encyclopedia/saved.html", {
                "form": form
            })

def random(request):
    allEntries = util.list_entries()
    rand_entry = choice(allEntries)
    return entry(request, rand_entry)

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdown2.markdown(content)
