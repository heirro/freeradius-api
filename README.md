# FreeRADIUS API

A modern RESTful API built with FastAPI for managing FreeRADIUS database operations. This API provides comprehensive endpoints for managing RADIUS users, NAS (Network Access Server) devices, accounting records, and group configurations.

## 🚀 Features

- **User Management**: Complete CRUD operations for RADIUS users (radcheck table)
- **NAS Management**: Manage Network Access Server configurations
- **Accounting Records**: Query and monitor RADIUS accounting sessions (radacct)
- **Group Management**: Handle user groups, group checks, and group replies
- **User Status Tracking**: Real-time monitoring of online/offline user status
- **Authentication**: HTTP Basic Authentication for Swagger UI documentation
- **Database Support**: Compatible with MySQL, MariaDB, and PostgreSQL
- **Auto-generated Documentation**: Interactive Swagger UI and ReDoc
- **CORS Enabled**: Cross-Origin Resource Sharing support

## 📋 Requirements

- Python 3.8+
- MySQL/MariaDB or PostgreSQL database
- FreeRADIUS database schema

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd freeradius-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate

# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` file with your database credentials:

```env
# Application Settings
APP_NAME=freeradius-api
APP_DEBUG=True

# Swagger/BASIC Auth Credentials
SWAGGER_USERNAME=admin
SWAGGER_PASSWORD=radius

# Database Settings
DB_TYPE=mariadb
DB_HOST=localhost
DB_PORT=3306
DB_NAME=radius
DB_USER=radius
DB_PASSWORD=radpass
```

## 🚀 Running the Application

### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Production Mode with Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs` (requires authentication)
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` (requires authentication)

> **Note**: Documentation endpoints are protected with HTTP Basic Authentication using credentials from `.env` file.

## 🔌 API Endpoints

### Root
- `GET /` - Health check endpoint

### Users (RadCheck)
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{username}` - Get user by username
- `POST /api/v1/users` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### NAS (Network Access Server)
- `GET /api/v1/nas/` - Get all NAS devices (with optional filters)
- `GET /api/v1/nas/{nas_id}` - Get NAS by ID
- `POST /api/v1/nas/` - Create new NAS
- `PUT /api/v1/nas/{nas_id}` - Update NAS
- `DELETE /api/v1/nas/{nas_id}` - Delete NAS

### RADIUS Accounting (RadAcct)
- `GET /api/v1/radacct/` - Get accounting records (with filters)
- `GET /api/v1/radacct/{radacctid}` - Get specific accounting record
- `GET /api/v1/radacct/status/{username}` - Get user online/offline status

### User Groups (RadUserGroup)
- `GET /api/v1/radusergroup/` - Get all user-group mappings
- `GET /api/v1/radusergroup/{id}` - Get specific mapping
- `POST /api/v1/radusergroup/` - Create user-group mapping
- `PUT /api/v1/radusergroup/{id}` - Update mapping
- `DELETE /api/v1/radusergroup/{id}` - Delete mapping

### Group Check (RadGroupCheck)
- `GET /api/v1/radgroupcheck/` - Get all group check attributes
- `GET /api/v1/radgroupcheck/{id}` - Get specific group check
- `POST /api/v1/radgroupcheck/` - Create group check
- `PUT /api/v1/radgroupcheck/{id}` - Update group check
- `DELETE /api/v1/radgroupcheck/{id}` - Delete group check

### Group Reply (RadGroupReply)
- `GET /api/v1/radgroupreply/` - Get all group reply attributes
- `GET /api/v1/radgroupreply/{id}` - Get specific group reply
- `POST /api/v1/radgroupreply/` - Create group reply
- `PUT /api/v1/radgroupreply/{id}` - Update group reply
- `DELETE /api/v1/radgroupreply/{id}` - Delete group reply

### RADIUS Reply (RadReply)
- `GET /api/v1/radreply/` - Get all user reply attributes
- `GET /api/v1/radreply/{id}` - Get specific reply
- `POST /api/v1/radreply/` - Create reply
- `PUT /api/v1/radreply/{id}` - Update reply
- `DELETE /api/v1/radreply/{id}` - Delete reply

## 🗄️ Database Schema

The API interacts with the following FreeRADIUS tables:

### radcheck
Stores user authentication credentials and check attributes.

| Column    | Type         | Description                    |
|-----------|--------------|--------------------------------|
| id        | Integer      | Primary key                    |
| username  | String(64)   | RADIUS username                |
| attribute | String(64)   | Check attribute name           |
| op        | String(2)    | Operator (e.g., :=, ==)        |
| value     | String(253)  | Attribute value                |

### nas
Network Access Server configurations.

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | Integer      | Primary key                    |
| nasname     | String(128)  | NAS identifier/IP              |
| shortname   | String(32)   | Short name                     |
| type        | String(30)   | NAS type                       |
| ports       | Integer      | Number of ports                |
| secret      | String(60)   | RADIUS shared secret           |
| server      | String(64)   | Server address                 |
| community   | String(50)   | SNMP community                 |
| description | String(200)  | NAS description                |

### radacct
RADIUS accounting session records.

