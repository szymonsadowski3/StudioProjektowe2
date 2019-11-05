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

![model]("https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/faker.PNG")

## Generowanie danych

Aby móc pracować z tak przygotowaną bazą danych użyliśmy biblioteki **faker** (https://github.com/joke2k/faker) to wygenerowania przykładowych rekordów w bazie danych

Po uruchomieniu skryptu tak wyglądała przykładowa porcja danych wygenerowana przez skrypt (na zrzucie ekranu poniżej widać wygenerowane prywatne wiadomości):

![faker]("https://raw.githubusercontent.com/szymonsadowski3/StudioProjektowe2/master/documentation/model.PNG")

Mając tak przygotowaną bazę danych mogliśmy przystąpić do implementacji sieciowego interfejsu dostępu do danych **REST**

## Implementacja dostępu REST

Do implementacji dostępu REST użyliśmy biblioteki **flask** (https://palletsprojects.com/p/flask/). Biblitoka ta jest lekkim rozwiązaniem do tworzenia małych aplikacji sieciowych i szczególnie dobrze nadaje się do implementacji aplikacji REST-owych.

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

## Linki

Rozwijany przez nas kod źródłowy dostępny jest pod adresem: https://github.com/szymonsadowski3/StudioProjektowe2

## Autorzy

Szymon Sadowski
Krzysztof Szczyrbak