import sys
sys.path.insert(0, "/var/www/MarketEdgePros/backend")

def extract_token_from_cookies(response, token_name="access_token"):
    cookies = response.headers.getlist("Set-Cookie")
    for cookie in cookies:
        if cookie.startswith(f"{token_name}="):
            token_part = cookie.split(";")[0]
            token_value = token_part.split("=", 1)[1]
            return token_value
    return None

def test_cookie_extraction():
    from src.app import create_app
    from src.models import User
    from src.database import db
    
    app = create_app("testing")
    
    with app.app_context():
        user = User(
            email="cookie_test@example.com",
            first_name="Cookie",
            last_name="Test",
            role="trader"
        )
        user.set_password("Test123!@#")
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        
        with app.test_client() as client:
            response = client.post("/api/auth/login", json={
                "email": "cookie_test@example.com",
                "password": "Test123!@#"
            })
            
            print(f"Status Code: {response.status_code}")
            print(f"Response JSON: {response.get_json()}")
            print("\nCookies in response:")
            for cookie in response.headers.getlist("Set-Cookie"):
                print(f"  {cookie[:100]}...")
            
            access_token = extract_token_from_cookies(response, "access_token")
            refresh_token = extract_token_from_cookies(response, "refresh_token")
            
            if access_token:
                print(f"\nExtracted access_token: {access_token[:50]}...")
            if refresh_token:
                print(f"Extracted refresh_token: {refresh_token[:50]}...")
            
            if access_token and refresh_token:
                print("\n✅ SUCCESS: Tokens extracted from cookies!")
                result = True
            else:
                print("\n❌ FAILED: Could not extract tokens from cookies")
                result = False
        
        db.session.delete(user)
        db.session.commit()
        return result

if __name__ == "__main__":
    success = test_cookie_extraction()
    sys.exit(0 if success else 1)
