from django.shortcuts import render
from django.http import HttpResponse


def run_workflow(request):

    return HttpResponse("AI Workflow Started")


def trending_topics(request):

    return HttpResponse("Trending Topics")


def generate_caption(request):

    return HttpResponse("Caption Generated")


def generate_image(request):

    return HttpResponse("Image Generated")


def content_history(request):

    return HttpResponse("Content History")
