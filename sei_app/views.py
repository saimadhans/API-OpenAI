from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from bs4 import BeautifulSoup
import requests
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

@ensure_csrf_cookie
def home(request):
    return render(request, "home.html")

def scrape_and_compare(request):
    if request.method == "POST":
        url1 = request.POST.get("url")
        url2 = request.POST.get("policy_url")

        content1 = scrape_webpage(url1)
        content2 = scrape_webpage(url2)

        findings = compare_content(content1, content2)

        return JsonResponse({"findings": findings})
    else:
        return render(request, "sei_app/home.html")

def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')
        webpage_content = soup.get_text()
        print("Webpage Content:")
        print(webpage_content)
        return webpage_content
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def compare_content(content1, content2):
    # print(content1)
    # print(content2)
    try:
        prompt = f"Check if the following content complies with the policy:\n\n{content1}\n\nPolicy:\n{content2}. Explain why."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1000
        )
        print("OpenAI Response:")
        print(response)
        findings = response["choices"][0]["text"]
    except Exception as e:
        findings = f"Error: {e}"
    return findings
