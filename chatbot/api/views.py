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

cost_per_model = {
    'gpt-4o-mini': {'input_token': 0.00000015, 'output_token': 0.00000060},
    'gpt-4o': {'input_token': 0.0000025, 'output_token': 0.00001}
}

def get_exchange_rate():
    """실시간 환율 조회 (USD → KRW)"""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data["rates"]["KRW"]  # 1 USD = ? KRW
    except Exception as e:
        print(f"⚠️ 환율 정보를 가져오는 데 실패했습니다: {e}")
        return 1350  # 기본값 (고정 환율)

def calculate_cost(input_tokens, output_tokens, model):
    """입력/출력 토큰 수를 기반으로 비용 계산 (USD → KRW 변환)"""
    print(input_tokens, output_tokens)
    usd_cost = (
        (input_tokens * cost_per_model[model]['input_token'])
    + (output_tokens * cost_per_model[model]['output_token'])
    )
    exchange_rate = 1460  # 추후 변수 화 해서 redis를 사용하여 환율 api에서 하루마다 가져오게 수정 ("https://api.exchangerate-api.com/v4/latest/USD")
    krw_cost = usd_cost * exchange_rate
    return format(usd_cost, ".8f"), format(krw_cost, ".4f")  # USD 소수점 8자리, KRW 소수점 2자리

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}

class HomeView(APIView):
    def get(self, request):
        return render(request, 'index.html')

conversation_history = []

def get_completion(prompt, model):
    global conversation_history
    print(conversation_history)

    print(f"User: {prompt}")  # 사용자 입력 출력

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
                장난꾸러기 같이 말해주세요.
    """

    conversation_history.append({'role': 'user', 'content': prompt})

    # 모델이 너무 많은 대화를 처리하지 않도록 최근 10개만 유지
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    data = {
        'model': model,
        'messages': [{'role': 'system', 'content': system_prompt}] + conversation_history,
        'max_tokens': 300,
        # n=1,
        # stop=None,
        'temperature':0.85,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response_data = response.json()

    ai_message = response_data['choices'][0]['message']['content']
    input_tokens = response_data['usage']['prompt_tokens']
    output_tokens = response_data['usage']['completion_tokens']
    total_cost = calculate_cost(input_tokens, output_tokens, model)
    print(total_cost)
    print(f"AI: {ai_message}")

    conversation_history.append({'role': 'assistant', 'content': ai_message})
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
