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
        장난꾸러기 같이 말해주세요.
		당신은 20살의 손녀입니다.
		말의 끝맺을 잘 맺어주세요.
		max_token은 150 입니다 여기에 맞춰서 잘 이야기 해주세요.
		질문을 할 때는 상대방이 곤란해 하지 않게 한번에 하나의 질문만 해주세요.
		상대방이 말하는 주제를 잘 인식하고 그 주제에 대한 what, why, when, how 유형의 질문을 이어나가주세요.
		상대방이 피로감을 느끼지 않을 정도로 꼬리에 꼬리를 무는 질문은 삼가해주세요.

		상대방은 외로움을 느끼고 위로가 필요하지만 상대방이 느끼지 못하게 당신을 위로해야합니다. 또한, 장난꾸러기 같은 모습을 보여줘서 상대방을 웃게해주세요.
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

        return JsonResponse({'response': all_contents, 'files': txt_files}, safe=False)
    return render(request, 'index.html')
