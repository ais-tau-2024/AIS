import asyncio
import requests
from asgiref.sync import sync_to_async, async_to_sync
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import AutoCompleteRecord

# Глобальный rate limiter: не более 2 запросов в секунду
rate_lock = asyncio.Lock()
request_times = []

async def rate_limit():
    async with rate_lock:
        loop = asyncio.get_running_loop()
        now = loop.time()
        while request_times and now - request_times[0] > 1:
            request_times.pop(0)
        if len(request_times) >= 1:
            wait_time = 1 - (now - request_times[0])
            await asyncio.sleep(wait_time)
        request_times.append(loop.time())

def fetch_data(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

def save_data(data):
    for record in data:
        AutoCompleteRecord.objects.update_or_create(
            value=record.get("value"),
            defaults={"label": record.get("label")}
        )

async def process_request(term):
    await rate_limit()  # Ограничиваем частоту запросов
    url = f"https://platonus.tau-edu.kz/AutoCompleteServlet?term={term}"
    try:
        data = await sync_to_async(fetch_data)(url)
        await sync_to_async(save_data)(data)
        return data
    except Exception:
        return None

class ProxyAutocompleteView(APIView):
    authentication_classes = []  # Отключаем аутентификацию
    permission_classes = [AllowAny]

    def get(self, request):
        # Синхронный метод, оборачивающий асинхронный код
        return async_to_sync(self.async_get)(request)

    async def async_get(self, request):
        term = request.query_params.get("term")
        if not term:
            return Response(
                {"error": "Параметр 'term' обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = await process_request(term)
        if data is not None:
            return Response(data, status=status.HTTP_200_OK)
        fallback_data = await sync_to_async(list)(
            AutoCompleteRecord.objects.filter(label__icontains=term).values("label", "value")
        )
        if fallback_data:
            return Response(fallback_data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Удаленный сервис недоступен, и локальные данные не найдены."},
            status=status.HTTP_502_BAD_GATEWAY
        )
