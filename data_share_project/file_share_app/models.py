from django.db import models
import uuid
# from django.contrib.postgres.fields import ArrayField

class Folder(models.Model):
    # need to inspect
    unq_folder_name = models.UUIDField(primary_key = True,editable = False ,default = uuid.uuid4)
    # access_all_files = models.BooleanField(default = True) # feature
    created_at = models.DateField(auto_now = True)
    
    def __str__(self):
        return f'Folder : {self.unq_folder_name}'


# normaly return type is path but trying give str which is working
# impliment session here
def get_folder_location(instance, filename) -> str:
    '''
    instance : it is the existing File object
    filename : it is the uploaded file(image audio or video) name with it's type

    returning the string output
    '''
    return f'{instance.folder.unq_folder_name}/{filename}'

class File(models.Model):
    user_token = models.CharField(max_length = 10000, blank = True)
    folder = models.ForeignKey(Folder,on_delete = models.CASCADE)
    # session = 
    file = models.FileField(upload_to = get_folder_location)
    created_at = models.DateField(auto_now = True)


    def __str__(self):
        return f'file name :{self.file}  group: {self.user_token}'



# we can check(fields and relations) our model design in admin without starting any things 

