# fullstack_backend

### Install requirements:
``` pip3 install -r requirements.txt ```

### Create /config/cors.py -file
- Check corsExample.py
- add your frontend address for example: http://localhost:5173

### Create cert folder to root
- run in terminal

```openssl genrsa -out cert/id_rsa 4096```

```openssl rsa -in cert/id_rsa -pubout -out cert/id_rsa.pub```

### Start server (mac):
``` python3 main.py ```