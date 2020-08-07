def test_home(app):
    app.get_html('/', status=200)
    app.get_html('/parameters/2')
    app.get_dt('/parameters')
    app.get_html('/languages')
    app.get_html('/languages/3')
    app.get_json('/languages.geojson')
    app.get_dt('/values?parameter=2')
    app.get_dt('/values?language=2')
