from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib import messages

# Create your views here.

def todolist_display(response, id):
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
            else:
                messages.error(response,"title can't be empty")
                print("invalid")
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
