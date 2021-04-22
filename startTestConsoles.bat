@ECHO OFF
start cmd /k python server\server.py
start cmd /k python client\client.py 6000 6001 Kony
start cmd /k python client\client.py 6002 6003 Stmpl
