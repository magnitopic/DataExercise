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

# Exercise aproach & methodology

The way this exercise was handeled was to first figure out the **database structure**, what **tables** and **relations** where needed. Next the needed data for those tables was extracted and **normalized**, for each of the tables we need there is a **Jupyter Notebook** that extracts, adds and creates the needed information for that table this is later **exported to a separate `CSV` file**. 

Once all the table files are exported we can use the [createDatabase.py](src/createDatabase.py) **python script** to **create the database** and then **populate it** with the information in the files.

## Process

Once in jupyter notebook, you can look at the diferent files in `src` in this order:

- [exploration.ipynb](src/exploration.ipynb)
- [clients.ipynb](src/clients.ipynb)
- [employees.ipynb](src/employees.ipynb)
- [transaction.ipynb](src/transaction.ipynb)
- [normalize.ipynb](src/normalize.ipynb)

If you run these files CVSs with the data to populate the database will be created in the `exports` folder

Finaly you can run the [createDatabase.py](src/createDatabase.py) file to create and populate the database with the CSV values.

## Result

Screenshot of data in `transaction` table

<img width="1032" height="743" alt="image" src="https://github.com/user-attachments/assets/f2e637ff-fa60-4e8e-a3ff-ac9d7ae16740" />

_A docker container with a sql database working and showing the values correctlly inserted in the `transaction` table_
