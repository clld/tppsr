# Releasing TPPSR

- Install from source:
  ```shell
  git clone https://github.com/clld/tppsr
  cd tppsr
  pip install -e .[test]
  ```
- Check out the latest released version of lexibank/tppsr
- Recreate the database:
  ```shell
  clld initdb --cldf ../tppsr-cldf/cldf/cldf-metadata.json development.ini
  ```
- make sure tests pass.
  ```shell
  pytest
  ```
- Store the tested requirements:
  ```shell
  pip freeze > requirements.txt
  ```
- Store a db dump:
  ```shell
  pg_dump -xO tppsr > tppsr.sql
  zip tppsr.sql.zip tppsr.sql
  rm tppsr.sql
  ```

