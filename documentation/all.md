## Autorzy

Szymon Sadowski
Krzysztof Szczyrbak

##Temat

Analiza porównawcza metod tworzenia sieciowych interfejsów dostępu do zasobów

##Linki

Rozwijany przez nas kod źródłowy dostępny jest pod adresem: https://github.com/szymonsadowski3/StudioProjektowe2

##Opis
Celem projektu jest porównanie dwóch popularnych metod tworzenia sieciowych interfejsów
dostępu do danych (zasobów): GraphQL i REST.
Porównanie będzie polegało na zaimplementowaniu sieciowego modelu dostępu do zbioru
danych na dwa sposoby, korzystając z różnych metod optymalizacji, aby później podjąć
bezpośrednie porównanie obu rozwiązań według kilku wybranych kryteriów:

* złożoność kodu
* wydajność obliczeniowa
* możliwości modyfikacji
* łatwość integracji z warstwą prezentacji

Dla celów porównawczych w obu technologiach zostanie zaimplementowana przykładowa
aplikacja - proste forum dyskusyjne. Charakterystyczna dla forów dyskusyjnych
hierarchiczna struktura danych pozwoli na wyodrębnienie zalet i wad obu implementacji.


---

# Implementacja dostępu GraphQL

Zgodnie z harmonogramem tym razem zakończyliśmy implementację sieciowego interfejsu dostępu do danych **GraphQL**

## Model danych

W poprzednim punkcie harmonogramu zakończyliśmy implementację dostępu **REST**, w trakcie czego zbudowaliśmy bazę danych. Ostateczna struktura bazy danych została wylistowana poniżej w skrypcie SQL:

```sql
create table "user"
(
	id serial not null
		constraint user_pkey
			primary key,
	username varchar(255) not null,
	"createdOn" timestamp not null,
	avatar text,
	"aboutMe" text,
	signature text
)
;

create table thread
(
	id serial not null
		constraint thread_pkey
			primary key,
	title varchar(255) not null,
	"createdBy_id" integer not null
		constraint "thread_createdBy_id_fkey"
			references "user",
	"createdOn" timestamp not null
)
;

create index "thread_createdBy_id"
	on thread ("createdBy_id")
;

create table post
(
	id serial not null
		constraint post_pkey
			primary key,
	title varchar(255),
	post_content text not null,
	"createdOn" timestamp not null,
	"parentThread_id" integer not null
		constraint "post_parentThread_id_fkey"
			references thread
)
;

create index "post_parentThread_id"
	on post ("parentThread_id")
;

create table privatemessage
(
	id serial not null
		constraint privatemessage_pkey
			primary key,
	subject varchar(255),
	message_content text not null,
	"sentOn" timestamp not null,
	sender_id integer not null
		constraint privatemessage_sender_id_fkey
			references "user",
	receiver_id integer not null
		constraint privatemessage_receiver_id_fkey
			references "user"
)
;

create index privatemessage_sender_id
	on privatemessage (sender_id)
;

create index privatemessage_receiver_id
	on privatemessage (receiver_id)
;

create table section
(
	id serial not null
		constraint section_pkey
			primary key,
	name varchar(255) not null,
	section_logo text
)
;

create table threadfollowers
(
	id serial not null
		constraint threadfollowers_pkey
			primary key,
	thread_id integer not null
		constraint threadfollowers_thread_id_fkey
			references thread,
	user_id integer not null
		constraint threadfollowers_user_id_fkey
			references "user"
)
;

create index threadfollowers_thread_id
	on threadfollowers (thread_id)
;

create index threadfollowers_user_id
	on threadfollowers (user_id)
;

```

## Implementacja dostępu GraphQL

