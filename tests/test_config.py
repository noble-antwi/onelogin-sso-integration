from config.settings import config

# Test configuration
print("Configuration Status:")
print("-" * 30)

validation = config.validate_config()
for key, status in validation.items():
    print(f"{key}: {'✓' if status else '✗'}")

print(f"\nOneLogin configured: {config.is_configured()}")
print(f"Enabled applications: {len(config.get_enabled_applications())}")