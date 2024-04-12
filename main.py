import eel
import search

# Initialize the Eel app with the location of your web files
eel.init('web')

@eel.expose
def on_close(page, sockets):
    print(page, 'closed')
    print('Remaining open sockets:', sockets)


@eel.expose
def search_profile(url):
    if url.startswith("https://wank.wavu.wiki/player/"):
        try:
            results = search.search(url)
            return results
        except Exception as e:
            return "An error occurred: " + str(e)
    else:
        return "The URL should start with 'https://wank.wavu.wiki/player/'. Please enter a valid URL."

# Start the Eel app
eel.start('index.html', mode='default', close_callback=on_close)
