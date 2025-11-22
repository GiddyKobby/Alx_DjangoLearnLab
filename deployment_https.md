# HTTPS Deployment Notes

To enable HTTPS in production:

1. Install SSL/TLS certificates
   - If using Nginx:
     sudo certbot --nginx -d yourdomain.com

   - If using Apache:
     sudo certbot --apache -d yourdomain.com

2. Nginx configuration example:

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

3. Ensure Django reads proxy headers:
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
