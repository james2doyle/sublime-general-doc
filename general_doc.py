import sublime
import sublime_plugin
import webbrowser

SETTINGS_FILENAME = 'GeneralDoc.sublime-settings'

# From: Packages/Default/symbol.py
# View Package File > Default/symbol.py
def lookup_symbol(window, symbol):
    if len(symbol.strip()) < 3:
        return []

    index_locations = window.lookup_symbol_in_index(symbol)
    open_file_locations = window.lookup_symbol_in_open_files(symbol)

    def file_in_location_list(fname, locations):
        for l in locations:
            if l[0] == fname:
                return True
        return False

    # Combine the two lists, overriding results in the index with results
    # from open files, while trying to preserve the order of the files in
    # the index.
    locations = []
    ofl_ignore = []
    for l in index_locations:
        if file_in_location_list(l[0], open_file_locations):
            if not file_in_location_list(l[0], ofl_ignore):
                for ofl in open_file_locations:
                    if l[0] == ofl[0]:
                        locations.append(ofl)
                        ofl_ignore.append(ofl)
        else:
            locations.append(l)

    for ofl in open_file_locations:
        if not file_in_location_list(ofl[0], ofl_ignore):
            locations.append(ofl)

    return locations

# From: Packages/Default/symbol.py
# View Package File > Default/symbol.py
def symbol_at_point(view, pt):
    symbol = view.substr(view.expand_by_class(pt, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, "[]{}()<>:."))
    locations = lookup_symbol(view.window(), symbol)

    if len(locations) == 0:
        symbol = view.substr(view.word(pt))
        locations = lookup_symbol(view.window(), symbol)

    return symbol, locations

class GeneralDoc(sublime_plugin.EventListener):
    def on_hover(self, view: sublime.View, point: int, hover_zone: int):
        settings = sublime.load_settings(SETTINGS_FILENAME)

        if not settings or hover_zone != sublime.HOVER_TEXT:
            return

        scope = view.scope_name(view.sel()[0].begin()).strip()

        docs = settings.get('docs')

        matching_doc = filter(lambda doc: doc["scope"] in scope, docs)

        matched_scope = next(matching_doc, None)
        # handle cases where the iterator is "empty"
        if not matched_scope:
            # no matching scopes found
            return

        if "name" not in matched_scope:
            sublime.error_message('Missing "name" key in scope definition. See "Documentation structure" in the README.')
            return

        matching_name = matched_scope["name"]
        if "cases" not in matched_scope:
            sublime.error_message('Missing "cases" key in scope definition. See "Documentation structure" in the README.')
            return

        cases = matched_scope["cases"]

        if len(cases) < 1:
            sublime.error_message('Missing "cases" key in scope definition. See "Documentation structure" in the README.')
            return

        word, _ = symbol_at_point(view, point)

        if len(word) < 1:
            return

        for case in cases:
            if "matches" not in case:
                sublime.error_message('Missing "matches" key in case definition. See "Documentation structure" in the README.')
                continue

            if len(case["matches"]) < 1:
                sublime.error_message('Missing "matches" in scope definition. See "Documentation structure" in the README.')
                continue

            if "url" not in case:
                sublime.error_message('Missing "url" key in case definition. See "Documentation structure" in the README.')
                continue

            if word in case["matches"]:
                url = case["url"].replace("$1", word)

                view.show_popup(make_popup(matching_name, url, word),
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                    point,
                    *view.viewport_extent(),
                    on_navigate=open_url
                )

# More code stolen from symbol.py
def make_popup(name: str, url: str, word: str):
    return """
    <body id=show-definitions>
        <style>
            body {
                font-family: system;
            }
            h1 {
                font-size: 1.1rem;
                font-weight: bold;
                margin: 0 0 0.25em 0;
            }
            p {
                font-size: 1.05rem;
                margin: 0;
            }
        </style>
        <h1>%s Documentation:</h1>
        <p><a href="%s">%s</a></p>
    </body>
    """ % (name, url, word)

# https://github.com/leonid-shevtsov/ClickableUrls_SublimeText/blob/2c1a8069e3ce40ef439ad583bc1220e572fba511/clickable_urls.py#L123
def open_url(url):
    browser =  sublime.load_settings(SETTINGS_FILENAME).get('browser')
    try:
        webbrowser.get(browser).open(url, autoraise=True)
    except(webbrowser.Error):
        sublime.error_message('Failed to open browser. See "Customizing the browser" in the README.')
