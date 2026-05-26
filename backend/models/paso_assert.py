# ============================================================
#  MODELO: PasoAssert
# ------------------------------------------------------------
#  Representa una validación (assert) que debe cumplirse
#  después de ejecutar la API asociada al paso.
#
#  tipo:
#   - status_code
#   - jsonpath
#   - header
#   - body_contains
#   - regex
#   - length
#
#  operador:
#   - equals / not_equals
#   - contains / not_contains
#   - gt / gte / lt / lte
#   - matches_regex
#   - len_equals / len_gt / len_lt
#   (se mantienen también los operadores legacy: ==, !=, >, <, >=, <=)
# ============================================================

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
from db.base import Base

if TYPE_CHECKING:
    from .paso import Paso


class PasoAssert(Base):
    __tablename__ = "paso_assert"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    paso_id: Mapped[int] = mapped_column(
        ForeignKey("paso.id"),
        nullable=False,
        index=True
    )

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)

    expresion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    operador: Mapped[str] = mapped_column(String(50), nullable=False)

    valor_esperado: Mapped[str | None] = mapped_column(Text, nullable=True)

    mensaje_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    orden: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # -----------------------------
    # Relación inversa con Paso
    # -----------------------------
    paso: Mapped["Paso"] = relationship(
        "Paso",
        back_populates="asserts",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<PasoAssert {self.id} paso={self.paso_id} tipo={self.tipo}>"
