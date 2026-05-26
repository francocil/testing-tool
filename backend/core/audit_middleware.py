from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from sqlalchemy.orm import Session
from db.session import SessionLocal
from services.auditoria import registrar_evento
from schemas.auditoria import AuditoriaCreate

class AuditoriaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        try:
            ruta = request.url.path.lower()

            # Registrar solo eventos relevantes
            if "login" in ruta or "logout" in ruta or "refresh" in ruta:
                db: Session = SessionLocal()

                usuario_id = None
                if request.state and hasattr(request.state, "user"):
                    usuario_id = request.state.user.id

                data = AuditoriaCreate(
                    usuario_id=usuario_id,
                    accion=ruta,
                    ip=request.client.host,
                    user_agent=request.headers.get("User-Agent")
                )
                registrar_evento(db, data)
                db.close()

        except Exception:
            pass

        return response
