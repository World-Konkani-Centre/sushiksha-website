import requests

url = "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism"

payload = '''{\r\n    \"text\": \"This is a test with a minimum of 40 characters to check plagiarism for.\",\r\n    \"language\": \"en\",\r\n    \"includeCitations\": false,\r\n    \"scrapeSources\": false\r\n}'''
headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com",
    'x-rapidapi-key': "db0042e89cmsh10eff3cd85c5355p1b2402jsne5885dd50ceb"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
