### ssl 용 도커 run

```
   sudo docker run -d \
            --name webserver \
            --memory=256m \
            --restart=always \
            -v $(pwd)/.webserver/default.conf:/etc/nginx/conf.d/default.conf \
            -v $(pwd)/.webserver/logs:/var/log/nginx \
            -v /etc/letsencrypt/archive:/cert \
            -p 80:80 \
            -p 443:443 \
            --network=django-network \
                nginx:latest
```
