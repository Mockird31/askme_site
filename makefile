MAIN_CMD := gunicorn
GUNICORN_SCRIPT := askme_inyakin/gunicorn.conf.py
MAIN_APP := askme_inyakin.wsgi:my_application
NGINX := nginx
BREW := brew
DOCKER := docker
MEMCACHED := memcached

.PHONY: run
run:
	make run_centrifugo
	make run_memcached
	$(MAIN_CMD) -c $(GUNICORN_SCRIPT) $(MAIN_APP)

.PHONY: run_server
run_server:
	$(MAIN_CMD) -c $(GUNICORN_SCRIPT) $(MAIN_APP)

.PHONY: check_syntax_nginx
check_nginx:
	$(NGINX) -t

.PHONY: restart
restart_nginx:
	$(BREW) services restart $(NGINX)

.PHONY: info
info: 
	$(BREW) services info $(NGINX)

.PHONY: env
env:
	source project_env/bin/activate

.PHONY: errlog
errlog:
	tail -f /opt/homebrew/var/log/nginx/askme_inyakin_error.log

.PHONY: run_centrifugo
run_centrifugo:
	$(DOCKER) run -d --rm --ulimit nofile=262144:262144 -v $(PWD)/centrifugo:/centrifugo -p 8010:8000 centrifugo/centrifugo:v5 centrifugo -c config.json

.PHONY: stop_centrifugo	
stop_centrifugo:
	$(DOCKER) stop $(shell $(DOCKER) ps -q)

.PHONY: run_memcached
run_memcached:
	$(BREW) services start $(MEMCACHED)

.PHONY: stop_memcached
stop_memcached:
	$(BREW) services stop $(MEMCACHED)

.PHONY: clean
clean:
	$(RM) -r askme_inyakin/__pycache__
	$(RM) -r app/__pycache__
	$(RM) -r __pycache__
	sudo $(RM) -rf nginx_cache/*

.PHONY: get_info
get_info:
	$(BREW) services info $(NGINX)
	$(BREW) services info $(MEMCACHED)