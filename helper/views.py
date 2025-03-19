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

from django.urls import get_resolver
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

EXCLUDED_PREFIXES = [
    "admin/",
    "grappelli/",
    "swagger/",
    "redoc/",
    "filebrowser/"
]

@csrf_exempt
def list_routes(request):
    resolver = get_resolver()
    routes = []

    for pattern in resolver.url_patterns:
        route_info = extract_route_info(pattern)
        if route_info:
            routes.extend(route_info)

    # Фильтруем маршруты, исключая ненужные
    routes = [route for route in routes if not is_excluded(route["path"])]

    # Форматируем вывод
    output = format_routes(routes)
    return HttpResponse(output, content_type="text/plain")


def extract_route_info(pattern, prefix=""):
    routes = []

    if hasattr(pattern, "url_patterns"):  # Это include()
        for sub_pattern in pattern.url_patterns:
            routes.extend(extract_route_info(sub_pattern, prefix + str(pattern.pattern)))
    else:
        view = pattern.callback
        methods = []

        if hasattr(view, "view_class"):  # Class-based View
            methods = getattr(view.view_class, "http_method_names", [])
        elif hasattr(view, "allowed_methods"):  # Function-based View
            methods = view.allowed_methods
        else:
            methods = ["GET"]  # По умолчанию считаем, что это GET

        route = {
            "methods": ", ".join(methods).upper(),
            "path": prefix + str(pattern.pattern),
            "controller": get_view_name(view)
        }
        routes.append(route)

    return routes


def get_view_name(callback):
    if hasattr(callback, "view_class"):
        return f"{callback.view_class.__module__}.{callback.view_class.__name__}"
    elif hasattr(callback, "__module__"):
        return f"{callback.__module__}.{callback.__name__}"
    return str(callback)


def is_excluded(path):
    """Проверяет, начинается ли путь с одного из исключённых префиксов."""
    return any(path.startswith(excluded) for excluded in EXCLUDED_PREFIXES)


def format_routes(routes):
    headers = ["METHODS", "PATH", "CONTROLLER"]

    # Фильтрация методов (убираем OPTIONS и TRACE)
    for route in routes:
        allowed_methods = route["methods"].split(", ")
        filtered_methods = [m for m in allowed_methods if m not in ["OPTIONS", "TRACE"]]
        route["methods"] = ", ".join(filtered_methods)

    # Вычисляем максимальную ширину для каждого столбца (с учётом заголовков)
    col_widths = [len(h) for h in headers]
    for route in routes:
        col_widths[0] = max(col_widths[0], len(route["methods"]))
        col_widths[1] = max(col_widths[1], len(route["path"]))
        col_widths[2] = max(col_widths[2], len(route["controller"]))

    header_line = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |"
    divider_line = "|-" + "-|-".join("-" * w for w in col_widths) + "-|"
    
    rows = []
    for route in routes:
        row = "| " + " | ".join([
            route["methods"].ljust(col_widths[0]),
            route["path"].ljust(col_widths[1]),
            route["controller"].ljust(col_widths[2])
        ]) + " |"
        rows.append(row)

    return "\n".join([header_line, divider_line] + rows)
