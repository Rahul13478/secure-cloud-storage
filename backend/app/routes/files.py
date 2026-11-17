#to upload file by using fastapi u need UploadFile 
# and need to install python multipart 
# foraign key meens the clomum have data from othe table cloum ? 
# but here we actualy calling the table first so we have the data 
# and we cansimple put it there without using a foraing key for this assessledger tabel


from fastapi import APIRouter  , UploadFile  , Depends  , HTTPException , status  , BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
from app.file_storage_cloud.s3_storage import save_bytes , read_bytes , delete_bytes

from sqlalchemy.orm import Session
from app.models.files import File , User
from app.core.settings import setting

import shutil 
from  app.db.database import get_db
import os 
import uuid
from app.security.auth import verify_token , encrypt_file , decrypt_file , delet_download_file
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.face_varify.face_varify_2 import varify_face
from app.blockchain.blockchain import add_block
from app.AI.security_cheack import cheack_security
from app.ML.activity_checker import cheack_activity

router = APIRouter(prefix="/files",tags=["Files"])

UPLOAD_DIR = "storage/uploads" #this is the dir and the sub dir 
DOWNLOAD_DIR ="file_download"

key = setting.ENCRYPTION_KEY
real_key = bytes.fromhex(key)

os.makedirs(UPLOAD_DIR , exist_ok=True) #this creats a dir if not exist 

@router.post("/upload")
async def upload_file(file:UploadFile , db:Session = Depends(get_db) ,get_id = Depends(verify_token)):
    get_user = db.query(User).filter_by(id  = get_id["id"]).first()

    
    original_filename = file.filename #file name stored in a veriable 
    
    extension = os.path.splitext(original_filename)[1] #extension from the filename .pdf
    uuid_string = uuid.uuid4().hex #creatig an uniq uuid
    stored_filename  = uuid_string+extension #making a new file name that will go in stored file name 
    file_path = os.path.join(UPLOAD_DIR , stored_filename)  #writing an address in a papper 
    
    with open(file_path , "wb") as buffer:
        shutil.copyfileobj(file.file , buffer) #file saved in disk

    output_path = file_path+ ".enc"
    encrypt_file(file_path , output_path, real_key)   
    os.remove(file_path) 
    user_id_str = str(get_user.id)
    label_key = user_id_str +"/"+ stored_filename + ".enc"
    print(label_key)
    with open(output_path , "rb") as enc_file:
         byts = enc_file.read()
    save_bytes(label_key , byts)     
    os.remove(output_path)

    new_file  =  File(original_filename = original_filename , stored_filename = stored_filename,
                      file_path = label_key , file_size = file.size, content_type = file.content_type,
                      owner_id = get_user.id)  

    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    file_id  = new_file.id
    add_block(db , "upload" ,get_id["id"] , file_id  )
    security = cheack_security(db , get_id["id"]) 
    print(security)
    cheak = cheack_activity(security["download"] , security["upload"] , security["delet"])# it will cheak the user is suspicious or not 
    print(cheak)
    if cheak == "suspicious" :
        add_block(db, "suspicious_activity" , get_id["id" ], file_id)



    return    {
        "filename":original_filename,
        "stored_filename":stored_filename,
        "content_type":file.content_type,
        "save_path" : label_key
    } 




@router.get("/get_file")
def file_info(get_id = Depends(verify_token), db:Session =Depends(get_db)):
    result = []
    
    get_file_info = db.query(File).filter(File.owner_id==get_id["id"]).all()

    

    for files in get_file_info:
        result.append({"filename":files.original_filename,
                       "file_id": files.id,
                       "owner-id":files.owner_id,
                       "filesize":files.file_size,
                       "stored-name":files.stored_filename})

    return result 
    


@router.post("/download/{get_file_id}")
def download_file(face_image: UploadFile , get_file_id :int,background : BackgroundTasks,  get_user_id = Depends(verify_token) ,  db : Session = Depends(get_db)):
    get_file = db.query(File).filter_by(id=get_file_id).first()
    if get_file is None:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    real_file_path = get_file.file_path
    real_file = str(real_file_path)
    



    output_path = os.path.join(DOWNLOAD_DIR , get_file.stored_filename)
    temporary_path = output_path + ".enc"
   

    
    if get_file.owner_id == get_user_id["id"]:
        verified = varify_face(face_image , db , get_user_id["id"] )
        if verified is True:
            data=read_bytes(real_file )
            with open(temporary_path , "wb")as f :
                 f.write(data) 
            
            decrypt_file(temporary_path , output_path , real_key)
            os.remove(temporary_path)
            add_block(db , "download" , get_user_id["id"] , get_file.id)  # this will add the data in block chain
            security = cheack_security(db , get_user_id["id"]) 
            print(security)
            cheak = cheack_activity(security["download"] , security["upload"] , security["delet"])# it will cheak the user is suspicious or not 
            print(cheak)
            if cheak == "suspicious" :
                 add_block(db, "suspicious_activity" , get_user_id["id" ], get_file.id)
            background.add_task(delet_download_file , output_path)
        
            return  FileResponse(
                                 path=output_path,
                                 filename=get_file.original_filename,
                                 media_type='application/octet-stream'
                     
                             )
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)    
        
      
    
       
        
@router.delete("/delet/{file_id}")
def delet_file(file_id:int, get_user_id = Depends(verify_token) ,   db : Session = Depends(get_db)):
    get_file = db.query(File).filter_by(id = file_id).first()
    if get_file is None:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    
   
    if get_file.owner_id == get_user_id["id"] :
        add_block(db , "delete" , get_user_id["id"] , get_file.id)
        security = cheack_security(db , get_user_id["id"]) 
        print(security)
        cheak = cheack_activity(security["download"] , security["upload"] , security["delet"])# it will cheak the user is suspicious or not 
        print(cheak)
        if cheak == "suspicious" :
             add_block(db, "suspicious_activity" , get_user_id["id" ], get_file.id)

        delete_bytes(get_file.file_path)
        db.delete(get_file)
        db.commit()
        output = {
            "massage":"file deleted from database "
        }
 

        return output
        
        
