import urllib.request
import urllib.error
import json
import random
import string

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

email = f"test_{get_random_string()}@example.com"
password = "testpassword123"

print("1. Registering test user...")
register_payload = {
    "name": "Test",
    "lastname": "User",
    "email": email,
    "password": password
}
status, resp = make_request(f"{BASE_URL}/api/users/register", method="POST", data=register_payload)
print("Register Status:", status)
print("Register Response:", resp)
assert status == 201

print("\n2. Logging in...")
login_payload = {
    "email": email,
    "password": password
}
status, resp = make_request(f"{BASE_URL}/api/users/login", method="POST", data=login_payload)
print("Login Status:", status)
print("Login Response:", resp)
assert status == 200
token = resp["token"]

headers = {
    "Authorization": f"Bearer {token}"
}

print("\n3. Creating a new category...")
category_payload = {
    "name": "Test Cat " + get_random_string(),
    "type": "expense"
}
status, resp = make_request(f"{BASE_URL}/api/categories", method="POST", data=category_payload, headers=headers)
print("Create Cat Status:", status)
print("Create Cat Response:", resp)
assert status == 201

# Get the category list to find the ID of the created category
status, resp = make_request(f"{BASE_URL}/api/categories", method="GET", headers=headers)
cats = resp
cat_id = None
for c in cats:
    if c["name"] == category_payload["name"]:
        cat_id = c["id"]
        break

print(f"Found created category ID: {cat_id}")
assert cat_id is not None

print("\n4. Deleting the category without movements (should succeed)...")
status, resp = make_request(f"{BASE_URL}/api/categories/{cat_id}", method="DELETE", headers=headers)
print("Delete Cat Status:", status)
print("Delete Cat Response:", resp)
assert status == 200
assert resp["message"] == "Categoría eliminada correctamente."

print("\n5. Creating the category again...")
status, resp = make_request(f"{BASE_URL}/api/categories", method="POST", data=category_payload, headers=headers)
assert status == 201

status, resp = make_request(f"{BASE_URL}/api/categories", method="GET", headers=headers)
cat_id2 = None
for c in resp:
    if c["name"] == category_payload["name"]:
        cat_id2 = c["id"]
        break
print(f"New Category ID: {cat_id2}")
assert cat_id2 is not None

print("\n6. Creating a movement associated with the category...")
movement_payload = {
    "description": "Test Mov",
    "amount": 100.50,
    "movement_date": "2026-07-08",
    "category_id": cat_id2
}
status, resp = make_request(f"{BASE_URL}/api/movements", method="POST", data=movement_payload, headers=headers)
print("Create Movement Status:", status)
print("Create Movement Response:", resp)
assert status == 201
movement_id = resp["movement_id"]

print("\n7. Attempting to delete the category with movements (should fail with 409 Conflict)...")
status, resp = make_request(f"{BASE_URL}/api/categories/{cat_id2}", method="DELETE", headers=headers)
print("Delete Fail Status (Expected 409):", status)
print("Delete Fail Response:", resp)
assert status == 409
assert resp["message"] == "No se puede eliminar la categoría porque tiene movimientos asociados."

print("\n8. Deleting the movement...")
status, resp = make_request(f"{BASE_URL}/api/movements/{movement_id}", method="DELETE", headers=headers)
print("Delete Mov Status:", status)
assert status == 200

print("\n9. Deleting the category again (should now succeed)...")
status, resp = make_request(f"{BASE_URL}/api/categories/{cat_id2}", method="DELETE", headers=headers)
print("Delete Success Status:", status)
print("Delete Success Response:", resp)
assert status == 200
assert resp["message"] == "Categoría eliminada correctamente."

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
