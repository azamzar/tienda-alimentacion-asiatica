from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.user import UserRole

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = "tu_clave_secreta_super_segura_cambiala_en_produccion"  # TODO: Mover a variables de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña almacenado en la BD

    Returns:
        True si coinciden, False en caso contrario
    """
    # Truncate password to 72 characters for bcrypt compatibility
    # bcrypt has a limit of 72 bytes, so we truncate to be safe
    password_truncated = plain_password[:72] if len(plain_password) > 72 else plain_password
    return pwd_context.verify(password_truncated, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    # Truncate password to 72 characters for bcrypt compatibility
    # bcrypt has a limit of 72 bytes, so we truncate to be safe
    password_truncated = password[:72] if len(password) > 72 else password
    return pwd_context.hash(password_truncated)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso

    Args:
        data: Datos a incluir en el token (user_id, email, role)
        expires_delta: Tiempo de expiración personalizado

    Returns:
        Token JWT firmado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT

    Args:
        token: Token JWT a decodificar

    Returns:
        Datos del token si es válido, None si es inválido o expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
