import pytest 
from types import SimpleNamespace  #fake user r object create korar jonne
from unittest.mock import MagicMock, AsyncMock #fake db,fake redis ,fake rate limit korar jonne also fake email
from fastapi import FastAPI               #create a test client for the FastAPI app
from fastapi.testclient import TestClient     #send requests to the FastAPI app and receive responses

from app.routes.user import    # <-- CHANGE to your real path  je folder e user.py ache setate change korbi 
from app.db.database import get_db        #overwite korar jonne with fake db 

