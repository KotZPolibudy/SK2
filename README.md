# Sieci komputerowe 2 - projekt zaliczeniowy
Gra Warcaby - serwer obsługujący zdalne połączenia od klientów,
dobiera ich w pary i pozwala przeprowadzić rozgrywkę w warcaby.

# Funfact
Nazwa "warcaby" pochodzi od niemieckiego "Wurfzabel" co oznacza grę z użyciem kostek.

("Wurfel" - kostka "Wurfeln" - rzucać kostką)

A co do drugiej części, "zabel", to prawie "Säbel", czyli szabla, 
więc żartobliwie można by nazwać warcaby kościanymi szablami,
albo rzucaniem szablą.

:) 

# Zasada działania - plan
Serwer - pisany w C, pod system linux
- Serwer odbiera od klienta ruch
- sprawdza jego poprawność (w tym, czy jest to tura tego gracza)
- jeśli ruch jest poprawny, odsyła informacje zwrotne o wykonaniu poprawnego ruchu do obu graczy
- w przeciwnym wypadku zwraca klientowi, który próbował wykonać nielegalne posunięcie, prośbę o powtórzenie ruchu
- serwer wysyła do obu graczy zaktualizowany stan gry
- sprawdza warunki zakończenia gry
- przechodzi do realizacji tury drugiego gracza


Klient - pisany w języku python, zapewniający GUI
- klient odczytuje ruch użytkownika z obsługi GUI
- wysyła ruch do serwera
- odczytuje od serwera wiadomość zwrotną
- odczytuje od serwera aktualny stan gry i wyświetla go użytkownikowi

# Info
Autor projektu:
- Wojciech Kot
- nr.indeksu 151879