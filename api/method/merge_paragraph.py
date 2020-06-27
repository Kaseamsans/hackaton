def merge_paragraph(meeting_contents):
    
  paragraph_meeting_content = ''
  for mssg in meeting_contents:
    paragraph_meeting_content = paragraph_meeting_content+' '+mssg

  return paragraph_meeting_content.strip()