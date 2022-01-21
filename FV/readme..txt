Il plugin di SWPI lancia il comando addcron.sh:
	- riscrive il file crontab
	- riavvia il serviio crontab

Tramite crontab ogni 3 minuti viene eseguito il comando vedirect.sh:
	- legge il consumo di corrente ads758.py
	- legge la produzione di energia:
		- vedirect1.py
		- vedirect2.py