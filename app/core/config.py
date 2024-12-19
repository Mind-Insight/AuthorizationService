from pathlib import Path
from pydantic import BaseModel
from databases import Database


BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "users.db"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


DATABASE_URL = "sqlite+aiosqlite:///./users.db"
database = Database(DATABASE_URL)


auth_jwt = AuthJWT()
