# My First Docker Container

## Commands used

```bash
docker pull nginx:alpine
docker images nginx
docker run -d --name first-nginx -p 8080:80 nginx:alpine
docker ps
curl http://localhost:8080
docker exec -it first-nginx sh
exit
docker logs first-nginx
docker stop first-nginx
docker ps
docker ps -a
docker rm first-nginx
docker ps -a
docker images nginx
```

## Observations

1. The image is the template, while the container is its running instance.
2. Inside the container, I found a Linux file system and the Nginx files.
3. The logs showed my `curl` request with status code `200`.
