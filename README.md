Wprowadzenie

Klasy:

**Klasa Vertex** - Okresla wierzchołek grafu i zawiera w sobie nazwe
przystanku i średnią szerokosc geograficzna np.

Vertex(\"Stalowa\",10.12212,11.1122)

**Klasa Edge** - Okresla polaczenie miedzy dwoma wierzcholkami i zawiera
w sobie nr linii, czas wyjazdu i czas przyjazdu na przystanek. np.
Edge(15:00:00,15:01:00,A)

**Klsa Graph**- Laczy w sobie wierzcholki i krawedzie w nastepujacy
sposob V1: \[(V2,E),\...\...\], jest to słownik ktory jako klucz posiada
nazwe przystanku a jako wartosc, liste krotek z przystankiem do ktorego
mozemy sie dostac i jakim polaczeniem(krawedzia) E. Warto podkreslic, ze
V1,V2 sa to wartosci typu STRING, a do ich odszyfrowania jako klasa
Vertex jest kolejny slownic Vertexes. Zdecydowalem sie na takie
rozwiazanie poniewaz nieczesto siegam do klasy vertex.

**Klasa PriorityQueue** - jest to implementacja kolejki priorytetowej
opartej o sterte.

Metody warte opisania

**Graph.getVertexLines(self,stop,time)**: - jest to metoda zwracajaca
linie ktore dojezdzaja do podanego przystanku (stop), po podanej
godzinie (time). Jest ona uzyta do funkcji heurystycznej przy kryterium
przesiadek w algorytmie A\*.

**Graph.getDeparturesAfterTime(self,time,stop)** - jest to metoda
zwracajaca wszystkie polaczenia z podanego przystanku (stop) po
okreslonym czasie (time).

**def calculate_b_star(N, d)** -- funkcja zwraca efektywny wspolczynnik
rozgalezienia obliczany metoda numetyczna ze wzoru:

N = 1 + b\* + (b\*)\^2 + \... + (b\*)\^d

**decode_path(came_from, goal, start, DEPTH, NODES)** - Funkcja
odczytujaca droge, jak i wyswietlajaca najwazniejsze dane dotyczace
trasy. Bedzie potrzebna w tworzeniu analizy danych otrzymanych wynikow.

zwraca:

> **path** - droge w postaci tablicy przystankow i czasow
>
> **path_df** - obiekt typu Pandas.DataFrame zawierajacy najwazniejsze
> informacje w srodku.
>
> **len(changes)** - ilosc przesiadek
>
> **time_diff** - czas trwania przejazdu
>
> **DEPTH** - glebokosc drzewa
>
> **NODES** - ilosc odwiedzonych wierzcholkow

Zadania

Algorytm Dijkstra

Algorytm dijkstry z kryterium czasu. Jako funkcje kosztu biore czas,
ktory potrzebujemy aby dostac sie z przystanku START to przystanku
biezacego. Jako priorytet biore wartosc funkcji kosztu. Najwieksza
trudnosc we wszystkich etapach to bylo przygotowanie czasu. Dodanie
sekund zamiana z powrotem na godzine.

A\* kryterium czasu

Algorytm A\* z kryterium czasu. Jako funkcje kosztu jak w algorytmie
Dijkstry wzialem czas potrzebny aby dostac sie z przystanku START do
przystanku biezacego. Roznica jest w postaci heurystyki, ktora dodajemy
do prioryteru. Funkcja time_heuristic zwraca odleglosc Manhattan,
pomnozona przez 10000 aby wynik byl bardziej wyskalowany oraz dawal
lepsze poczucie zmierzania do celu.

Wyznaczony za pomocą prob i bledow.

Algorytm A\* z kryterium przesiadek

rozni sie od poprzednika tym, ze:

1\. Funkcja heurystyczna jest oparta na podstawie przesiadek.
Przedstawilem to w postaci- jesli linia dojezdza bezposrednio do celu
nie dodaje sie kary

2\. Jesli wzgledem poprzedniego przystanku zmienilismy linie dostajemy
wiekszy koszt.

3\. Do kosztu wliczamy liczbe przesiadek pkt.2 oraz przeskalowany czas.
(wspolczynnik skalowania znaleziony na podstawie petli for i patrzeniu
na optymalny stosunek przesiadek do czasu trwania przejazdu)

4\. parametr N- wspolczynnik skalowania czasu pkt.3

Optymalizacja algorytmu A\*

do oprymalizacji czasu pracy algorytmu uzywam:

1\. Kolejki priorytetowej opartej na stercie

2\. Przy przeszukiwaniu wezlow biore tylko te ktore maja czas \> od
podanego

3\. Wyznaczone współczynniki optymalne dla heurystyki.

Opracowanie wyników

Puściłem algorytmy w pętli 100 razy, aby zobaczyć czy algorytm jest

Stabilny -- wyszukuje ciągle te same ścieżki i nie ma losowości.

Optymalny -- czy współczynnik rozgałęzienia jest wystarczająco niski.

Szybki -- czy czas pracy algorytmu jest zadowalający i różni się między
algorytmami

Tak prezentują się wyniki dla danych początkowych:

start = \'OPORÓW\'\
goal = \'Kasprowicza\'\
time = \'11:00:00\'

![Graphical user interface Description automatically generated with low
confidence](media/image1.png){width="4.652777777777778in"
height="4.694444444444445in"}

Do wstępnego przejrzenia wyników użyłem funkcji wbudowanej w pandas
DF.describe()

Jak widać, że:

1\. Każdy algorytm jest stabilny ponieważ wyszukuje za każdym razem tą
samą ścieżkę

2\. Dla wariantu przesiadek wyszukał aż o 3 przesiadki mniej i tylko 3
min dłuższą trasę.

3\. Rozgałęzienie wszystkich algorytmów jest bliskie 1 więc jest to
bardzo dobry wynik, dla A\* w wariancie przesiadek jest najmniejszy
ponieważ algorytm stara się podażać tylko jedną linią. Dla Dijkstry
dochodzi głębiej, a w wariancie czasowym płycej.

4\. Algorytm A\* jest [zdecydowanie]{.underline} szybszy od swoich
konkurentów, co może oznaczać, że heurystyka i skala jest dobrze
dobrana.

Kolejny przykład dla danych:

start = \'OPORÓW\'

goal = \'BISKUPIN\'

time = \'17:00:00\'

![Graphical user interface Description automatically generated with low
confidence](media/image2.png){width="4.597222222222222in"
height="4.597222222222222in"}

Potwierdzają się wszystkie poprzednie obserwacje, teraz nawet jeszcze
bardziej widać, że A\* w wariancie czasowym jest zdecydowanie szybszy
niż Dijkstra, ale za to bardzo podobny do swojego odpowiednika z
przesiadkami.

Przykładowa droga dla algorytmu A\*

z przesiadkami:

![Graphical user interface Description automatically generated with low
confidence](media/image3.png){width="2.8354166666666667in"
height="3.8610968941382326in"}

Przykładowa droga dla algorytmu A\* z kryterium czasu:

![A picture containing text Description automatically
generated](media/image4.png){width="2.8360662729658794in"
height="3.333179133858268in"}
