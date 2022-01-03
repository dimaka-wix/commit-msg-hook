# commit-msg-hook
This hook is made as a custom plugin under the [pre-commit](https://pre-commit.com/) hook framework and checks if commit message matches the chaos-hub team commit rules.

## Installation 
```
pip install commit-msg-hook
```
## Using commit-msg-hook with pre-commit 

For more details see: [pre-commit](https://pre-commit.com/)
### Install pre-commit package manager 
```
pip install pre-commit
```


### Create a file ```.pre-commit-config.yaml``` in the root folder with the following configuration
```
- repo: https://github.com/dimaka-wix/commit-msg-hook.git
  rev: v0.3.4
  hooks:
    - id: commit-msg-hook
      stages: [commit-msg]
```
### To enable commit-msg hook with pre-commit run:
```
pre-commit install --hook-type commit-msg
```
### Update to the latest release (optional)
```
pre-commit autoupdate --repo https://github.com/dimaka-wix/commit-msg-hook.git
```
### _Commit Rules_

* _Write up to **72** characters(preventing ellipsis in git)_
* _Capitalize the subject line_
* _Use the imperative mood(e.g. **Add** instead of **Added**, **Adds** or **Adding**)_
* _Do not end the lines with any punctuation character_
* _Use the description to explain what and why vs how_
* _In case of multiline message do the following:_
  * _Press **Shift+Enter** to create a new line and to write more characters then vscode lets you_
  * _Separate subject line from message body with a blank line_
  * _Follow the rules above when writing each line of the message_


#### _Example_
```
Refactor foo function in x file from y component

* Remove duplications
* Add docstrings
* Update the types of arguments
 ```
 ### Bypass the hook in one of the following ways
- ```SKIP=commit-msg-hook git commit -m "Your message"```
- ```git commit -m "Your message" --no-verify```
- ```git commit -m "Your message" -n (not recommended)```
