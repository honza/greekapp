cat greekapp/static/base.js greekapp/static/ajax.js greekapp/static/models.js greekapp/static/views.js greekapp/static/app.js > tmp.js 
uglifyjs tmp.js > greekapp/static/greekapp.min.js
cp greekapp/static/greekapp.min.js app.js
rm tmp.js
