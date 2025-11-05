from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Repository for RefreshToken operations"""

    def __init__(self, db: Session):
        super().__init__(RefreshToken, db)

    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """
        Obtiene un refresh token por su valor

        Args:
            token: Valor del token

        Returns:
            RefreshToken si existe, None en caso contrario
        """
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def get_by_user_id(self, user_id: int, active_only: bool = True) -> List[RefreshToken]:
        """
        Obtiene todos los refresh tokens de un usuario

        Args:
            user_id: ID del usuario
            active_only: Si True, solo devuelve tokens válidos (no revocados y no expirados)

        Returns:
            Lista de RefreshTokens
        """
        query = self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id)

        if active_only:
            query = query.filter(
                RefreshToken.is_revoked == False,
                RefreshToken.expires_at > datetime.utcnow()
            )

        return query.all()

    def revoke_token(self, token: str) -> bool:
        """
        Revoca un refresh token

        Args:
            token: Valor del token a revocar

        Returns:
            True si se revocó exitosamente, False si no se encontró
        """
        refresh_token = self.get_by_token(token)
        if not refresh_token:
            return False

        refresh_token.is_revoked = True
        self.db.commit()
        return True

    def revoke_all_user_tokens(self, user_id: int) -> int:
        """
        Revoca todos los refresh tokens de un usuario
        (útil para logout de todas las sesiones)

        Args:
            user_id: ID del usuario

        Returns:
            Número de tokens revocados
        """
        result = self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({"is_revoked": True})
        self.db.commit()
        return result

    def delete_expired_tokens(self) -> int:
        """
        Elimina todos los refresh tokens expirados
        (útil para limpieza periódica)

        Returns:
            Número de tokens eliminados
        """
        result = self.db.query(RefreshToken).filter(
            RefreshToken.expires_at < datetime.utcnow()
        ).delete()
        self.db.commit()
        return result

    def create_refresh_token(self, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
        """
        Crea un nuevo refresh token

        Args:
            token: Valor del token
            user_id: ID del usuario
            expires_at: Fecha de expiración

        Returns:
            RefreshToken creado
        """
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token
