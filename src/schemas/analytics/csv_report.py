"""Схемы: Аналитика продавца — CSV-отчёты."""
from pydantic import BaseModel, Field


class NmReportDownloadRequest(BaseModel):
    """Запрос на формирование CSV-отчёта по артикулам."""
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID). Если не указаны — по всем.")
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    reportType: str | None = Field(None, description="Тип отчёта: `by_nm` — по артикулам, `by_period` — по периоду")


class NmReportDownloadItem(BaseModel):
    """Задача формирования CSV-отчёта."""
    downloadId: str | None = Field(None, description="ID задачи формирования отчёта")
    status: str | None = Field(None, description="Статус: `pending`, `processing`, `done`, `error`")
    createAt: str | None = Field(None, description="Дата создания задачи (ISO 8601)")
    updatedAt: str | None = Field(None, description="Дата последнего обновления (ISO 8601)")
    params: dict | None = Field(None, description="Параметры запроса")


class NmReportDownloadsResponse(BaseModel):
    """Список задач формирования CSV-отчётов."""
    data: list[NmReportDownloadItem] | None = Field(None, description="Задачи")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class NmReportRetryRequest(BaseModel):
    """Повторный запрос на формирование CSV-отчёта."""
    downloadId: str = Field(description="ID задачи для повторного запуска")
