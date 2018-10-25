# MAPOBS
Repository for OVPF MAPOBS project

MAPOBS est une application Web pour la saisie et l'exploitation de phénomènes éruptifs. Il est destiné au personnel de l'Observatoire Volcanologique du Piton de la Fournaise (OVPF).



Avant toute chose, vous devez avoir installé Django sur votre machine. Pour plus d'informations consultez: https://docs.djangoproject.com/en/2.1/intro/install/

Une fois Django installé:

- Télécharger le code source de MAPOBS
- Placez vous dans le dossier contenant le projet (au niveau du manage.py)
- Modifiez le document mapobs/settings.py à la ligne 29, en remplaçant ALLOWED_HOST par l'adresse de votre choix
- Puis, afin d'accéder à l'application depuis un navigateur Web, tapez les commandes suivantes dans un terminal Ubuntu:

python manage.py runserver 0.0.0:8000

- Ouvrez votre navigateur Web et rendez-vous à l'adresse: http://195.83.188.45:8000. En remplaçant 195.83.188.45 par l'addresse renseignée dans le fichier de configuration.

Pour plus d'informations sur la manière de remplir la base de données de l'application, consulter le fichier gestion_bdd.pdf qui se trouve à la racine de ce projet.
