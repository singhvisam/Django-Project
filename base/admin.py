from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse

def request(request):
    render('base/home.html')
