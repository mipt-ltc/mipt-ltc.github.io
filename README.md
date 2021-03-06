# LTC webpage

## How does "Backend" works?
- We have python scripts (in `assets/DBmanage/`) that interacts with data on Google Drive:
  1. `getDriveTree.py`  
    It uses an API key and pulls info about Drive files. It generates the `autoGenerated/notesTree.yml` (at the `_data/` dir)
  1. `updateDBs.py`
    It processes the `notesTree.yml` file and extracts info about
      - lecturers surnames,
      - notes names,
      - subject names.  
    After that script search names that are not in the database yet and writes them in `autoGenerated/newLecturers.yml` and `autoGenerated/newSubjects.yml`. Notes with strange names go into `autoGenerated/badNamedNotesAndSubjects.log`.
  1. `addNewNames.py`
    This script allows easily add new names in databases (by hand). Just run make addNames (from `assets/DBmanage/` dir) and follow instructions.
- Every day the GitHub actions run our scripts to update databases (except `addNewNames.py`).  
  Scripts while run produces descriptive comments about new names, bad naming and etc, so don't be shy to see the actions log.
  
## Files in _data
- `lecturers.yml`, `subjects.yml`: aliases strings for lectureres family names and subject names.  
  The content looks like this:
  ```
  - "|$ООП|object oriented programming|oop|объектно-ориентированное программирование|"
  - "|$Алгебра и геометрия|algebra and geometry|алгем|"

  ```
  The `$` char at the beggining means that this name will be choosed when displaying at webpage.  
- `autoGenerated/`: files generated by `getDriveTree.py` and `updateDBs.py` scripts.
  - `notesTree.yml`: tree of pdfs and folders from Google Drive. 
  - `badNamedNotesAndSubjects.log`: strange names (automatic check).
  - `newLecturers.yml`, `newSubjects.yml`: names that wasn't found in `lecturers.yml` or `subjects.yml`, but exists on Google Drive
  - `notesList.yml`, `subjectsList.yml`: files for js script at home page. It uses only their info for generating html.


## How to contribute

### Frontend
1. Install or update your `Docker`. 
2. Start docker container with:
   ```
   $ docker-compose up    # will take some time to download dependencies at first time, but then will run quickly.
   ```
   After it is done please check the `localhost:4000` . Changed made in your folder will automatically (within few seconds) appear at the local webpage.

5. After you push changesin files (like `markdown` and `html`) GitHub Pages may need up to hour to fully deploy it.
6. For adding `LaTeX` equations in your `markdown` and `html` you can check [upmath.me](https://upmath.me/).

### Backend
Install python dependencies with:
```
$ pip install -r requirements.txt
```
For testing the interaction with Google Drive you need to [create your API key](https://cloud.google.com/docs/authentication/api-keys) (it is not necessary to generate one to work with other sections, because Google Drive data automatically updates every day by GitHub Actions).  After that run:
```
$ echo 'YOUR_API_KEY' > assets/DBmanage/apiKey.txt
```

After you edit files you can wait when actions updates `autoGenerated` files or update them manually with:
```
$ cd assets/DBmanage/
$ make        # will pull info from Google Drive as well
```
or
```
$ make update # will just update based on current info from drive
```

To make an update of names (when new notes with new names were added on the Google Drive) you can run:
```
$ make add    # will run an CLI, that allows to easily add new names
```