Aby zaimplementować dostęp GraphQL użyliśmy biblioteki **postgraphile** (https://www.graphile.org/postgraphile/). Jest ona wygodna w użyciu, ponieważ wystarczy skonfigurować połączenie do bazy danych, a narzędzie postgraphile na tej podstawie potrafi uruchomić interfejs GraphQL. Przykładowe uruchomienie biblioteki prezentuje się następująco:

```
postgraphile --cors -c postgres://postgres:postgres@localhost:5432/postgres
```

Po uruchomieniu tej komendy interfejs GraphQL będzie dostępny pod domyślnym adresem `http://localhost:5000/graphql` natomiast pod adresem `http://localhost:5000/graphiql` zostanie uruchomiony prosty interfejs użytkownika pozwalający na testowe uruchomienie zapytań i uzyskanie danych.

Na zrzucie ekranu poniżej umieszczono przykładowe zapytanie ukazujące zaletę GraphQL - w prosty sposób w zapytaniu wyspecyfikowano, że pobrane zostać powinny jedynie: identyfikator, tytuł oraz zawartość postu na forum:


![allPosts](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/queryAllPosts.PNG)

Treści postów zostały wygenerowane za pomocą biblioteki **faker** (https://github.com/joke2k/faker).
Na drugim zrzucie ekranu widoczne jest przykładowe zapytanie z parametrem (pobierany jest post z identyfikatorem 801):

![queryById](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/queryById.PNG)

---

# Implementacja REST

## Model danych

Zgodnie z harmonogramem zakończyliśmy implementację sieciowego interfejsu dostępu do danych **REST**

Do stworzenia modelu danych w bazie danych użyliśmy biblioteki **peewee** (http://docs.peewee-orm.com/en/latest/) tworząc następujące modele:

```py
class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pgdb


class Section(BaseModel):
    name = CharField()
    section_logo = TextField(null=True)


class User(BaseModel):
    username = CharField()
    createdOn = DateTimeField(default=datetime.datetime.now)
    avatar = TextField(null=True)
    aboutMe = TextField(null=True)
    signature = TextField(null=True)


class Thread(BaseModel):
    title = CharField()
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField(default=datetime.datetime.now)
    section = ForeignKeyField(Section)


class ThreadFollowers(BaseModel):
    thread = ForeignKeyField(Thread)
    user = ForeignKeyField(User)


class Post(BaseModel):
    title = CharField(null=True)
    post_content = TextField()
    createdOn = DateTimeField(default=datetime.datetime.now)
    parentThread = ForeignKeyField(Thread)


class PrivateMessage(BaseModel):
    subject = CharField(null=True)
    message_content = TextField()
    sentOn = DateTimeField(default=datetime.datetime.now)
    sender = ForeignKeyField(User)
    receiver = ForeignKeyField(User)
```

Po uruchomieniu aplikacji schemat w bazie danych przedstawiał się następująco

![model](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/model.PNG)

## Generowanie danych

Aby móc pracować z tak przygotowaną bazą danych użyliśmy biblioteki **faker** (https://github.com/joke2k/faker) to wygenerowania przykładowych rekordów w bazie danych

Po uruchomieniu skryptu tak wyglądała przykładowa porcja danych wygenerowana przez skrypt (na zrzucie ekranu poniżej widać wygenerowane prywatne wiadomości):

![faker](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/faker.PNG)

Mając tak przygotowaną bazę danych mogliśmy przystąpić do implementacji sieciowego interfejsu dostępu do danych **REST**

## Implementacja dostępu REST

Do implementacji dostępu REST użyliśmy biblioteki **flask** (https://palletsprojects.com/p/flask/). Biblioteka ta jest lekkim rozwiązaniem do tworzenia małych aplikacji sieciowych i szczególnie dobrze nadaje się do implementacji aplikacji REST-owych.

Dostęp do wszystkich modeli (wylistowane poniżej) zaimplementowaliśmy w podobny sposób.

1. Sekcja
2. Użytkownik
3. Temat
4. TematŚledzący
5. Post
6. Wiadomość Prywatna

Przykładowa implementacja dostępu do tematów została zaprezentowana poniżej.

```py
@app.route('/thread')
def get_threads():
    return handler_by_query(Thread.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/thread/<int:thread_id>')
def get_thread_by_id(thread_id):
    return handler_by_query(
        Thread.select().where(Thread.id == thread_id).paginate(get_int_arg('page'), get_int_arg('per_page'))
    )


@app.route('/thread/<int:thread_id>/followers')
def get_thread_followers_by_id(thread_id):
    return handler_by_query(
        User
        .select()
        .join(ThreadFollowers, on=(ThreadFollowers.user == User.id))
        .where(ThreadFollowers.thread == thread_id)
        .paginate(get_int_arg('page'), get_int_arg('per_page'))
    )
```

Zatem jak widać na powyższym przykładzie implementacja dostępu REST ograniczyła się do stworzenia odpowiednich zapytań do bazy danych uwzględniając rzeczy takie jak:

1. Paginacja (ograniczanie wyników zapytania) - nie chcemy bowiem przesyłać przez sieć całej zawartości tabeli, wystarczy jedynie porcja danych
2. Łączenie tabel (tzw. *joinowanie*) - gdyż chcemy uzyskać niektóre powiązane informacje, np. którzy użytkownicy śledzą dany temat
3. Filtrowanie - gdy przykładowo chcemy uzyskać dane dla konkretnego użytkownika

## Wnioski

Implementacja dostępu REST nie sprawiła dużego problemu. W takiej formie aplikacja jest łatwa do utrzymania i rozbudowy. 

W kolejnej części zaimplementujemy dostęp GraphQL

---

# Implementacja dostępu GraphQL

Zgodnie z harmonogramem tym razem zakończyliśmy implementację sieciowego interfejsu dostępu do danych **GraphQL**

## Model danych

W poprzednim punkcie harmonogramu zakończyliśmy implementację dostępu **REST**, w trakcie czego zbudowaliśmy bazę danych. Ostateczna struktura bazy danych została wylistowana poniżej w skrypcie SQL:

```sql
create table "user"
(
	id serial not null
		constraint user_pkey
			primary key,
	username varchar(255) not null,
	"createdOn" timestamp not null,
	avatar text,
	"aboutMe" text,
	signature text
)
;

create table thread
(
	id serial not null
		constraint thread_pkey
			primary key,
	title varchar(255) not null,
	"createdBy_id" integer not null
		constraint "thread_createdBy_id_fkey"
			references "user",
	"createdOn" timestamp not null
)
;

create index "thread_createdBy_id"
	on thread ("createdBy_id")
;

create table post
(
	id serial not null
		constraint post_pkey
			primary key,
	title varchar(255),
	post_content text not null,
	"createdOn" timestamp not null,
	"parentThread_id" integer not null
		constraint "post_parentThread_id_fkey"
			references thread
)
;

create index "post_parentThread_id"
	on post ("parentThread_id")
;

create table privatemessage
(
	id serial not null
		constraint privatemessage_pkey
			primary key,
	subject varchar(255),
	message_content text not null,
	"sentOn" timestamp not null,
	sender_id integer not null
		constraint privatemessage_sender_id_fkey
			references "user",
	receiver_id integer not null
		constraint privatemessage_receiver_id_fkey
			references "user"
)
;

create index privatemessage_sender_id
	on privatemessage (sender_id)
;

create index privatemessage_receiver_id
	on privatemessage (receiver_id)
;

create table section
(
	id serial not null
		constraint section_pkey
			primary key,
	name varchar(255) not null,
	section_logo text
)
;

create table threadfollowers
(
	id serial not null
		constraint threadfollowers_pkey
			primary key,
	thread_id integer not null
		constraint threadfollowers_thread_id_fkey
			references thread,
	user_id integer not null
		constraint threadfollowers_user_id_fkey
			references "user"
)
;

create index threadfollowers_thread_id
	on threadfollowers (thread_id)
;

create index threadfollowers_user_id
	on threadfollowers (user_id)
;

```

## Implementacja dostępu GraphQL

Aby zaimplementować dostęp GraphQL użyliśmy biblioteki **postgraphile** (https://www.graphile.org/postgraphile/). Jest ona wygodna w użyciu, ponieważ wystarczy skonfigurować połączenie do bazy danych, a narzędzie postgraphile na tej podstawie potrafi uruchomić interfejs GraphQL. Przykładowe uruchomienie biblioteki prezentuje się następująco:

```
postgraphile --cors -c postgres://postgres:postgres@localhost:5432/postgres
```

Po uruchomieniu tej komendy interfejs GraphQL będzie dostępny pod domyślnym adresem `http://localhost:5000/graphql` natomiast pod adresem `http://localhost:5000/graphiql` zostanie uruchomiony prosty interfejs użytkownika pozwalający na testowe uruchomienie zapytań i uzyskanie danych.

Na zrzucie ekranu poniżej umieszczono przykładowe zapytanie ukazujące zaletę GraphQL - w prosty sposób w zapytaniu wyspecyfikowano, że pobrane zostać powinny jedynie: identyfikator, tytuł oraz zawartość postu na forum:


![allPosts](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/queryAllPosts.PNG)

Treści postów zostały wygenerowane za pomocą biblioteki **faker** (https://github.com/joke2k/faker).
Na drugim zrzucie ekranu widoczne jest przykładowe zapytanie z parametrem (pobierany jest post z identyfikatorem 801):

![queryById](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/queryById.PNG)

---

# Porównanie pod względem wydajności

Zgodnie z harmonogramem tym razem przeprowadziliśmy porównanie interfejsów **Rest** i **GraphQL** biorąc pod uwagę kryterium wydajności

## Uruchomienie interfejsu **Rest** w warunkach produkcyjnych

Ponieważ interfejs **Rest** został zaimplementowany przez nas w bibliotece *flask*, aby porównanie było wiarygodne, musieliśmy znaleść sposób na uruchomienie serwera w warunkach wysokiej wydajności (mini-serwer domyślnie dołączony do biblioteki *flask* nie jest zalecany do użytku tzw. *produkcyjnego*). Aplikacja została zatem osadzona w serwerze *waitress* (https://docs.pylonsproject.org/projects/waitress/en/stable/). Konfiguracja serwera w języku python była bardzo łatwa i wyglądała następująco:

```py
from waitress import serve

from rest_api import app

serve(app, host='0.0.0.0', port=8080)
```

Następnie, aby umożliwić porównanie wydajności dwóch metod wygenerowaliśmy dużą ilość przykładowych danych w bazie danych (10000 rekordów typu "thread")

## Obliczenia zostały wykonane na sprzęcie o następujących parametrach:

* Procesor: Intel Core i5-4440
* Pamięć cache procesora: 6MB
* Taktowanie: 3.10Ghz
* Liczba rdzeni: 4
* Liczba wątków: 4
* Pamięć ram: 8GB
* System operacyjny: Windows 10
* Wersja systemu: Windows 10 PRO N (Version 10.0.17134 Build 17134)
* Architektura system: 64-bit

Do uzyskania połączonych (tzw. *zjoinowanych* danych) w interfejsie GraphQL użyto następującego *query*:

```
{
  allThreads {
    edges {
      node {
        userByCreatedById {
          aboutMe
          avatar
          createdOn
          id
          signature
          username
        }
        
        createdOn

        id
        
        sectionBySectionId {
          id
          name
          sectionLogo
        }
        
        title
      }
    }
  }
}
```

Dla 10 000 rekordów w interfejsie **REST** wyniki przedstawiały się następująco:

![rest10k](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/rest10k.png)

Zaś dla interfejsu **GraphQl** wyniki były takie:

![graphql10k](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/graphql10k.png)

Na powyższym przykładzie widoczna jest dużo wyższa wydajność interfejsu GraphQL, za pomocą którego te same dane uzyskano ponad 10 razy szybciej. Nieco większy był natomiast rozmiar odpowiedzi interfejsu GraphQL - 3.66MB, natomiast odpowiedź REST-a miała 3.46MB. Jest to spowodowane tym, że w GraphQl każdy obiekt jest dodatkowo *opakowany* w pole o nazwie *node*. Jest to jednakże nieznaczna różnica, która nie powinna powodować żadnych niekorzyści.

## Jeszcze większa ilość danych

Taki sam test postanowiliśmy przeprowadzić na większej ilości danych - 50 000 rekordów

Dla 10 000 rekordów w interfejsie **REST** wyniki przedstawiały się następująco:

![rest50k](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/rest50k.png)

Zaś dla interfejsu **GraphQl** wyniki były takie:

![graphql50k](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/graphql50k.png)

Przewaga interfejsu **GraphQl** jest już bardzo widoczna. Widoczna jest tendencja, że wraz ze wzrostem ilości danych, dysproporcja między wydajnością **GraphQL** a **Rest** jest coraz większa na korzyść **GraphQL**

---

# Weryfikacja projektu

W celu zweryfikowania czy zaimplementowane przez nas serwisy **Rest** oraz **GraphQL** nadają się do użycia zaimplementowaliśmy prosty interfejs użytkownika. Interfejs ten zaimplementowaliśmy w ten sposób, aby najpierw był zintegrowany z serwisem **REST** a następnie zintegrowaliśmy go z serwisem **GraphQL**. Dzięki takiemu podejściu mogliśmy dokonać porównania również z perspektywy integracji między serwisem a interfejsem użytkownika (tzw. integracja "front-end" - "back-end").

Poniżej zamieszczono przykładowe zrzuty ekranu obrazujące interfejs:

![mainView](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/forum_screenshots/forum_threads.PNG)

![mainView](https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/forum_screenshots/forum_posts.PNG)

Na tej podstawie można uznać weryfikację za zakończoną sukcesem - oba serwisy w pełni nadają się, aby implementować interfejsy użytkownika z nich korzystające.

Nasze finalne spostrzeżenia na temat porównania interfejsów **Rest** oraz **GraphQL** zamieściliśmy w poniższym podsumowaniu:

| #                                                                     | Rest                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | GraphQL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Trudność implementacji serwisu   ("back-end")                         | Stosunkowo duża. Konieczna   ręczna implementacja dostępu do konkretnych zasobów.      Niektóre metody np. pobieranie tematu za pomocą identyfikatora wymagają   manualnego tworzenia zapytań.      W przypadku dużej ilości różnych modeli w bazie danych trudność   implementacji rośnie. Z powodu dużej ilości manualnej implementacji obecna   jest podatność na błędy                                                                                                                                                                                                                                                                                                                                                                                             | Niska trudność implementacji.   Użyte przez nas narzędzie wymagało od nas jedynie stworzenia struktury w   bazie danych, aby na tej podstawie uruchomić interfejs GraphQL.      Dzięki temu manualna implementacja nie była konieczna. Co za tym idzie   pewność co do braku błędów wzrasta. Jedynie w przypadku, gdy chcielibyśmy   zaimplementować jakieś niestandardowe zapytania, wówczas do tego zadania   wymagana byłaby dobra znajomość narzędzia.                                                                                                                                                                                                                                                                                                                                                                      |
| Trudność integracji serwisu z interfejsem   użytkownika ("front-end") | Średnia trudność integracji. Platformy front-endowe posiadają wbudowane, rozbudowane narzędzia pozwalające na łatwe tworzenie i modyfikowanie zapytań protokołu REST. Głównym problemem tego protokołu jest to, że ilość i typ danych zwracanych przez dany punkt końcowy interfejsu są stałe - skonfigurowane na podstawie danego modelu. Natomiast widoki front-endowe są bardzo dynamiczne w zawartości - często zmienia się, jakie dane wyświetla się w danym widoku. Aby uniknąć pobierania niepotrzebnych danych z serwera, koniecznością jest stworzyć osobny punkt końcowy dla każdego widoku docelowej aplikacji, ale takie rozwiązanie jest bardzo nieoptymalne, ponieważ każda zmiana widoku pociąga za sobą ingerencję w interfejs REST, dokładając pracy. | Stosunkowo niska trudność integracji. Dynamiczny model tworzenia zapytań w graphQL znacznie ułatwia pracę z aplikacjami front-end, które posiadają wiele widoków lub pobierają duże ilości danych, ponieważ zwracane dane w stu procentach polegają na zapytaniu wysłanym przez klienta. Oznacza to, że zawsze gdy zmienia się widok w aplikacji front-endowej, należy po prostu odpowiednio zmodyfikować zapytanie, aby otrzymać potrzebne dane, które jednocześnie nie posiadają zbędnych elementów. W przypadku naszego rozwiązania Postgraphile trudność implementacji front-end była zwiększona, ponieważ dane zwracane były modelowane na podstawie schematu bazy danych, a nie ustalonego przez programistę nazewnictwa, co wymusiło dodatkowe modyfikowanie otrzymanych danych aby były używalne w przyjemnym formacie. |
| Wydajność                                                             | Szczegółowo opisane w dokumencie   nr. 3.      W analizowanym przez nas przypadku czas przesłania dużej ilości danych   przez interfejs REST był dosyć wysoki. Może to świadczyć o niskiej wydajności                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | W analizowanym przez nas przypadku czas przesłania dużej ilości danych   przez interfejs GrapQL był dosyć niski. Świadczy to o wysokiej wydajności                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Zajętość pamięci                                                      | Szczegółowo opisane w dokumencie   nr. 3.      W analizowanym przez nas przypadku rozmiar odpowiedzi z dużą ilością danych   był niski (dzięki skorzystaniu z "lekkiego" formatu JSON)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Szczegółowo opisane w dokumencie   nr. 3.      W analizowanym przez nas przypadku rozmiar odpowiedzi z dużą ilością danych   był nieznacznie większy niż w przypadku technologii REST                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Poziom wsparcia dla technologii                                       | Wysoki. Dzięki temu, że   technologia REST jest od paru lat podstawą w tworzeniu aplikacji webowych   dostępnych jest dużo bibliotek przeznaczonych dla tej technologii. Można   znaleźć również dużą ilość pomocy i materiałów na temat tej technologii.   Również dzięki temu, że REST jest obecnie standardem w tworzeniu dostępu do   danych, inni programiści mogą prawdopodobnie łatwiej skorzystać z naszych   serwisów jeśli są one zaimplementowane w REST (ponieważ są zaznajomieni z   technologią)                                                                                                                                                                                                                                                         | Stosunkowo nieduży. Technologia GraphQL jest jeszcze na etapie rozwoju,   jednakże pojawia się coraz więcej narzędzi dla niej przeznaczonych.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Dodatkowe komentarze                                                  | Ponieważ technologia REST jest   standardem w tworzeniu aplikacji webowych, być może jest dobrym wyborem jeśli   implementowana przez nas aplikacja musi być stabilna                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | GraphQL ma dużo zalet w porównaniu z REST. Główną zaletą GraphQL jest to,   że wykorzystując natywny język zapytań zawsze uzyskamy tylko taką ilość   danych, jaką potrzebuje (nie dostaniemy ich za mało lub zbyt dużo, co zwykle   ma miejsce w przypadku użycia REST). Dzięki istnieniu takich narzędzi jak   użyty przez na PostGraphile GraphQL może być lepszym wyborem w przypadku,   jeśli chcemy szybko zaimplementować aplikację                                                                                                                                                                                                                                                                                                                                                                                      |


