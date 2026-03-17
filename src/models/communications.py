"""ORM модели: Коммуникации — отзывы, вопросы, претензии."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Integer, Numeric, String, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class WbFeedback(Base):
    """Отзыв покупателя."""
    __tablename__ = "wb_feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feedback_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="ID отзыва")
    created_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания")
    product_valuation: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Оценка товара 1–5")
    was_viewed: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Просмотрен")
    text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Текст отзыва")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    supplier_article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Текст ответа продавца")
    answer_state: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус ответа")
    user_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Имя покупателя")
    is_able_to_change_grade: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Можно изменить оценку")
    photo: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Фото в отзыве (JSON)")
    video: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Видео в отзыве (JSON)")
    product_details: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Данные товара (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbQuestion(Base):
    """Вопрос покупателя."""
    __tablename__ = "wb_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="ID вопроса")
    created_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания")
    state: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус: none=новый, wbRu=отвечен WB, answered=отвечен продавцом")
    text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Текст вопроса")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Текст ответа")
    user_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Имя покупателя")
    product_details: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Данные товара (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbClaim(Base):
    """Претензия покупателя."""
    __tablename__ = "wb_claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    claim_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="ID претензии")
    created_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания")
    state: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус претензии")
    text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Текст претензии")
    user_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Имя покупателя")
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Текст ответа продавца")
    product_details: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Данные товара (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")
