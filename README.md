
# prio-main (Python port)

Port awal dari bot Discord Node.js ke Python (`discord.py`). Struktur dibuat agar mirip dengan project asli dan siap diisi detail logic.

## Fitur yang dipindah (versi awal / placeholder)
- Kerangka command (`commands/*`) sebagai *cogs*
- Model database via **Motor** (MongoDB async)
- Scheduler via **APScheduler**
- Logger layanan, validator .env, utilitas tanggal & pagination
- Event & error handler dasar

## Cara Menjalankan
1. Python 3.10+ disarankan.
2. Buat virtualenv lalu install dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Salin `.env.example` menjadi `.env` dan isi token Discord & MongoDB:
   ```bash
   cp .env.example .env
   # Edit DISCORD_TOKEN dan MONGODB_URI
   ```
4. Jalankan bot:
   ```bash
   python main.py
   ```

## Struktur
```
.env.example
__init__.py
commands/__init__.py
commands/priority_manage.py
commands/priority_stats.py
commands/reminder.py
commands/user_dashboard.py
controllers/admin_panel_controller.py
controllers/button_controller.py
controllers/command_controller.py
controllers/error_controller.py
controllers/event_controller.py
controllers/helpers.py
controllers/interaction_controller.py
controllers/modal_controller.py
controllers/priority_controller.py
controllers/stats_controller.py
main.py
models/priority_log.py
models/reminder.py
models/subscription.py
requirements.txt
routes/commands.py
services/bot_logger_service.py
services/reminder_service.py
services/role_management_service.py
services/subscription_service.py
services/webhook_service.py
utils/database_connector.py
utils/date_formatter.py
utils/environment_validator.py
utils/pagination.py
```

## Catatan Migrasi
- Perintah di `commands/*` bersifat contoh. Silakan map dari file asli:
  - `priorityManage.js` → `commands/priority_manage.py`
  - `priorityStats.js` → `commands/priority_stats.py`
  - `reminder.js` → `commands/reminder.py`
  - `userDashboard.js` → `commands/user_dashboard.py`
- Model:
  - `models/PriorityLog.js` → `models/priority_log.py`
  - `models/Reminder.js` → `models/reminder.py`
  - `models/Subscription.js` → `models/subscription.py`
- Service penjadwalan, role, subscription, & webhook sudah disiapkan placeholder.

## Lanjutan
- Isi logika spesifik sesuai project asli (controller & services).
- Jika project asli menggunakan slash command, kita bisa ubah ke `app_commands` (tree) di `discord.py`.
- Jika ada WebSocket/HTTP admin panel terpisah, tambahkan `aiohttp` server.
