Kompilacja

gcc serwer.C -o server -lssl -lcrypto -pthread


dla klienta, wystarczy użyć "pip install <nazwa>" dla odpowiednich modułów (pygame...) znajdujących się na początku pliku, aby je zainstalować, a potem użyć polecenia

python <hostname> <port> 

gdzie domyślny port dla załączonego serwera to 1234