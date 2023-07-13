SHELL := /bin/bash


client_local:
	@echo "Running client locally..."
	@python client_echo3_udp.py 127.0.0.1 1818

client_remote:
	@echo "Running client remotely..."
	@python client_echo3_udp.py anakena.dcc.uchile.cl 1818

server:
	@echo "Running server..."
	@python server_echo_udp3.py

pirate:
	@echo "Running pirate..."
	@python pirate_udp.py $(client_port) $(server_ip) 1818