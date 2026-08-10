## Swagger OAuth2

The frontend uses JSON-based authentication:

POST /api/v1/auth/login

{
  "email": "...",
  "password": "..."
}

Swagger's OAuth2 "Authorize" dialog expects
OAuth2PasswordRequestForm (username/password form data).

Therefore the built-in Authorize button is not functional.

This does not affect the frontend application.