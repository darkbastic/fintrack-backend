import urllib.request
import urllib.error
import json
import random
import string
import datetime

BASE_URL = "http://127.0.0.1:5000"

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    
    req_headers = {"Content-Type": "application/json"}
    req_headers.update(headers)
    
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        return status, json.loads(body) if body else {}

print("--- SECURITY TESTS ---")
# 1. Without token
status, resp = make_request(f"{BASE_URL}/api/dashboard", method="GET")
print("Without token status:", status)
assert status == 401
assert resp["message"] == "Token no proporcionado."

# 2. Invalid token
status, resp = make_request(f"{BASE_URL}/api/dashboard", method="GET", headers={"Authorization": "Bearer invalidtoken"})
print("Invalid token status:", status)
assert status == 401
assert resp["message"] == "Token inválido o expirado." or resp["message"] == "Token inválido."

print("\n--- REGISTRATION & LOGIN ---")
email = f"dash_{get_random_string()}@example.com"
password = "testpassword123"

# Register
status, resp = make_request(f"{BASE_URL}/api/users/register", method="POST", data={
    "name": "Dash",
    "lastname": "User",
    "email": email,
    "password": password
})
assert status == 201

# Login
status, resp = make_request(f"{BASE_URL}/api/users/login", method="POST", data={
    "email": email,
    "password": password
})
assert status == 200
token = resp["token"]
headers = {"Authorization": f"Bearer {token}"}

print("\n--- CASE 1: USER WITH NO MOVEMENTS ---")
status, resp = make_request(f"{BASE_URL}/api/dashboard", method="GET", headers=headers)
print("No movements status:", status)
print("No movements response:", json.dumps(resp, indent=2))
assert status == 200
assert resp["summary"]["balance"] == 0.0
assert resp["summary"]["income"] == 0.0
assert resp["summary"]["expense"] == 0.0
assert resp["summary"]["movements"] == 0
assert resp["last_movements"] == []
assert resp["expenses_by_category"] == []
assert resp["monthly_balance"]["balance"] == 0.0
assert resp["monthly_balance"]["income"] == 0.0
assert resp["monthly_balance"]["expense"] == 0.0

print("\n--- CREATING TEST CATEGORIES ---")
# Create categories
status, resp = make_request(f"{BASE_URL}/api/categories", method="POST", data={"name": "Salario", "type": "income"}, headers=headers)
assert status == 201
status, resp = make_request(f"{BASE_URL}/api/categories", method="POST", data={"name": "Comida", "type": "expense"}, headers=headers)
assert status == 201
status, resp = make_request(f"{BASE_URL}/api/categories", method="POST", data={"name": "Alquiler", "type": "expense"}, headers=headers)
assert status == 201

# Find category IDs
status, cats = make_request(f"{BASE_URL}/api/categories", method="GET", headers=headers)
cat_ids = {c["name"]: c["id"] for c in cats}
print("Category IDs:", cat_ids)

print("\n--- CREATING TEST MOVEMENTS ---")
today_str = datetime.date.today().strftime("%Y-%m-%d")
last_month = datetime.date.today() - datetime.timedelta(days=35)
last_month_str = last_month.strftime("%Y-%m-%d")

print("Today's Date (Current Month):", today_str)
print("Last Month's Date (Other Month):", last_month_str)

# 1. Income current month
status, resp = make_request(f"{BASE_URL}/api/movements", method="POST", data={
    "description": "Salario Julio",
    "amount": 2500.0,
    "movement_date": today_str,
    "category_id": cat_ids["Salario"]
}, headers=headers)
assert status == 201

# 2. Expense current month (Comida)
status, resp = make_request(f"{BASE_URL}/api/movements", method="POST", data={
    "description": "Supermercado",
    "amount": 150.0,
    "movement_date": today_str,
    "category_id": cat_ids["Comida"]
}, headers=headers)
assert status == 201

# 3. Expense current month (Alquiler)
status, resp = make_request(f"{BASE_URL}/api/movements", method="POST", data={
    "description": "Pago Departamento",
    "amount": 800.0,
    "movement_date": today_str,
    "category_id": cat_ids["Alquiler"]
}, headers=headers)
assert status == 201

# 4. Expense last month (Comida)
status, resp = make_request(f"{BASE_URL}/api/movements", method="POST", data={
    "description": "Restaurante mes pasado",
    "amount": 50.0,
    "movement_date": last_month_str,
    "category_id": cat_ids["Comida"]
}, headers=headers)
assert status == 201

print("\n--- CASE 2: USER WITH MOVEMENTS ---")
status, resp = make_request(f"{BASE_URL}/api/dashboard", method="GET", headers=headers)
print("With movements status:", status)
print("With movements response:", json.dumps(resp, indent=2))
assert status == 200

# Assert general summary
# Income: 2500.0
# Expense: 150.0 + 800.0 + 50.0 = 1000.0
# Balance: 2500.0 - 1000.0 = 1500.0
# Movements: 4
assert resp["summary"]["income"] == 2500.0
assert resp["summary"]["expense"] == 1000.0
assert resp["summary"]["balance"] == 1500.0
assert resp["summary"]["movements"] == 4

# Assert monthly balance
# Income (this month): 2500.0
# Expense (this month): 150.0 + 800.0 = 950.0
# Balance (this month): 2500.0 - 950.0 = 1550.0
assert resp["monthly_balance"]["income"] == 2500.0
assert resp["monthly_balance"]["expense"] == 950.0
assert resp["monthly_balance"]["balance"] == 1550.0

# Assert expenses by category
# Alquiler: 800.0
# Comida: 150.0 + 50.0 = 200.0
# Sorted by total desc: Alquiler first, then Comida
assert len(resp["expenses_by_category"]) == 2
assert resp["expenses_by_category"][0]["category"] == "Alquiler"
assert resp["expenses_by_category"][0]["total"] == 800.0
assert resp["expenses_by_category"][1]["category"] == "Comida"
assert resp["expenses_by_category"][1]["total"] == 200.0

# Assert last movements
# Should have 4 movements
assert len(resp["last_movements"]) == 4
# The first one should be "Restaurante mes pasado" or according to date ordering:
# Let's check date ordering: today's movements should be first.
# "Restaurante mes pasado" should be last.
assert resp["last_movements"][-1]["description"] == "Restaurante mes pasado"

print("\nALL DASHBOARD VERIFICATIONS PASSED SUCCESSFULLY!")
