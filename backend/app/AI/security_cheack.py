#need to make a func that will cheack accessledger table and see if any user is suspicious -->
# doing first for only download 
#RULE - if a user download 10 files unders 1 minit it called suspicious 
# need to learn how to get download rows for a perticular user in last minute -->

from sqlalchemy import select , func 
from datetime import datetime , timedelta , timezone
from app.models.accessledger import AccessLedger


#this function should be call in download api 
def cheack_security(db , user_id):
    time_treshhold = datetime.now(timezone.utc) - timedelta(minutes=1)
    get_info = (select(AccessLedger.event_type ,  func.count(AccessLedger.id).label("total_count"))
                .where(AccessLedger.user_id == user_id)
                
                .where(AccessLedger.timestamp>= time_treshhold)
                .group_by(AccessLedger.event_type ))
    result = db.execute(get_info).all()
    download = 0
    upload = 0
    delet = 0 
    
    for row in result:
        if row.event_type == "download":
            download = row.total_count
        elif row.event_type == "upload":
            upload = row.total_count    
        elif row.event_type == "delete" :
            delet = row.total_count   
      
    # if count > 5 :
    #     status= "suspicious"
    # else:
    #     status = "normal"  
    return {"download": download,
            "upload": upload,
            "delet": delet}      


    