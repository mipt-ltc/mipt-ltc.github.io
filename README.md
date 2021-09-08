# LTC webpage
https://mipt-ltc.github.io/  
It is the page made for the LTC student club. It provides an interface to search for notes that we gathered on our Google Drive.

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
  - "|$#ооп|object oriented programming|oop|объектно-ориентированное программирование|"
  - "|$алгебра и геометрия|algebra and geometry|алгем|"

  ```
  The `$` char at the beggining means that this name will be choosed when displaying at webpage.  
  The `#` char after `$` means that all letters will be displayed in uppercase.
- `autoGenerated/`: files generated by `getDriveTree.py` and `updateDBs.py` scripts.
  - `notesTree.yml`: tree of pdfs and folders from Google Drive. 
  - `badNamedNotesAndSubjects.log`: strange names (automatic check).
  - `newLecturers.yml`, `newSubjects.yml`: names that wasn't found in `lecturers.yml` or `subjects.yml`, but exists on Google Drive
  - `notesList.yml`, `subjectsList.yml`: files for js script at home page. It uses only their info for generating html.


## How to contribute

### Frontend
1. Install or update your `ruby` and `gem`. (You can check if they installed with commands `$ ruby -v` and `$ gem -v`.)
1. Run instructions from https://jekyllrb.com to install `Jekyll` :
    ``` 
    $ gem install bundler jekyll
1.  Install `Jekyll` dependencies:
    ``` 
    $ git clone git@github.com:mipt-ltc/mipt-ltc.github.io.git
    $ cd mipt-ltc.github.io.git
    $ bundle install
    ```
1. You can start server with the command `$ bundle exec jekyll serve`


### Backend
Install python dependencies with:
```
$ pip install -r requirements.txt
```
To test interaction with Google Drive you need to [create your API key](https://cloud.google.com/docs/authentication/api-keys). After that run:
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
