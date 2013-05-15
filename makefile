prepare-index:
	echo "<html><head><title>Echo HTTP requests</title></head><body>" > index.html
	markdown README.md >> index.html
	echo "</body>" >> index.html 
start-server: prepare-index
	~/bin/google_appengine/old_dev_appserver.py .
deploy: prepare-index
	~/bin/google_appengine/appcfg.py -v update .
