
## Install and run

Run database on Docker

```bash
docker run --name testdb -e MYSQL_ROOT_PASSWORD=pass123 -e MYSQL_DATABASE=testdb -p 3306:3306 -d mysql:8.0
```
