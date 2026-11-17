#learning blockchain --->

#1 . we will store the data in JASON formate in blocks . each blocks 
# will be defferentiate with a fingerprint .. 

#how we make the fingerprint ??
# By using hash .. we will use SHA256 -->
# each block will have its own hash and also hash of previous block 
# so that it cannot get tempered ...
#this is how we make a chaing a block will have the previous one hash and will gove his hash 
# to the next block ...

#a ledger is a collactions of blocks 

# block data
# → convert all fields into one consistent text/JSON value
# → SHA-256 hash
# → block_hash

# Python hashlib sha256 hash multiple values JSON dumps sort_keys --> for coverting all data
# in a block to genarate a block hash 

# 1 block will have this datas -->
# event_type, user_id, file_id, timestamp, previous_hash = GENESIS

# convert all the data into a hash for block hash 
from app.models.accessledger import AccessLedger
from datetime import datetime , timezone
import json
import hashlib


def add_block(db , event_type , user_id , file_id):
    get_ledger_row = db.query(AccessLedger).order_by(AccessLedger.id.desc()).first()
    time_stamp = datetime.now(timezone.utc)
    if get_ledger_row is None:
         previous_hash = "GENESIS"
    else:
         previous_hash = get_ledger_row.block_hash 
        
    iso_formate = time_stamp.isoformat() # coverting time into string because it cant be string automticaly 
          
    json_data = {
               "event_type" : event_type,
               "user_id": user_id,
               "file_id":file_id,
               "timestamp": iso_formate,
               "previous_hash":previous_hash
   
           }
           # converting json to string 
    json_string = json.dumps(json_data , sort_keys=True)
   
    block_hashed = hashlib.sha256(json_string.encode("utf-8")).hexdigest()
    
     
    new_block = AccessLedger(event_type = event_type , user_id = user_id , file_id = file_id , timestamp = time_stamp , previous_hash = previous_hash , block_hash =block_hashed )
    db.add(new_block)
    db.commit()
    db.refresh(new_block)

    return {"message ":"ok "}
   
#need to create  a func that will cheak each blocks previous hash with  previous blocks block hash       
# i have to use for loop 

def verify_chain(db):
     get_rows  = db.query(AccessLedger).order_by(AccessLedger.id.asc()).all()
     expected_previous_hash = "GENESIS"
     for i in get_rows:
          if i.previous_hash != expected_previous_hash:
               return False
          if i.previous_hash == expected_previous_hash:
               json_data = {
                    "event_type":i.event_type,
                    "user_id":i.user_id,
                    "file_id":i.file_id,
                    "timestamp":i.timestamp.astimezone(timezone.utc).isoformat(),
                    "previous_hash":i.previous_hash

               }
               json_string = json.dumps(json_data, sort_keys=True)
               
               block_hash_2 = hashlib.sha256(json_string.encode("utf-8")).hexdigest()
               if block_hash_2 != i.block_hash :
                     return False
               if i.block_hash == block_hash_2:
                    expected_previous_hash = i.block_hash
          

     return True          

     
          
         

