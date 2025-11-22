# LibraryProject

This is a basic Django project created for the ALX Django Learn Lab.  
It demonstrates how to set up a Django environment and run the development server.

# Security Review Summary

1. HTTPS Enforcement
   - SECURE_SSL_REDIRECT forces all HTTP traffic to HTTPS.
   - HSTS (SECURE_HSTS_SECONDS, INCLUDE_SUBDOMAINS, PRELOAD) prevents accidental insecure requests.

2. Cookie Security
   - SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE ensure cookies are only sent via HTTPS.
   - SameSite cookies help mitigate CSRF attacks.

3. Secure Headers
   - X_FRAME_OPTIONS="DENY" protects against clickjacking.
   - SECURE_BROWSER_XSS_FILTER enables browser-level XSS protection.
   - SECURE_CONTENT_TYPE_NOSNIFF prevents MIME sniffing vulnerabilities.

4. Additional Notes
   - CSRF tokens are added to forms for CSRF protection.
   - Django ORM is used to prevent SQL injection.
