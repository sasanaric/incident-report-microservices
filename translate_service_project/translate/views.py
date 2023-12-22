from django.shortcuts import render
from django.http import JsonResponse
from deep_translator import GoogleTranslator
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from langdetect import detect

# Create your views here.

class HelloAPI(generics.CreateAPIView):
    def get(self,request):
        return Response({"Translate service says hello."},status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        text = request.data.get('text');
        return Response({"your text is "+text},status=status.HTTP_200_OK)
    
def translate_text(request):
    # Your original text
    original_text = "Hello, how are you?"

    # Translate the text to a specific language (e.g., Spanish)
    translated_text = GoogleTranslator(target='sr').translate(original_text)

    # Return the translation as JSON
    response_data = {
        'original_text': original_text,
        'translated_text': translated_text,
    }

    return JsonResponse(response_data)

class TranslateEN_SR(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        original_text = request.data.get('text')
        translated_text = GoogleTranslator(source='en', target='sr').translate(original_text)

        return HttpResponse(translated_text, content_type='text/plain')

class TranslateSR_EN(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        original_text = request.data.get('text')
        translated_text = GoogleTranslator(source='sr', target='en').translate(original_text)
        # translated_text = translated_result['text']

        return HttpResponse(translated_text, content_type='text/plain')
    
class TranslateDynamic(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        original_text = request.data.get('text')

        # Detect the source language
        source_language = detect(original_text)

        # Define the target language (you can customize this logic)
        target_language = 'sr' if source_language == 'en' else 'en'

        # Translate the text
        translated_text = GoogleTranslator(source=source_language, target=target_language).translate(original_text)

        return HttpResponse(translated_text, content_type='text/plain')

