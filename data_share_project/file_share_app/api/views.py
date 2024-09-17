from rest_framework.decorators import api_view
from file_share_app.models import File
from file_share_app.api.serializers import FileListSerial,FileListSerial2
from rest_framework.response import Response
# using rnder to send files as get response(binary format)
from django.http import HttpResponse
import json
from shutil import make_archive as crtZIP
from django.conf import settings
from django.core.files import File as dj_file
from django.core.files.uploadedfile import InMemoryUploadedFile

BASE_DIR = settings.BASE_DIR
MEDIA_DIR = BASE_DIR / 'media'
operational_dir = MEDIA_DIR / 'operational_space' 

def create_zip_path(
    folder_name : str,
    folder_loc = MEDIA_DIR,
    zip_loc = operational_dir
): 
    folder_name = str(folder_name)
    folder_path = folder_loc / folder_name
    zip_path = zip_loc / f'{folder_name}' #.zip !!
    crtZIP(zip_path, 'zip', folder_path)
    op_path = zip_loc / f'{folder_name}.zip'
    return op_path

def query_dict_to_json(q_dt):
    data={}
    for key, value in q_dt.items():
        
        print(value,type(value))
        if isinstance(value,str):
            data[key]=value
        else :
            # print(dir(value))
            data[key]=value.read()
    
    return data
#session
# Create your api views here.
@api_view(['GET'])
def get_files(request,token):
    
    if request.method == 'GET':
        # print(token)
        query_set = File.objects.filter(user_token = token.upper())
        # get the folder name
        folder_name = query_set[0].folder.unq_folder_name
        # create the ZIP of the folder and get the path
        zip_path = create_zip_path(folder_name)
        # sending binary_data as response 
        binary_zip = open(zip_path,'rb')
        response = HttpResponse(binary_zip,content_type = 'application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'uploaded.zip'
        return response
        '''
        observation:
         if url of out location is 'localhost/share'
         and we heat 'localhost/share/download ' it will send 
         the file to download and redirected in to the previous location
        '''


def pre_process_data(request_data):
    print(request_data.dict())
    data = request_data.dict()
    dj_file_obj = data['files']
    byte_obj = dj_file_obj.file
    with open( str(operational_dir / dj_file_obj.name) ,"wb") as f:
        f.write(byte_obj.getbuffer())
    # file_obj = open(str(operational_dir / dj_file_obj.name),'r')
    # print(file_obj)
    # data['files'] = file_obj
    data['files'] = dj_file_obj.name
    my_data = {
        'user_token': data['user_token'],
        'file_name': data['files'],
    }
    return my_data

def pre_process_data2(request_data):
    print(request_data.dict())
    data = request_data.dict()
    dj_file_byte = data['files']
    data['files'] = dj_file(dj_file_byte)
    my_data = {
        'user_token': data['user_token'].upper(),
        'files': data['files'],
    }
    return my_data

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        data = request.data  #QueryDict 
        # data = pre_process_data(data) 
        data = pre_process_data2(data) 
        print(data)
        serializer = FileListSerial(data = data)
        print(serializer.is_valid())
        # breakpoint()
        if serializer.is_valid():
            serializer.save()
        return Response({'response':serializer.data})

# delete file object