# General Doc

> A plugin for [Sublime Text 3](http://sublimetext.com) that creates documentation from it's own config

![demo](demo.gif)

## Summary

This packages allows you to list an array of symbols and supply a URL that will be used to point to the documentation for that symbol.

### Use Cases

There are lots of "languages" (mostly templating ones) that don't have support for more of the common features of languages that can be statically analysed or run through a [LSP](https://microsoft.github.io/language-server-protocol/).

This package allows you to provide a nice popup for words that are being hovered over that will link to documentation for that symbol. For languages with lots of keywords and features that don't require being "analysed", this can be really helpful.

This package works by allowing you to define your documentation structure in the plugins settings file so that when hovered words are matched, it will give you a popup with a link to documentation.

You can provide a single documentation URL for a group of words, or make a group for each word. The documetations are divided into Sublime "scopes" so that they are only used on scopes that actually have matching documentation supplied.

## Installation

With [Package Control](http://wbond.net/sublime_packages/package_control) (look for "General Doc"), or just drop the plugin into Sublime Text's Packages folder.

## Configuration

All configuration is done via the settings file that you can open via the main menu: `Preferences > Package Settings > General Doc > Settings - User`.

### Documentation structure

See [GeneralDoc.sublime-settings](GeneralDoc.sublime-settings) for an example of the structure.

### Built-in documentation

- [x] HTML (using [MDN Web/HTML/Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element))
- [x] Twig (using [twig.symfony.com/doc/2.x](https://twig.symfony.com/doc/2.x/))
- [x] Liquid (using [shopify.github.io/liquid](https://shopify.github.io/liquid/) or [shopify.dev/docs/liquid](https://shopify.dev/docs/liquid))
- [ ] more examples to come!

### Debugging

Set `logging` to `true` in the plugin settings to help debug your documentation definition as well as what the plugin is doing:

    {
        "logging": true,
    }

Open the Sublime Console (View > Show Console) to see the logging output.

### Customising the browser

By default, General Doc uses the default system browser. If it doesn't work for you, you can change the browser by setting the `browser` in the `GeneralDoc.sublime-settings`
file, to which you can get from the menu.

Anything from [this list](https://docs.python.org/2/library/webbrowser.html#webbrowser.register) will work, for example:

    {
        "browser": "firefox"
    }

**Note for Windows users.** If the browser you want won't open, you might have to specify the full path manually:

    {
        "browser": "\"c:\\program files\\mozilla firefox\\firefox.exe\" %s &"
    }

Take note of the escaped slashes and the quoting around the name.

The ampersand at the end is significant - without it the editor will hang and wait for browser to close.

## References

- Packages/Default/symbol.py
- [leonid-shevtsov/ClickableUrls_SublimeText](https://github.com/leonid-shevtsov/ClickableUrls_SublimeText)
