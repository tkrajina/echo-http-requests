start-server:
	~/bin/google_appengine_1.8.0/old_dev_appserver.py .
deploy:
	~/bin/google_appengine_1.8.0/appcfg.py update .
