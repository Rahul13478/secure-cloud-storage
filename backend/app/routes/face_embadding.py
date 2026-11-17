from fastapi import APIRouter , UploadFile , Depends,  status , HTTPException
from deepface import DeepFace
import os 
import shutil
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.security.auth import verify_token
from app.models.user import User
from app.models.face import Face

router = APIRouter(prefix="/face_embadding", tags=["Face_embadding"])
UPLOAD_DIR = r"F:\cloud-storage\backend\app\image-storage\store-image-for-faceveryfication"


# i have to upload the img normaly like file upload then i have to extract the embeddings and store them in 
# face table with the user id as a foraignkey 
@router.post("/upload-image")
def upload_image(image : UploadFile , db :Session = Depends(get_db) , get_id = Depends(verify_token) ):
    get_user = db.query(User).filter_by(id = get_id["id"]).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    original_image_name = image.filename #this veriable will store the original image name 
    image_path = os.path.join(UPLOAD_DIR , original_image_name) #this veriable will store the image path
    with open(image_path , "wb") as buffer:
        shutil.copyfileobj(image.file , buffer) #the image now saved in the upload_dir

    face_embeddings = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        detector_backend="opencv"
    )
    facial_embeddings = face_embeddings[0]["embedding"]
    take_embedding = facial_embeddings
    image_database = Face(user_id = get_user.id , embedding = take_embedding ,model_name = "Facenet")
    db.add(image_database)
    db.commit()
    db.refresh(image_database)

    return{"messgae":"complete"}