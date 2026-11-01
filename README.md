# Flask-Smorest REST API

A Flask REST API built with Flask-Smorest and JWT authentication.

### Features

* Product CRUD operations
* Categories and product relationships
* Pagination and sorting
* User registration
* JWT authentication and refresh tokens
* Role-based authorization
* Token revocation and logout
* Database migrations with Flask-Migrate
* Swagger UI and OpenAPI documentation
* Pytest authorization tests

## Database Tables

### Category

| Field | Type    | Description   |
| ------ | ------- | ------------- |
| `id`   | Integer | Primary key   |
| `name` | String  | Category name |

### Products

| Field        | Type    | Description                           |
| ------------- | ------- | ------------------------------------- |
| `id`          | Integer | Primary key                           |
| `name`        | String  | Product name                          |
| `description` | String  | Product description                   |
| `price`       | Float   | Product price                         |
| `qty`         | Integer | Available quantity                    |
| `category_id` | Integer | Foreign key referencing `category.id` |

### User

| Field     | Type    | Description                         |
| ---------- | ------- | ----------------------------------- |
| `id`       | Integer | Primary key                         |
| `name`     | String  | User's name                         |
| `username` | String  | Unique username                     |
| `password` | String  | Hashed password                     |
| `role`     | String  | User's role, used for authorization |


### Data Validation
Marshmallow schemas validate incoming request data and define the structure of API responses.

The API can reject invalid requests, including requests with missing required fields.

### Project Structure

```text
flask-smorest-rest-api/
├── app.py
├── models.py
├── routes.py
├── schemas.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── migrations/
│   ├── env.py
│   └── versions/
├── test/
│   ├── conftest.py
│   └── test_app.py
└── instance/
    └── products.db
```


### Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your configuration:

```env
DATABASE=sqlite:///database.db
JWT_SECRET_KEY=your-secret-key
```

Start the application:

```bash
python app.py
```

Swagger UI: `http://127.0.0.1:5000/swagger-ui`

Start here if you are a beginner [flask-smorest-rest-api-tutorial](https://github.com/xhimatty/flask-smorest-rest-api-tutorial)

