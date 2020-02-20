REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [ 
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser", 
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": 
    [                              # new
        "rest_framework.authentication.SessionAuthentication",        # new
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # new 
        
    ],
} 