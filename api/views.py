from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os,sys
from django.core.files.storage import default_storage
from django.contrib.contenttypes.models import ContentType
import requests
from pydub import AudioSegment
import json
import soundfile as sf

from .method.get_meeting_content import get_meeting_content
from .method.finding_planning_date import finding_planning_date
from .method.get_sentiment_content import get_sentiment_content
from .method.Summarizer import FrequencySummarizer 



class UploadFile(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        #print(ContentType.objects.get_for_model(self))
        print(request.content_type);
        if 'file' not in request.data:
            raise ParseError("Empty content")

        try:
            f = request.data['file']
            file_name = f.name
            #print(file_name)
            if file_name.endswith(".wav"):
                file_name = default_storage.save(f.name, f)
                return Response({"status":"success","filename":file_name},status=status.HTTP_201_CREATED)

            else :
                return Response({"status":"bad request"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"status":"bad requests"},status=status.HTTP_400_BAD_REQUEST)
        #mymodel.my_file_field.save(f.name, f, save=True)


class analysis(APIView):
    def get(self, request, format=None):
        
        text_arr = analyticText();
                    
        return Response(text_arr,status=status.HTTP_201_CREATED)

class summary(APIView):
    def post(self, request, format=None):
        n = request.data['n']
        print(n)
        text_arr = analyticText();
        content = get_meeting_content(text_arr)

        freq = FrequencySummarizer(content)
        result = freq.summarize(int(n))
                    
        return Response(result,status=status.HTTP_201_CREATED)

class Planning(APIView):
    def get(self, request, format=None):
        
        text_arr = analyticText();
        contents = get_meeting_content(text_arr)

        return_data = []

        for content in contents:
            content_tmp = finding_planning_date(content)
            if(content_tmp["day_of_week"] != "null"):
                return_data.append(content_tmp)
            
                    
        return Response(return_data,status=status.HTTP_201_CREATED)

class Sentiment(APIView):
    def get(self,request,format=None):
        text_arr = analyticText();
        contents = get_meeting_content(text_arr)
        #print(contents)
        sentiment_content = get_sentiment_content(contents)

        print(dict(sentiment_content))


        return Response(dict(sentiment_content),status=status.HTTP_201_CREATED)

class total(APIView):
    def post(self, request, format=None):
        n = request.data['n']
        n = int(n)
        text_arr = analyticText();
        contents = get_meeting_content(text_arr)

        sentiment_content = get_sentiment_content(contents) #sentiment
        sentiment_content = dict(sentiment_content);

        plan = [] #planning
        for content in contents:
            content_tmp = finding_planning_date(content)
            if(content_tmp["day_of_week"] != "null"):
                plan.append(content_tmp)

        freq = FrequencySummarizer(contents) #summary
        summary = freq.summarize(n)

        return Response({'analytic':text_arr,'sentiment':sentiment_content,'planning':plan,'summary':summary},status=status.HTTP_201_CREATED)

def analyticText():
    folder = 'media'
    text_arr = list()
    text_with_space = ""
    start = 0;
    end = 0
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".wav"):
                filepath = dirpath + '/' + filename
                f = sf.SoundFile(filepath)
                    
                res = SpeechToText(filepath);
                json_data = json.loads(res.text)
                if(json_data['status'] == 'success'):
                    text_with_space = json_data['result']
                    text = json_data['result'].replace(' ','');
                    end = end  + (len(f) / f.samplerate)
                    info = { "start": start, "end": end, "string_data": text, "string_data_with_space" :text_with_space, "data":{ "note":text }  }
                    start = start + (len(f) / f.samplerate)   
                    text_arr.append(info)

    return text_arr

                        

def SpeechToText(filename):
        url = "https://api.aiforthai.in.th/partii-webapi"
 
        files = {'wavfile': open(filename, 'rb')}
 
        headers = {
            'Apikey': "1tsglCACL1dgAqaP30UVhB4e3Up1txxe",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
        }
 
        param = {"format":"json"}
 
        response = requests.request("POST", url, headers=headers, files=files, data=param)

        return response

