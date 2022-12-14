from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib import messages
from practicingsq3lite import *

# Create your views here.

def todolist_display(response, id):
    if id == 25:
        tweet_type = "stackchain"
    elif id == 26:
        tweet_type = "stackchaintip"
    elif id == 28:
        tweet_type = "pbstack"
    else:
        tweet_type = "stackjoin"
    ls = ToDoList.objects.get(id=id)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c"+str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 0:
                ls.item_set.create(text=txt, complete=False)
                print(txt)
            else:
                messages.error(response,"title can't be empty")
                print("invalid")
            update_s3(tweet_type)
        elif response.POST.get("deleteItem"):
            print("pressed delete tweet button")
            print(f"this is the response: {response.POST.get('deleteItem')}")
            for item in ls.item_set.all():
                print(item.id)
                if int(response.POST.get("deleteItem")) == item.id:
                    print("item igual")
                    item.delete()
                else:
                    print("item nao igual")
            update_s3(tweet_type)
            return HttpResponseRedirect("/" + str(id))
        elif response.POST.get("printItem"):
            print("pressed print item button")
            for item in ls.item_set.all():
                if int(response.POST.get("printItem")) == item.id:
                    print(item)
            return HttpResponseRedirect("/" + str(id))
        elif response.POST.get("delete"):
            print(id)
            ToDoList.delete(ls)
            return HttpResponseRedirect("/")
    return render(response, "main/todolist_display.html", {"ls":ls})

def home(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            return HttpResponseRedirect("/")
    else:
        form = CreateNewList()

    queryset = ToDoList.objects.all() # list of objects
    context = {
        "object_list": queryset, "form": form
    }
    return render(response, "main/home.html", context)

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            return HttpResponseRedirect("/")
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})
