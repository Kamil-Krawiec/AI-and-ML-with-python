% Fakty

problem(
    czynnik(wirowanie),
    'Brak odprowadzania wody i/lub wirowania',
    problem_z(odprowadznie_wody)
    ).
problem(
    czynnik(wirowanie),
    'Halas podczas widowania/czasu pracy. Nadmierne drgania',
    problem_z(halas)
    ).
problem(
    czynnik(drzwi),
    'Drzwi urzadzenia nie otwieraja sie',
    problem_z(otwieranie_drzwi)
    ).
problem(
    czynnik(silnik),
    'Pralka buczy/wydaje dziwne dzwieki.',
    problem_z(odglosy)
).


przyczyna(
    czynnik(silnik),
    dotyczy(silnik),
    'Silnik może emitować hałas podczas normalnej pracy.',
    problem_z(odglosy)
).
przyczyna(
    czynnik(drzwi),
    dotyczy(drzwi),
    'Drzwi otwieraja sie dopiero po 3min od zakonczenia programu',
    problem_z(otwieranie_drzwi)
    ).
przyczyna(
    czynnik(drzwi),
    dotyczy(beben),
    'Woda pozostala w bebnie',
    problem_z(otwieranie_drzwi)
    ).
przyczyna(
    czynnik(wirowanie),
    dotyczy(waz),
    'Waz odplywowy może byc zaplatany/skrecony',
    problem_z(odprowadznie_wody)
    ).
przyczyna(
    czynnik(wirowanie),
    dotyczy(filtr),
    'Filtr zanieczyszczen jest zapchany',
    problem_z(odprowadznie_wody)
    ).
przyczyna(
    czynnik(wirowanie),
    dotyczy(waz),
    'Waz jest nieprawidlowo podlaczony do odplywu/doplywu',
    problem_z(odprowadznie_wody)
    ).[]
przyczyna(
    czynnik(wirowanie),
    dotyczy(beben),
    'W kieszeniach ciuchow wystepuja przedmioty, np. monety',
    problem_z(halas)
    ).
przyczyna(
    czynnik(wirowanie),
    dotyczy(czynnik_zewnetrzny),
    'Pralka stoi na nierownej podlodze',
    problem_z(halas)
    ).

rozwiazanie(
    czynnik(wirowanie),
    dotyczy(waz),
    'Wyprostuj waz odplywowy',
    problem_z(odprowadznie_wody)
    ).
rozwiazanie(
    czynnik(wirowanie),
    dotyczy(filtr),
    'Wyczysc filtr z zanieczyszczen'
    ,problem_z(odprowadznie_wody)
    ).
rozwiazanie(
    czynnik(wirowanie),
    dotyczy(waz),
    'Sprawdz podlaczenie weza'
    ,problem_z(odprowadznie_wody)
    ).
rozwiazanie(
    czynnik(wirowanie),
    dotyczy(beben),
    'Wyciagnij wszystkie przedmioty z kieszeni ciuchow.',
    problem_z(halas)
    ).
rozwiazanie(
    czynnik(wirowanie),
    dotyczy(czynnik_zewnetrzny),
    'Podnies/ureguluj stopki pralki',
    problem_z(halas)
    ).
rozwiazanie(
    czynnik(drzwi),
    dotyczy(drzwi),
    'Poczekaj 3min',
    problem_z(otwieranie_drzwi)
).
rozwiazanie(
    czynnik(drzwi),
    dotyczy(beben),
    'Oproznij beben i otworz drzwi recznie',
    problem_z(otwieranie_drzwi)
    ).
rozwiazanie(
    czynnik(silnik),
    dotyczy(silnik),
    'Normalnym jest, ze silnik pracuje zauwazalnie, jesli ma Pan/Pani obawy, prosze zadzownic na infolinie',
    problem_z(odglosy)
).

% Reguły

wyswietl_liste([]).
wyswietl_liste([Head|Tail]) :-
    format('\'~w\'',[Head]),nl,
    wyswietl_liste(Tail).

mozliwe_problemy_z(Czynnik) :-
    findall(Opis_problemu, problem(czynnik(Czynnik), Opis_problemu,_), ListaProblemow),
    nl,write('Czy twoim problemem jest: '),nl,
    wyswietl_liste(ListaProblemow),
    write('?'),nl.

powody_problemu(Opis_problemu) :-
    problem(_,Opis_problemu,Problem_Z),
    nl,write('Twoj problem moze powodowac: '),nl,
    findall(Opis_przyczyny, przyczyna(_,_,Opis_przyczyny,Problem_Z), ListaPrzyczyn),
    wyswietl_liste(ListaPrzyczyn).

rozwiazanie_problemu(Opis_przyczyny):-
    przyczyna(Czynnik,Dotyczy,Opis_przyczyny,Problem_z),
    rozwiazanie(Czynnik,Dotyczy,Opis_rozwiazania,Problem_z),
    format('Wszystko jasne, twoj problem dotyczy \'~w\' i problem lezy w \'~w\', musisz \'~w\'.',[Czynnik,Dotyczy,Opis_rozwiazania]).

poprowadz_mnie_przez_proces :-
    write('Mam problem z: '),
    read(X),
    mozliwe_problemy(X),
    write('Tak moim problem jest: '),
    read(Y), 
    powody_problemu(Y),
    write('Chce wiedziec jak rozwiazac przyczyne: '),
    read(Z), 
    rozwiazanie_problemu(Z).

z_czym_moge_miec_problem :-
    write('Twoj problem moze byc zwiazany z: '),
    findall([X,Y], problem(czynnik(X),_,problem_z(Y)), ListaCzynnikow),nl,
    write('[Czynnik z ktorym jest problem, Problemem jest]'),nl,
    wyswietl_liste(ListaCzynnikow).

czesci_z_ktorymi_moge_miec_problem:-
    write('Twoj problem moze byc zwiazany z czescia: '),
    findall(X, przyczyna(_,dotyczy(X),_,_), ListaPrzyczyn),nl,
    wyswietl_liste(ListaPrzyczyn).

mam_problem_z_czescia(Czesc):-
    przyczyna(Czynnik,dotyczy(Czesc),Opis_przyczyny,Problem_Z),
    rozwiazanie(Czynnik,dotyczy(Czesc),Opis_rozwiazania,Problem_Z),
    problem(Czynnik,Opis_problemu,Problem_Z),
    write('Wyglada na to ze twoj problem to: '),nl,
    format('Opis problemu:~n ~w',[Opis_problemu]),nl,
    format('Opis przyczyny:~n ~w',[Opis_przyczyny]),nl,
    format('Jak rozwiazac:~n ~w',[Opis_rozwiazania]),nl.