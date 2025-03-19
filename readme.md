# Application de Gestion de Bibliothèque en Microservices

Cette application décompose une solution monolithique de gestion de bibliothèque en plusieurs microservices. Les principaux services sont :

- **Books-Service** : Gestion des livres (CRUD, disponibilité, etc.)
- **Members-Service** : Gestion des membres (création, mise à jour, etc.)
- **Reservation-Service** : Gestion des réservations de livres (vérification, création, etc.)

L'architecture s'appuie également sur des services complémentaires tels que PostgreSQL pour la base de données, RabbitMQ pour la communication asynchrone et éventuellement des outils de monitoring.

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) installé sur votre machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installé.
- (Optionnel) Git pour cloner le dépôt.

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/maxencelgy/micro-services-with-docker.git
   cd library
   ```

2. **Structure du projet :**

   ```
   library/
   ├── books-service/
   │   ├── main.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── database.py
   │   ├── requirements.txt
   │   └── Dockerfile
   ├── members-service/
   │   ├── main.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── database.py
   │   ├── requirements.txt
   │   └── Dockerfile
   ├── reservation-service/
   │   ├── main.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── database.py
   │   ├── requirements.txt
   │   └── Dockerfile
   └── docker-compose.yml
   ```

## Lancer l'application

1. **Construire et lancer les services avec Docker Compose :**

   ```bash
   docker-compose up --build -d
   ```

   Cette commande va :
    - Construire les images Docker pour chaque service.
    - Lancer tous les conteneurs en arrière-plan.

2. **Vérifier que tous les services tournent :**

   ```bash
   docker-compose ps
   ```

   Vous pouvez également utiliser :

   ```bash
   docker ps
   ```

## Vérification du bon fonctionnement

### Accéder aux logs

Pour consulter les logs d'un service, par exemple **Books-Service** :

```bash
docker-compose logs -f books-service
```

### Tester les endpoints

1. **Books-Service :**

    - Pour récupérer la liste des livres :

      ```bash
      curl http://localhost:8001/books/
      ```

    - Pour récupérer un livre spécifique :

      ```bash
      curl http://localhost:8001/books/1
      ```

2. **Members-Service :**

    - Pour récupérer la liste des membres :

      ```bash
      curl http://localhost:8002/members/
      ```

3. **Reservation-Service :**

    - Pour créer une réservation (adapter les données selon vos besoins) :

      ```bash
      curl -X POST http://localhost:8003/reservations/ \
           -H "Content-Type: application/json" \
           -d '{"book_id": 1, "member_id": 1}'
      ```

### Vérification du Healthcheck

Certains services disposent d'un endpoint de santé (healthcheck). Par exemple, pour vérifier le service Books :

```bash
curl http://localhost:8001/health/live
```

## Dépannage

- **Module non trouvé ou erreurs d'import :** Vérifiez que la structure des dossiers est correcte et que les modules (`models.py`, `schemas.py`, `database.py`) existent dans chaque service.
- **Ports déjà utilisés :** Assurez-vous qu'aucun autre service n'utilise les ports définis dans le fichier `docker-compose.yml`.
- **Logs :** Consultez les logs avec `docker-compose logs -f <service>` pour identifier d'éventuelles erreurs lors du démarrage.

## Arrêt des services

Pour arrêter et supprimer les conteneurs, exécutez :

```bash
docker-compose down
```


