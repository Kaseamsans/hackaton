def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def finding_planning_date(text_sentence):

  import requests
  from datetime import date , timedelta
  import calendar

  url ='https://api.aiforthai.in.th/lextoplus'
  headers = {'Apikey':"jIu8xU0JhX9ZYO94VzvCCLooNQrjMPHH"}

  text_sentence = text_sentence.replace(' ','')
  params = {'text':text_sentence,'norm':'1'}

  response = requests.get(url, params=params, headers=headers)

  text_array = response.json()['tokens']

  for i in text_array:
    idx = text_array.index(i)
    text_array[idx] = i.replace('วัน','')


  list_datetime_previous = ['เมื่อวาน','เมื่อวานซืน','ที่ผ่านมา','ที่แล้ว']
  list_datetime_next = ['พรุ่งนี้','มะรืนนี้','มะเรือง','นี้','หน้า']
  list_datetime_deadline = ['อีก','ภายใน','ในอีก','ใน']

  day_of_week = {'Monday':'วันจันทร์','Tuesday':'วันอังคาร','Wednesday':'วันพุธ','Thursday':'วันพฤหัสบดี','Friday':'วันศุกร์','Saturday':'วันเสาร์','Sunday':'วันอาทิตย์'}
  num_day_of_week = {'จันทร์':1,'อังคาร':2,'พุธ':3,'พฤหัสบดี':4,'พฤหัส':4,'ศุกร์':5,'เสาร์':6,'อาทิตย์':7}
  num_day_of_unit = {'สัปดาห์':7,'อาทิตย์':7,'เดือน':30,'ปี':365}

  today = date.today()
  num_current_day = num_day_of_week[day_of_week[calendar.day_name[today.weekday()]].replace('วัน','')]

  previous = False
  after = False
  words = []

  word_previous = intersection(text_array, list_datetime_previous)
  if word_previous:
    previous = True
    words = word_previous

  word_next = intersection(text_array, list_datetime_next)
  if word_next:
    after = True
    words = word_next

  word_deadline = intersection(text_array, list_datetime_deadline)

  try:
    diff_day = 0
    if (not previous) & (not after) & (len(word_deadline) > 0 ):
      idx = text_array.index(word_deadline[0])
      after_word = text_array[idx+1]
      if int(after_word) in range(0,1000):
        diff_day = int(after_word)
      words = word_deadline
  except:
    return { "day_of_week": 'null', "date": 'null', "sentences": 'null'}

  try:
    target_day_of_week = 0
    if previous | after:
      target_day = intersection(text_array, num_day_of_week.keys())
      target_day_of_week = int(num_day_of_week[target_day[0]])
  except:
    return { "day_of_week": 'null', "date": 'null', "sentences": 'null'}

  if len(words) ==0:
    return { "day_of_week": 'null', "date": 'null', "sentences": 'null'}

  word = words[0]

  if len(word) > 0 :
    idx = text_array.index(word)
    before_word = text_array[idx-1]
  else:
    before_word = []

  before_or_after = 0
  # find day of week
  if previous:
    before_or_after = -1
  if after:
    before_or_after = 1

  num_date = 0
  cal_only_date = False

  if before_word in num_day_of_unit.keys():
    num_date = num_day_of_unit[before_word]

  if before_word in num_day_of_week.keys() :
    num_date = num_day_of_week[before_word]
    cal_only_date = True
    if previous:
      before_or_after = -1


  ''' Calculate diff day from current day to get the target date '''
  if cal_only_date:
    target_diff_day = 7- num_current_day+ target_day_of_week
    if before_or_after <0:
      target_diff_day = ((7+num_current_day) - target_day_of_week) * before_or_after
      if num_current_day > target_day_of_week:
        target_diff_day = (num_current_day - target_day_of_week) * before_or_after

  else:
    target_diff_day = (target_day_of_week - num_current_day) + (num_date *  before_or_after)
    if diff_day > 0:
      target_diff_day = diff_day+1



  new_date = date.today()+ timedelta(days=target_diff_day)
  new_day = day_of_week[calendar.day_name[new_date.weekday()]]
  new_date = new_date.strftime('%Y-%m-%d')

  results =  { "day_of_week": new_day, "date": new_date, "sentences": text_sentence}
  return results
