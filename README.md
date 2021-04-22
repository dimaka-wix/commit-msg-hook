# commit-msg-hook
This hook is made as custom plugins under the [pre-commit](https://pre-commit.com/) hook framework and checks if commit message matches the chaos-hub team commit rules.

### Installation 
```
pip install commit-msg-hook
```
### Using commit-msg-hook with pre-commit 

See [pre-commit](https://pre-commit.com/) for instructions

Add this to your ```.pre-commit-config.yaml```
```
-   repo: https://github.com/DimaKarpukhin/commit-msg-hook.git
    rev: v0.1.6
    hooks:
    -   id: commit-msg-hook
        stages: [commit-msg]
        # args is optional, the default length limit is 72
        args: [--max-msg-length=<number>]
 ```   
 Update to the latest release (optional)
  ```
  pre-commit autoupdate --repo https://github.com/DimaKarpukhin/commit-msg-hook.git
  ```
 ### Commit Rules

* _Write up to **72** characters(preventing ellipsis in git)_
* _Capitalise the subject line_
* _Do not end the subject line with a period_
* _Use the imperative mood(e.g. **Add** instead of **Added**)_
* _Start message with one of following prefixes_
  - _**Fix** ..._
  - _**Add** ..._
  - _**Refactor** ..._
  - _**Update** ..._
  - _**Remove** ..._
  - _**Release** ..._
  - _**Move** ..._ 
  - _**Tslint** ..._
  - _**Rename** ..._
  - _**Merge** ..._
* _Use the description to explain what and why vs how_
* _Press **Shift+Enter** to create a new line and to write more characters then vscode lets you_
* _**Separate subject from body with a blank line!**_
* _Use **in/from** format **in suject line** to add the place where the change was made (file/component)_


#### Example
```
Refactor Z function in X file from Y component

- Fix ...
- Add ...
- Update ...
 ```
 ### Bypass the hook
```
git commit -m "Your message" --no-verify
``` 
or
```
git commit -m "Your message" -n
```
