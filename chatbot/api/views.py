from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse

import openai
import os
import requests
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Please set it in the environment variable OPENAI_API_KEY.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}

class HomeView(APIView):
    def get(self, request):
        return render(request, 'index.html')


def get_completion(prompt, model): 
	print(prompt)

	now = datetime.now()
	current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
	nickname = '승진님'
	system_prompt = f"""
        친절하게 응대해주세요.
    """
	data = { 
		'model': model,
		'messages': [
            {'role': 'system', 'content': system_prompt},
            # *[
            #     {'role': 'system',  'content': '무엇을 도와드릴까요?'},
            #     {'role': 'user',  'content': '시청역 가고 싶어.'},
            # ],
            {'role': 'user', 'content': prompt}
        ],
		'max_tokens': 150, 
		# n=1,
		# stop=None, 
		'temperature':0.85, 
    }
	response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
	response_data = response.json()
	ai_message = response_data['choices'][0]['message']['content']
	print(ai_message)
	return ai_message 


def gpt_4(request): 
	if request.method == 'POST':     
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt, model='gpt-4')
		return JsonResponse({'response': response}) 
	return render(request, 'index.html')


def gpt_4o(request): 
	if request.method == 'POST':     
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt, model='gpt-4o')
		return JsonResponse({'response': response}) 
	return render(request, 'index.html')


def gpt_4o_mini(request): 
	if request.method == 'POST':     
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt, model='gpt-4o-mini')
		return JsonResponse({'response': response}) 
	return render(request, 'index.html')


def gpt_4_turbo(request): 
	if request.method == 'POST':     
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt, model='gpt-4-turbo')
		return JsonResponse({'response': response}) 
	return render(request, 'index.html')


def gpt_3_turbo(request): 
	if request.method == 'POST':     
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt, model='gpt-3.5-turbo')
		return JsonResponse({'response': response}) 
	return render(request, 'index.html')


def read_txt_files(request):
    if request.method == 'GET':
        file_path = os.path.join(settings.BASE_DIR, 'conversation')
        txt_files = [f for f in os.listdir(file_path) if f.endswith('.txt')]

        all_contents = []
        for file_name in txt_files:
            with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as f:
                # 파일의 모든 줄을 읽고, 각 줄에서 줄바꿈 문자를 제거
                contents = [line.strip() for line in f]
                all_contents.append(contents)

        return JsonResponse({'response': all_contents}, safe=False)
    return render(request, 'index.html')
