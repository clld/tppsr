# Releasing TPPSR

- Check out the latest released version of lexibank/tppsr
- Recreate the database:
  ```shell script
  clld initdb --cldf ../tppsr-data/cldf/cldf-metadata.json development.ini
  ```
