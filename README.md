# <p id="title">Interface</p>

## **/!\ This library is only compatible for Windows computers with the language in French**

Infos des interfaces réseau de Windows.

Librairie Python par Lassa Inora.

--------
## Sommaire

- **[Liens](#links)**
- **[Contacts](#contact)**
- **[Class Interface](#class_interface)**
  - ***[Interface initialization](#interface__init__)***
  - ***[Methods](#interface_methods)***
- **[Class Connexion](#class_connexion)**
  - ***[Connexion initialization](#connexion__init__)***
  - ***[Methods](#connexion_methods)***
--------

## <p id="links">Liens</p>

- [GitHub personnel](https://github.com/LassaInora)
- [GitHub du projet](https://github.com/LassaInora/Interface)
- [Site web du projet](https://lassainora.fr/projet/librairies/interface)

## <p id="contact">Contacts</p>

- [Email personnel](mailto:axelleviandier@lassainora.fr)
- [Email professionnel](mailto:lassainora@lassainora.fr)
--------
## <p id="class_interface">Class Interface:</p>

- ### <p id="interface_methods">Méthodes:</p>

  - str(time):
    - Envoie les informations de l'Interface et de ses connexions.

--------
## <p id="class_connexion">Class Connexion:</p>

- ### <p id="connexion__init__">Initialisation de Connexion.</p>

  - infos: Le texte contenant toutes les infos de connexion.

- ### <p id="connexion_methods">Méthodes:</p>

  - get_me(interface):
    - Récupère l'instance correspondant à la variable Connexion actuel
  - speedtest(duree):
    - Test de la vitesse de la connexion.
  - async_speedtest(duree):
    - Test de la vitesse de la connexion de façon asynchrone.
  - str(time):
    - Envoie les informations de la connexion.