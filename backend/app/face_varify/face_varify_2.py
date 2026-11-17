from fastapi import UploadFile  , Depends ,HTTPException , status
from deepface import DeepFace

from app.models.face import Face
import os 
import shutil
import uuid

UPLOAD_DIR = r"F:\cloud-storage\backend\app\image2.0-storage\for-making-verification"

def varify_face(faces:UploadFile , db , get_id ):
    get_user  = db.query(Face).filter(Face.user_id==get_id).first()  #  <--finding the user 

    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    get_embeddings = get_user.embedding #extracting stored embeddings from that user

    original_name = faces.filename

    extension = os.path.splitext(original_name)[1]

    uuid_string =uuid.uuid4().hex

    stored_name = uuid_string+extension

    image_path = os.path.join(UPLOAD_DIR , stored_name)
  
#making new embedding for new face --->
    try:
        with open(image_path , "wb") as buffer :
            shutil.copyfileobj(faces.file, buffer)

        face_embeddings_new = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            detector_backend="opencv"
        )

        new_embeddings = face_embeddings_new[0]["embedding"]  
        take_new_embeddings = new_embeddings

        verify_face = DeepFace.verify(
        img1_path=get_embeddings,
        img2_path=take_new_embeddings,
        model_name="Facenet",
        distance_metric="cosine"
    )
        
    finally:
         if os.path.exists(image_path):
          os.remove(image_path)

    
    return verify_face["verified"]





