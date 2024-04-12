import eel
import search


print("....STARTING GUI")

print("GO TO YOUR BROWSER!")
print("remember to close the browser window before the the console's one")

print("Thanks for @6weetbix (https://twitter.com/6weetbix) for making wavu.wank.wiki")

eel.init('web')

@eel.expose
def on_close(page, sockets):

    print(page, 'closed')
    print('the app is now closed!', sockets)
    print("you can now close this window")


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
