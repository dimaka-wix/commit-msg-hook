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
  rev: v0.2.8
  hooks:
    - id: commit-msg-hook
      stages: [commit-msg]
```
### Add valid prefixes(optional)
Add additional prefixes as an ```args:``` separated by ```,``` after the keyword ```--prefix```  and end with the delimiter ```--```
#### Example
```
hooks:
  - id: commit-msg-hook
    args: [--prefix, Check, Modify, --]
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
### Commit Rules

* _Write up to **72** characters(preventing ellipsis in git)_
* _Capitalise the subject line_
* _Do not end the subject line with a period_
* _Use the imperative mood(e.g. **Add** instead of **Added**)_
* _Start message with one of following prefixes_
  - _**Add ...**_
  - _**Change ...**_
  - _**Create ...**_
  - _**Disable ...**_
  - _**Fix ...**_
  - _**Merge ...**_
  - _**Move ...**_
  - _**Refactor ...**_
  - _**Release ...**_
  - _**Remove ...**_
  - _**Rename ...**_
  - _**Tslint ...**_
  - _**Update ...**_
* _Use the description to explain what and why vs how_
* _Press **Shift+Enter** to create a new line and to write more characters then vscode lets you_
* _**Separate subject from body with a blank line!**_


#### Example
```
Refactor Z function in X file from Y component
<optional part, adding it leave an empty line here>
* Fix ...
* Add ...
* Update ...
 ```
 ### Bypass the hook in one of the following ways
- ```SKIP=commit-msg-hook git commit -m "Your message"```
- ```git commit -m "Your message" --no-verify```
- ```git commit -m "Your message" -n (not recommended)```
