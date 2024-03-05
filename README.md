<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->

## About The Project

Application pour la reconnaissance des yeux d'employés pour contrôle de sécurité.

Démo factice avec jeu de données MMU IRIS Database

[Watch the Demo](https://drive.google.com/file/d/1tdMh40xKPWvn9w6cJblMWNXi0sa4TU9a/view)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- Nécessite la mise en place en amont d'une base de données MySQL, pour sauvegarde des archives et user
- Possibilité de créer un environnement virtuel pour le projet

### Installation

_Ci-dessous la procédure à suivre pour lancer l'application_

1. Monter une base de données MySQL (docker supporté)
2. Cloner le répertoire à l'emplacement souhaité
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Installer un environnement virtuel (optionnel) et les requirements

   ```
   pip install -r requirements.txt
   ```

4. Remplir les informations dans les scripts config.py et utils.py:

   - config.py :
     - la fonction config : host, user, password, port et database.
   - utils.py :
     - ASSETS_PATH : chemin vers le dossier assets.
     - SAVING_PATH : chemin vers le répertoire pour sauvegarder les images provenant de l'archive (double-clic sur l'image à sauvegarder), utile pour rapport de sécurité pour récupérer les images des personnes refusées.
     - MAIL : mail du développeur de l'application pour rapport de bug de l'application fait par utilisateur.

5. Lancer l'application via app.py (peut prendre plusieurs minutes pour se lancer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
