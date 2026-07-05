# Initial message для автономной обработки Maverick KB

Скопируй этот текст в Codex/другого агента. Замени только путь в строке `SOURCE_FOLDER`.

---

Ты работаешь с проектом Maverick KB.

SOURCE_FOLDER:

```text
D:\JetBrains\cl_maverick_kb\inbox\_new\<ПАПКА_ИЛИ_ФАЙЛ_С_МАТЕРИАЛАМИ>
```

## Goal

Автономно обработай все материалы из `SOURCE_FOLDER` и преврати их в рабочие инструкции Maverick KB.

Нужен не отчёт о попытке, а готовый результат:

- материалы разобраны;
- видео/аудио транскрибированы или обработаны fallback-способом;
- аудио и экран сопоставлены;
- скриншоты извлечены и подготовлены;
- существующие страницы проверены на пересечение;
- канонические wiki-страницы созданы или обновлены;
- неподтверждённые факты вынесены в `QUESTIONS.md`;
- `INDEX.md` и `CHANGELOG.md` обновлены;
- публичная Pages-версия синхронизирована;
- MkDocs build прошёл;
- ссылки, картинки и поиск проверены;
- изменения закоммичены и запушены;
- GitHub Pages deploy успешен;
- live URL проверены.

Это сообщение является явным `approve` на полный цикл. Не останавливайся после плана и не жди дополнительного разрешения.

## Что прочитать перед работой

Прочитай и следуй:

```text
D:\JetBrains\cl_maverick_kb\AGENTS.md
D:\JetBrains\cl_maverick_kb\docs\MAVERICK_KB_PROJECT_BRIEF.md
D:\JetBrains\cl_maverick_kb\docs\MAVERICK_KB_TZ.md
D:\JetBrains\cl_maverick_kb\docs\MAVERICK_KB_PROCESS.md
D:\JetBrains\cl_maverick_kb\docs\MAVERICK_KB_AGENT_PROMPT.md
D:\JetBrains\cl_maverick_kb\docs\MAVERICK_KB_CHECKLIST.md
D:\JetBrains\cl_maverick_kb\docs\WIKI_DIGESTION_RULES.md
D:\JetBrains\ai-skills\skills\maverick-kb-content-pipeline\SKILL.md
D:\JetBrains\ai-skills\skills\maverick-kb-content-pipeline\references\*.md
```

## Важно про транскрипцию

Не ищи только команду `whisper` в PATH и не требуй PowerShell-команду `whisper`.

Локальный Whisper находится здесь:

```text
D:\soft\Whisper\whisper-cli.exe
```

В Git Bash/MSYS:

```bash
/d/soft/Whisper/whisper-cli.exe
```

Модели:

```text
D:\soft\Whisper\models\ggml-base.bin
D:\soft\Whisper\models\ggml-small.bin
D:\soft\Whisper\models\ggml-large-v3.bin
```

Отсутствие `OPENAI_API_KEY`, Python-модуля `openai`, Python-модуля `whisper` или команды `whisper` в PATH не является причиной остановки.

Если полноценный транскрипт не получается, продолжай через fallback:

1. прямой `whisper-cli.exe`;
2. нарезка аудио на сегменты;
3. `.venv_stt` / `faster-whisper`, если доступен;
4. contact sheets + скриншоты + частичный транскрипт;
5. спорные бизнес-факты — в `QUESTIONS.md`.

Остановиться можно только если `SOURCE_FOLDER` физически недоступен, агент запущен не на машине с `D:\JetBrains` / `D:\soft`, нет прав записи или требуется опасное действие с риском потери данных.

## Финальный ответ

Отвечай только после полной проверки.

Формат:

```text
Готово.

Обработано:
- ...

Создано/обновлено:
- ...

Где лежит:
- ...

Проверка:
- mkdocs build --strict: OK
- links/assets: OK
- search: OK
- commit: <hash>
- deploy: success
- live URL: ...

Вопросы:
- ...
```
