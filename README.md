# pyscrap
Srap scrap scrap!

REMINDER: Only for educational purpose

# Usage
Install dependencies, please install [pipenv](https://pypi.org/project/pipenv/).
```$bash
$ pipenv shell --three && pipenv install
```
To scrap, we need to be authenticated by providing our linkedin cookies in JSON format.
You can get your cookies with some chrome extension like [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=id)
and follow its instruction. After that create a JSON file and paste in.

Run the main.py, we must provide action, url, save and and cookies argument.
```$xslt
$ python main.py --action=full --url=https://www.linkedin.com/in/{USER_PUBLIC_IDENTIFIER}/ --cookies=./cookies.json --save=./result.csv
```
* action: full (provide user identifier, profile, and connection) | profile (only provide user profile)
* url: user profile url that you want to scrap
* cookies: path to your cookies
* save: csv filename
