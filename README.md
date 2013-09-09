sublime-github-issues
=====================

Sublime Text Plugin to handle github issues.  

### Usage

Copy the *.py files to `Packages/User` directory in your Sublime text settings folder. (`~/Library/Application Support/Sublime Text 3` on OS X).   
Set up a shortcut or menu item for the `github-list-issues` command. (More info in the [unofficial documentation](http://docs.sublimetext.info/en/latest/customization/key_bindings.html))   

If no settings are set and the command is run with a file loaded in the view, the local repository of the file is used.
      
Create a settings file name `GithubIssues.sublime-settings` with the following content:   

``` JSON
{
    "repository": "", /* The repository the issues of which you want to use the plugin with */
    "username": "", /* The username of the owner of that repository */
    "token": "" /* If the repository is private an access token is needed to be created on github.com */
}
``` 

More information on the access token [here](https://help.github.com/articles/creating-an-access-token-for-command-line-use).
