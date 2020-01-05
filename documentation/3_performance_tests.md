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