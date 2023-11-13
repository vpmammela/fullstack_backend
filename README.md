# fullstack_backend

### Install requirements:
``` pip3 install -r requirements.txt ```

### Create /config/cors.py -file
- Check corsExample.py
- add your frontend address for example: http://localhost:5173

### Create .env -file
JWT_SECRET=
JWT_TYPE=
SSL=
AUTH_TYPE=
DB=

for local db have used "mysql+mysqlconnector://root:@localhost/fullstack3002mvp"

### Run migrations
```alembic upgrade head```

### Start server (mac):
``` python3 main.py ```