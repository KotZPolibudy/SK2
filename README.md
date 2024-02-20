# Sieci komputerowe 2 - projekt zaliczeniowy
Gra Warcaby - serwer obsługujący zdalne połączenia od klientów,
dobieranie ich w pary i przeprowadzenie rozgrywki w warcaby.

# Kompilacja i uruchamianie

dla serwera, należy użyć:

gcc serwer.C -o server -lssl -lcrypto -pthread


dla klienta, wystarczy użyć "pip install nazwa" dla odpowiednich modułów (pygame...) znajdujących się na początku pliku, aby je zainstalować, a potem użyć polecenia

python warcabyklient.py hostname port 

gdzie domyślny port dla załączonego serwera to 1234

# Zasada działania - plan
Serwer - pisany w C, pod system linux
- Serwer odbiera od klienta informacje o gotowości do gry
- Kiedy otrzyma informacje o drugim gotowym graczu, łączy ich w parę i rozpoczyna między nimi grę,
oraz przechodzi do nasłuchiwania o kolejnych graczach
- Gra od strony serwera jest obsługiwana poprzez:
- - nadanie graczom kolorów
- - przesyłanie naprzemiennie ruchu gracza białego i czarnego, aż do wykrycia końca stanu gry przez jednego gracza
- - zakończenie gry i przesłanie informacji o wygranej/przegranej gracza


Klient - pisany w języku python, zapewniający GUI
- klient automatycznie łączy się z serwerem oczekując na sparowanie do gry 
- klient odczytuje ruch użytkownika z obsługi GUI
- weryfikuje poprawność ruchu
- wysyła ruch do serwera
- odczytuje od serwera wiadomość zwrotną (ruch przeciwnika)
- wyświetla użytkownikowi aktualny stan gry
- w przypadku wykrycia stanu końca gry przesyła informacje o tym do serwera


# Komunikacja
Do komunikacji został wykorzystany protokół TCP z szyfrowaniem za pomocą OpenSSL

# Info
Autor projektu:
- Wojciech Kot
- nr.indeksu 151879

# Funfact
Nazwa "warcaby" pochodzi od niemieckiego "Wurfzabel" co oznacza grę z użyciem kostek.

("Wurfel" - kostka "Wurfeln" - rzucać kostką)

A co do drugiej części, "zabel", to pierwsze skojarzenie to "Säbel", czyli szabla, 
więc żartobliwie można by nazwać warcaby kościanymi szablami,
albo rzucaniem szablą.

:) 