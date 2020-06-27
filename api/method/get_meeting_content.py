def get_meeting_content(contents):
  meeting_content = []
  for sentence in contents:
      meeting_content.append(sentence['string_data'])

  return meeting_content