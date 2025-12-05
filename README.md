
# ============================================================================
# FILE: README.md
# ============================================================================
# FastAPI + Telegram Bot Project

A complete example project showing FastAPI + Telegram Bot integration with proper architecture.

## 🏗️ Architecture Patterns Used

### 1. **Inheritance**
- `BaseModel` → `Report`, `Notification` (SQLAlchemy models)
- `BaseSchema` → All Pydantic schemas
- `CRUDBase` → `CRUDReport`, `CRUDNotification`
- `BaseService` → `ReportService`, `NotificationService`

### 2. **Composition**
- Services use CRUD instances: `self.crud = crud_report`
- NotificationService uses Bot: `self.bot = bot`
- Middleware wraps the application
- Routers compose into main API router

## 📁 Project Structure

```
app/
├── config/          # Settings and configuration
├── core/            # Database and core functionality
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic validation schemas
├── crud/            # Database operations (Create, Read, Update, Delete)
├── services/        # Business logic layer
├── api/             # FastAPI endpoints
│   └── v1/
│       └── endpoints/
├── bot/             # Telegram bot handlers
├── middleware/      # Request/response interceptors
└── main.py          # Application entry point
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your values:
# - BOT_TOKEN (get from @BotFather)
# - NOTIFICATION_CHAT_ID (your chat ID)
# - ALLOWED_CHAT_IDS (optional, restrict bot to specific chats)
```

### 3. Get Telegram Bot Token
1. Message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow instructions
4. Copy the token to `.env`

### 4. Get Your Chat ID
1. Start your bot
2. Send `/start` to your bot
3. Copy the chat ID shown

### 5. Run Application
```bash
python -m app.main
```

## 📚 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤖 Bot Commands

- `/start` - Show welcome message and your chat ID
- `/status` - Check API health status
- `/reports` - List all reports
- `/create` - Create a test report

## 🔒 Security

### IP Whitelist
Only IPs in `ALLOWED_IPS` can call the API.

Default allowed IPs:
- `127.0.0.1`
- `localhost`
- `::1`

To add more IPs, edit `.env`:
```
ALLOWED_IPS=127.0.0.1,localhost,::1,192.168.1.100
```

### Chat Restrictions
Bot can be restricted to specific chats:
```
ALLOWED_CHAT_IDS=-1001234567890,123456789
```

## 📝 Example Usage

### Create Report via API
```bash
curl -X POST http://localhost:8000/api/v1/reports/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Sales Report", "description": "Q4 2024 sales"}'
```

### Send Notification via API
```bash
curl -X POST http://localhost:8000/api/v1/notifications/send \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "YOUR_CHAT_ID", "message": "Hello from API!"}'
```

### Broadcast Message
```bash
curl -X POST "http://localhost:8000/api/v1/notifications/broadcast?message=Test%20message"
```

## 🎓 Learning Points

### Inheritance Example
```python
# Base class
class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

# Child class inherits id
class Report(BaseModel):
    name = Column(String)
```

### Composition Example
```python
# Service composes CRUD and Bot
class ReportService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.crud = crud_report  # Composition!
```

### Generic CRUD Example
```python
# Works with any model!
class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
```

## 🔄 Request Flow

```
User → API Endpoint → Service → CRUD → Database
                    ↓
              Telegram Bot (notification)
```

Example:
1. POST `/api/v1/reports/` creates report
2. `ReportService` uses `CRUDReport` to save
3. Background task processes report
4. `NotificationService` sends Telegram message

## 🛠️ Development

### Add New Endpoint
1. Create schema in `app/schemas/`
2. Create model in `app/models/`
3. Create CRUD in `app/crud/`
4. Create service in `app/services/`
5. Create endpoint in `app/api/v1/endpoints/`
6. Register router in `app/api/v1/router.py`

### Add New Bot Command
1. Create handler in `app/bot/handlers.py`
2. Register in `register_handlers()` function

## 📊 Database

Uses SQLite by default. To use PostgreSQL:

```bash
# Install driver
pip install psycopg2-binary

# Update .env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🐛 Troubleshooting

### Bot not responding
- Check BOT_TOKEN is correct
- Check bot is started (check console logs)
- Send `/start` to bot first

### API returns 403
- Check your IP is in ALLOWED_IPS
- Default only allows localhost

### Database errors
- Delete `app.db` file and restart
- Check DATABASE_URL in .env

## 📦 Optional: Database Migrations

```bash
# Initialize alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

## 🎯 Next Steps

1. Add MSSQL connection in `services/mssql_service.py`
2. Add real report generation logic
3. Add scheduled tasks with APScheduler
4. Add unit tests in `tests/`
5. Add Docker support
6. Add CI/CD pipeline

## 📖 Key Concepts

- **Models**: Database structure (SQLAlchemy)
- **Schemas**: Validation (Pydantic)
- **CRUD**: Database operations
- **Services**: Business logic
- **Middleware**: Request interceptors
- **Background Tasks**: Async processing

## 🤝 Contributing

This is a learning project. Feel free to modify and experiment!

## 📄 License

MIT