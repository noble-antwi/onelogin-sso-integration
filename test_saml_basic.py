"""
Basic test for SAML Handler functionality
"""
from config.settings import config
from src.saml_handler import SAMLHandler

print("Testing SAML Handler...")
print("=" * 40)

# Initialize SAML handler
saml_handler = SAMLHandler(config)

# Test 1: Generate SAML request
print("1. Generating SAML Request:")
request_id, encoded_request = saml_handler.generate_saml_request()
print(f"   Request ID: {request_id}")
print(f"   Request generated: {'✓' if encoded_request else '✗'}")
print(f"   Request length: {len(encoded_request)} characters")

# Test 2: Create demo session
print("\n2. Creating Demo User Session:")
demo_attributes = {
    "email": "test.user@example.com",
    "first_name": "Test",
    "last_name": "User",
    "user_id": "test_123",
    "department": "IT"
}

session_id = saml_handler.create_user_session(demo_attributes)
print(f"   Session ID: {session_id}")
print(f"   Session created: {'✓' if session_id else '✗'}")

# Test 3: Validate session
print("\n3. Validating Session:")
validation = saml_handler.validate_session(session_id)
print(f"   Session valid: {'✓' if validation['valid'] else '✗'}")
print(f"   User email: {validation.get('user_attributes', {}).get('email', 'N/A')}")

# Test 4: Get session statistics
print("\n4. Session Statistics:")
stats = saml_handler.get_session_stats()
print(f"   Active sessions: {stats['active_sessions']}")
print(f"   Total sessions: {stats['total_sessions']}")
print(f"   Success rate: {stats['success_rate']}%")

# Test 5: Logout user
print("\n5. Testing Logout:")
logout_success = saml_handler.logout_user(session_id)
print(f"   Logout successful: {'✓' if logout_success else '✗'}")

# Verify logout
final_validation = saml_handler.validate_session(session_id)
print(f"   Session invalidated: {'✓' if not final_validation['valid'] else '✗'}")

print("\n" + "=" * 40)
print("SAML Handler Test Complete!")