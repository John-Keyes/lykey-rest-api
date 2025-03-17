
## dependencies
- package manager -> uv: https://docs.astral.sh/uv/
- sqlalchemy
- alembic for migrations


## activate and deactivate .venv (virtual environment)

- Activate Command:
```bash
source .venv/Scripts/activate
```
- Deactivate Command
```bash
deactivate
```

## alembic

- To migrate
```bash
alembic revision --autogenerate -m "message"
```

- Apply Migration
```bash
alembic upgrade head
```

## Swagger
- at /docs endpoint


## Revisit
https://dev.to/spaceofmiah/jwt-authentication-in-fastapi-comprehensive-guide--c0p 

Email Validation:

https://medium.com/@philipokiokio/user-authentication-with-checks-in-fastapi-e34fe5879448

## Redis



## Creating User
    This procedure creates a new unverified user.

    I am using a definer to specify the security context so that only certain users can access this.

    We must create the user with the privileges:
    Create USER IF NOT EXISTS SFS1 IDENTIFIED BY '<connection password>';

    GRANT ALL PRIVILEGES ON sfs1.* TO <user pattern>;

    Examples
    GRANT ALL PRIVILEGES ON sfs1.* TO `SFS1`@`%`;
    GRANT ALL PRIVILEGES ON sfs1.* TO 'root'@'localhost';