cat greekapp/nt/static/base.js greekapp/nt/static/ajax.js greekapp/nt/static/models.js greekapp/nt/static/views.js greekapp/nt/static/app.js > tmp.js 
uglifyjs tmp.js > greekapp/nt/static/app.min.js
cp greekapp/nt/static/app.min.js app.js
