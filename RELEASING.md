# Releasing TPPSR

- Check out the latest released version of lexibank/tppsr
- Recreate the database:
  ```shell script
  clld initdb --cldf ../tppsr-cldf/cldf/cldf-metadata.json development.ini
  ```
