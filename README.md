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

## Run backend using docker
- Make sure you have docker installed and running
- follow this to create SSL for local: https://www.section.io/engineering-education/how-to-get-ssl-https-for-localhost/


```docker compose up --build```

## Run backend locally
### Run migrations
- Make sure you have mysql running (for example XAMPP)

```alembic upgrade head```

### Start local server:
#### mac:
``` python3 main.py ```
#### windows:
```python main.py```
