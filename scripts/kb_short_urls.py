from __future__ import annotations

import html
import os
import re
from pathlib import PurePosixPath
from urllib.parse import urljoin

from mkdocs.plugins import BasePlugin


_CHAR_MAP = str.maketrans(
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
)

_SECTION_SLUGS = {
    "Manager": "manager",
    "Seller": "seller",
    "SupportBot": "support",
    "Waiter": "waiter",
    "Афиша и витрина": "showcase",
    "Виджет": "widget",
    "Киоск": "kiosk",
    "Портал": "portal",
    "Прайсы и налоги": "prices-tax",
    "Продажа билетов": "sales",
    "Расписание и события": "schedule",
    "Сайт mooon.by": "site",
    "Сертификаты": "certificates",
}

_PAGE_SLUGS = {
    "Как пользоваться базой знаний.md": "guide",
    "Продажа билетов.md": "sales",
    "Расписание и события.md": "schedule",
    "Сертификаты.md": "certificates",
    "Прайсы и налоги.md": "prices-tax",
    "Технический setup.md": "technical-setup",
    "Афиша и витрина.md": "showcase",
    "Manager.md": "products/manager",
    "Seller.md": "products/seller",
    "Waiter.md": "products/waiter",
    "Портал.md": "products/portal",
    "Киоск.md": "products/kiosk",
    "Виджет.md": "products/widget",
    "Сайт mooon.by.md": "products/site",
    "users-access.md": "users-access",
    "analytics-reports.md": "analytics-reports",
    "setup-equipment.md": "setup-equipment",
    "troubleshooting.md": "troubleshooting",
    "products.md": "products",
    "glossary.md": "glossary",
    "review-gaps.md": "review/gaps",
    "review-questions.md": "review/questions",
}

_TASK_SLUGS = {
    "Продажа билетов/Возврат билетов.md": "sales/refund",
    "Продажа билетов/Базовая работа в Seller Web.md": "sales/seller-basics",
    "Портал/Поиск билета в Portal.md": "sales/ticket-search",
    "Портал/Очистка чека в Portal.md": "sales/clear-receipt",
    "Виджет/Userflow покупки в виджете.md": "sales/widget-purchase",
    "Сертификаты/Активация сертификатов через Portal.md": "certificates/activate",
    "Сертификаты/Проверка и разбор проблем с сертификатами.md": "certificates/troubleshooting",
    "Сертификаты/Создание и выпуск сертификатов в Manager.md": "certificates/create",
    "Прайсы и налоги/Заполнение прайса с НДС.md": "prices-tax/vat-price",
    "Киоск/Запуск киоска.md": "kiosk/start",
    "Афиша и витрина/Сортировка афиши.md": "showcase/order",
    "Waiter/Работа официанта в Waiter.md": "waiter/service",
    "Waiter/Работа администратора в Waiter.md": "waiter/admin",
    "Waiter/Настройка меню и цехов в Manager для Waiter.md": "waiter/menu-setup",
}

_RISK_WORDS = (
    "возврат",
    "оплат",
    "ндс",
    "сертификат",
    "очистка чека",
    "технический setup",
    "массовая отмена",
)


def _slugify(value: str) -> str:
    value = value.lower().translate(_CHAR_MAP)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "page"


def _short_path(src_uri: str) -> str:
    if src_uri == "index.md":
        return ""
    if src_uri in _TASK_SLUGS:
        return _TASK_SLUGS[src_uri]
    if src_uri in _PAGE_SLUGS:
        return _PAGE_SLUGS[src_uri]

    path = PurePosixPath(src_uri)
    parts = list(path.parts)
    stem = path.stem
    slug_parts = [_SECTION_SLUGS.get(part, _slugify(part)) for part in parts[:-1]]
    slug_parts.append(_slugify(stem))
    return "/".join(slug_parts)


class ShortUrlsPlugin(BasePlugin):
    """Publish ASCII URLs while keeping readable Russian source filenames."""

    def on_config(self, config):
        self._redirects: list[tuple[str, str]] = []
        return config

    def on_files(self, files, config):
        for file in files.documentation_pages():
            old_dest = file._get_dest_path()
            short_path = _short_path(file.src_uri)
            new_dest = "index.html" if not short_path else f"{short_path}/index.html"
            if new_dest != old_dest:
                file.dest_uri = new_dest
                self._redirects.append((old_dest, file.url))
        return files

    def on_page_content(self, html_content, page, config, files):
        if page.file.src_uri == "index.md":
            return html_content

        author = html.escape(str(config.extra.get("article_author", "Кирилл Осинский")))
        updated = html.escape(str(config.extra.get("article_updated", "1 июля 2026")))
        meta = (
            '<div class="kb-article-meta" aria-label="Информация о статье">'
            f'<span><strong>Автор</strong> {author}</span>'
            f'<span><strong>Обновлено</strong> <time datetime="2026-07-01">{updated}</time></span>'
            "</div>"
        )
        html_content = re.sub(r"(</h1>)", rf"\1{meta}", html_content, count=1)

        lowered = page.file.src_uri.lower()
        if any(word in lowered for word in _RISK_WORDS):
            warning = (
                '<div class="kb-risk-note" role="note">'
                "<strong>Повышенное внимание.</strong> "
                "Операция может влиять на деньги, учёт или рабочие настройки. "
                "Перед изменением проверьте объект, параметры и ожидаемый результат."
                "</div>"
            )
            html_content = html_content.replace(meta, meta + warning, 1)
        return html_content

    def on_post_page(self, output, page, config):
        if page.file.src_uri in {"review-gaps.md", "review-questions.md"}:
            robots = '<meta name="robots" content="noindex,nofollow,noarchive">'
            output = output.replace("</head>", f"  {robots}\n  </head>", 1)
        return output

    def on_post_build(self, config):
        base_url = str(config.site_url or "/")
        for old_dest, new_url in self._redirects:
            target = urljoin(base_url, new_url)
            destination = os.path.abspath(os.path.join(config.site_dir, *old_dest.split("/")))
            site_root = os.path.abspath(config.site_dir)
            if os.path.commonpath([destination, site_root]) != site_root:
                raise RuntimeError(f"Unsafe redirect destination: {destination}")
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            escaped = html.escape(target, quote=True)
            with open(destination, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(
                    "<!doctype html><html lang=\"ru\"><head>"
                    "<meta charset=\"utf-8\">"
                    f"<meta http-equiv=\"refresh\" content=\"0; url={escaped}\">"
                    f"<link rel=\"canonical\" href=\"{escaped}\">"
                    "<meta name=\"robots\" content=\"noindex\">"
                    f"<title>Перенаправление</title></head><body>"
                    f"<p><a href=\"{escaped}\">Открыть актуальную страницу</a></p>"
                    "</body></html>"
                )
