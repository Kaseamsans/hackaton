from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os,sys
from django.core.files.storage import default_storage
import requests
from pydub import AudioSegment
import json
import soundfile as sf



class UploadFile(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']

        file_name = default_storage.save(f.name, f)
        
        #mymodel.my_file_field.save(f.name, f, save=True)
        return Response({file_name},status=status.HTTP_201_CREATED)

class analysis(APIView):
    def get(self, request, format=None):
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
                        info = { "start": start, "end": end, "string_data": text, "string_data_with_space" :text_with_space  }
                        start = start + (len(f) / f.samplerate)   
                        text_arr.append(info)

                    
        return Response(text_arr,status=status.HTTP_201_CREATED)


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
 


# Create your views here.
