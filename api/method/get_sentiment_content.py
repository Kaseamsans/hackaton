def get_sentiment_content(meeting_content):

  import requests
  from collections import defaultdict
  url = "https://api.aiforthai.in.th/ssense"
  headers = {'Apikey': "jIu8xU0JhX9ZYO94VzvCCLooNQrjMPHH"}

  sentiment_content = defaultdict(list)

  for sentence in meeting_content:
    data = {'text':sentence}
    response = requests.post(url, data=data, headers=headers)

    intend = []
    for i in response.json()['intention'].items():
      if float(i[1]) >=60:
        intend.append(i[0])

    for i in intend:
      sentiment_content[i].append(sentence)

  return  sentiment_content