| Column            | Type         | Description                    |
|-------------------|--------------|--------------------------------|
| radacctid         | Integer      | Primary key                    |
| acctsessionid     | String(64)   | Session ID                     |
| username          | String(64)   | Username                       |
| nasipaddress      | String(15)   | NAS IP address                 |
| acctstarttime     | DateTime     | Session start time             |
| acctstoptime      | DateTime     | Session stop time              |
| acctsessiontime   | Integer      | Session duration (seconds)     |
| acctinputoctets   | Integer      | Input bytes                    |
| acctoutputoctets  | Integer      | Output bytes                   |
| framedipaddress   | String(15)   | User IP address                |

### radusergroup
Maps users to groups.

| Column    | Type         | Description                    |
|-----------|--------------|--------------------------------|
| id        | Integer      | Primary key                    |
| username  | String(64)   | Username                       |
| groupname | String(64)   | Group name                     |
| priority  | Integer      | Priority (default: 1)          |

### radgroupcheck
Group-level check attributes.

| Column    | Type         | Description                    |
|-----------|--------------|--------------------------------|
| id        | Integer      | Primary key                    |
| groupname | String(64)   | Group name                     |
| attribute | String(64)   | Check attribute                |
| op        | String(2)    | Operator                       |
| value     | String(253)  | Attribute value                |

### radgroupreply
Group-level reply attributes.

| Column    | Type         | Description                    |
|-----------|--------------|--------------------------------|
| id        | Integer      | Primary key                    |
| groupname | String(64)   | Group name                     |
| attribute | String(64)   | Reply attribute                |
| op        | String(2)    | Operator                       |
| value     | String(253)  | Attribute value                |

## 📖 Usage Examples

### Create a New User

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "attribute": "Cleartext-Password",
    "op": ":=",
    "value": "password123"
  }'
```

### Check User Status

```bash
curl -X GET "http://localhost:8000/api/v1/radacct/status/testuser"
```

### Add NAS Device

```bash
curl -X POST "http://localhost:8000/api/v1/nas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nasname": "192.168.1.1",
    "shortname": "router1",
    "type": "cisco",
    "ports": 1812,
    "secret": "sharedsecret",
    "description": "Main Router"
  }'
```

### Get Accounting Records

```bash
# Get all records
curl -X GET "http://localhost:8000/api/v1/radacct/"

# Filter by username
curl -X GET "http://localhost:8000/api/v1/radacct/?username=testuser"

# With pagination
curl -X GET "http://localhost:8000/api/v1/radacct/?skip=0&limit=50"
```

## 🏗️ Project Structure

```
freeradius-api/
├── __init__.py
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── src/
    ├── api/
    │   ├── __init__.py
    │   ├── api.py         # API utilities
    │   ├── endpoints/     # API route handlers
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── users.py
    │   │   ├── nas.py
    │   │   ├── radacct.py
    │   │   ├── radusergroup.py
    │   │   ├── radgroupcheck.py
    │   │   ├── radgroupreply.py
    │   │   └── radreply.py
    │   └── v1/
    │       └── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── config.py      # Configuration management
    ├── db/
    │   ├── __init__.py
    │   └── database.py    # Database connection
    ├── models/            # SQLAlchemy ORM models
    │   ├── __init__.py
    │   ├── user.py
    │   ├── operator.py
    │   ├── nas.py
    │   ├── radacct.py
    │   ├── radcheck.py
    │   ├── radgroupcheck.py
    │   ├── radgroupreply.py
    │   ├── radreply.py
    │   └── radusergroup.py
    ├── schemas/           # Pydantic schemas
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── user.py
    │   ├── operator.py
    │   ├── nas.py
    │   ├── radacct.py
    │   ├── radcheck.py
    │   ├── radgroupcheck.py
    │   ├── radgroupreply.py
    │   ├── radreply.py
    │   └── radusergroup.py
    ├── services/          # Business logic layer
    │   └── __init__.py
    └── utils/             # Utility functions
```

## 🔧 Configuration

### Database Connection Pool

The application uses SQLAlchemy with optimized connection pooling:

- **Pool Size**: 200 connections
- **Max Overflow**: 100 additional connections
- **Pool Timeout**: 600 seconds
- **Pool Recycle**: 3600 seconds (1 hour)
- **Pre-ping**: Enabled for connection health checks

### CORS Configuration

CORS is enabled for all origins by default. Modify in `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔒 Security

- Swagger UI and OpenAPI documentation are protected with HTTP Basic Authentication
- Configure strong credentials in `.env` file
- Use environment variables for sensitive data
- Never commit `.env` file to version control

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_users.py
```

## 📝 Dependencies

Key dependencies include:

- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **PyMySQL**: MySQL/MariaDB driver
- **psycopg2-binary**: PostgreSQL driver
- **python-dotenv**: Environment variable management
- **Uvicorn**: ASGI server
- **Alembic**: Database migrations

See `requirements.txt` for complete list.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Verify database credentials in `.env`
2. Ensure database server is running
3. Check firewall rules
4. Verify database exists and user has proper permissions

### Import Errors

If you get import errors:

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
uvicorn main:app --host 0.0.0.0 --port 8080
```

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Check existing documentation
- Review FreeRADIUS documentation for database schema questions

---

**Built with ❤️ using FastAPI and FreeRADIUS**
