# Data exercise

## Modelo entidad relación

![mer](img/modelo_entidad_relacion.png)

## Modelo relacional

![mr](img/modelo_relacional.png)


## Install and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run jupyter notebook to see the data treatment

```bash
jupyter lab
```

Run database on Docker

```bash
docker run --name testdb -e MYSQL_ROOT_PASSWORD=pass123 -e MYSQL_DATABASE=testdb -p 3306:3306 -d mysql:8.0
```

Run database population script

```bash
python src/createDatabase.py
```

## Result

Screenshot of data in `transaction` table

<img width="1032" height="743" alt="image" src="https://github.com/user-attachments/assets/f2e637ff-fa60-4e8e-a3ff-ac9d7ae16740" />
