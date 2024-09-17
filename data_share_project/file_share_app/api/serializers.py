from rest_framework import serializers
from file_share_app.models  import Folder,File
from django.conf import settings
from django.core.files import File as dj_file

BASE_DIR = settings.BASE_DIR
MEDIA_DIR = BASE_DIR / 'media'
operational_dir = MEDIA_DIR / 'operational_space' 

class FolderSerializer(serializers.ModelSerializer):
    pass
    class Meta:
        model = Folder
        fields = '__all__'


# custom serializer  created only for post request it will return error for get request
#******** understand
class FileListSerial(serializers.Serializer):
    user_token = serializers.CharField(required = False)
    # file = serializers.ListField(
    #     child = serializers.FileField(
    #         max_length = 100000 , 
    #         allow_empty_file = False , 
    #         use_url = False
    #         )
    # )
    files = serializers.FileField(
            max_length = 100000 , 
            allow_empty_file = False , 
            use_url = False,
            required = False
            )
    folder = serializers.CharField(required = False)
    
    def create(self,validated_data):
        # print(validated_data)
        # creating folder object
        folder_obj = Folder.objects.create()

        utk = validated_data.get('user_token')
        files = validated_data.get('files')
        # create file object and set in folder
        print('creating a model')
        
        File.objects.create(
            user_token = utk,
            folder = folder_obj,
            file = files
        ) 
        print("folder object created ",folder_obj.unq_folder_name)
        
        return {
            'user_token': utk,
            'folder':folder_obj.unq_folder_name,
        }
        

    #work on validastions

class FileListSerial2(serializers.Serializer):
    user_token = serializers.CharField(required = False)
    file_name = serializers.CharField(required = True)
    folder = serializers.CharField(required = False)
    
    def create(self,validated_data):
        print(validated_data) # {'user_token': 'arup', 'file_name': 'JobAid-C.png'}
        # creating folder object 
        folder_obj = Folder.objects.create()

        utk = validated_data.get('user_token')

        files = dj_file(open(str(operational_dir/ validated_data.get("file_name")),'r'))
        # error!
        # create file object and set in folder
        print('creating a model',files)
        breakpoint()
        # for _file in files:
        File.objects.create(
            user_token = utk,
            folder = folder_obj,
            file = files #_file
            )
        print(f"data saved {folder_obj.unq_folder_name}")
        # error!
        return {
            'user_token': utk,
            'file_name':folder_obj.unq_folder_name,
        }