# Digital Equb - Rotating Savings & Credit Association (ROSCA) Platform

![Equb Logo](https://via.placeholder.com/150x50?text=Digital+Equb) *(optional logo)*

A Django REST API backend for managing digital rotating savings groups (Equb/Ekub), with features for group management, payment tracking, and automated payout rotation.

## ✨ Key Features

- **JWT Authentication** - Secure user registration/login
- **Equb Group Management** - Create, join, and manage savings groups
- **Payment Simulation** - Mock payment processing with success/failure states
- **Automated Payouts** - Round-robin distribution of collected funds
- **Swagger Documentation** - Interactive API documentation
- **WebSocket Notifications** - Real-time payout alerts

## 🛠️ Technology Stack

- **Backend**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT with refresh tokens
- **API Docs**: drf-yasg (Swagger/OpenAPI)
- **Real-Time**: Django Channels (WebSockets)

## 🚀 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (for WebSockets)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/digital-equb.git
   cd digital-equb


  python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install dependencies:
pip install -r requirements.txt

Configure environment:
cp .env.sample .env

Project Structure
text
digital-equb/
├── core/               # Django project config
├── users/              # User management app
├── groups/             # Equb group logic
├── payments/           # Payment processing

🌐 API Endpoints
Endpoint	Method	Description
/api/v1/auth/register/	POST	User registration
/api/v1/auth/login/	POST	User login (JWT tokens)
/api/v1/groups/	POST	Create new Equb group
/api/v1/groups/{id}/pay/	POST	Submit payment
/api/v1/groups/{id}/rotate/	POST	Trigger payout rotation
/swagger/	GET	Interactive API documentation

Documentation
API Docs: Access Swagger UI at http://localhost:8000/swagger/
