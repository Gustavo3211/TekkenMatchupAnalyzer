import requests
from bs4 import BeautifulSoup
import pandas as pd


def iniciarbs4(url):
    response = requests.get(url)
    

    website = BeautifulSoup(response.text, 'html.parser')

    return website




"""calculate the matchups"""
"""i used gpt here cuz i was about to commit a crime trying to wrap my head around bs4 and tables LMAO"""
"""that is the part someone prolly can do a better job then me tbh, but its working"""
def replaytable(url):
    website = iniciarbs4(url)
    if website:
        replay_table_heading = website.find("h2", string="Replays")
        if replay_table_heading:
            replay_table = replay_table_heading.find_next('table')

    # win/loses count
    if replay_table:
        rows = replay_table.find_all('tr')[1:]  # Skip the header row
        data = [[td.text.strip() for td in row.find_all('td')] for row in rows]
        df = pd.DataFrame(data, columns=['When', 'Score', 'Rating', 'Opponent', 'Opp. char', 'Opp. rating'])
        df['Win'] = df['Score'].str.contains('WIN').astype(int)  # Convert boolean to int
        df['Loss'] = df['Score'].str.contains('LOSE').astype(int)

        win_loss_count = df.groupby('Opp. char')[['Win', 'Loss']].sum().reset_index()
        win_loss_count = win_loss_count.sort_values(by=['Win', 'Loss'], ascending=False)  # Sort win_loss_count

        # Calculate the total number of matches for each character
        win_loss_count['Total Matches'] = win_loss_count['Win'] + win_loss_count['Loss']

        win_percentages = df.groupby('Opp. char')['Win'].mean() * 100  # Calculate win percentage for each character
        win_percentages = win_percentages.reset_index()
        win_percentages.columns = ['Character', 'Win Percentage %']
        win_percentages = win_percentages.sort_values(by='Win Percentage %', ascending=False)  # Sort win_percentages

        def format_percentage(val):
            return '{:.2f}%'.format(val)

        win_percentages['Win Percentage %'] = win_percentages['Win Percentage %'].apply(format_percentage)

        return win_loss_count, win_percentages

def search(url):
    website = iniciarbs4(url)
    rating_table = website.find("h2", string="Ratings")
    name = website.find_all("h1", limit =2)
    number_data = website.find("p")

    if rating_table:
        ratings_table = rating_table.find_next_sibling('table')
        mainchar = ratings_table.find("a")

    result_html = ""
    for names in name:
        if names.text != "Wavu Wank":
            result_html += '<div class="container">'
            result_html += '<h2 class="mt-4">URL: ' + url + '</h2>'
            result_html += '<h2 class="no-capture text-danger">Note: 1. If your link includes a character name at the end, it will display the win rate and related information for that specific character. Otherwise, it will provide information based on the highest rated character.</h2>'
            result_html += '<h2 class="no-capture text-danger">2. Winrate is calculated based on the number of wins divided by the total number of games (wins + losses). If the total number of games is less than 10, the win rate might not be reliable.</h2>'
            
            

            result_html += '<h3 class="mt-4">Player: ' + names.text.strip() + '</h3>'
            result_html += '<h2 class="mt-4">'+ number_data.string +' </h2>'

            winloses, winrate = replaytable(url) 

            result_html += '<div class="row">'
            result_html += '<div class="col-md-6">'
            result_html += '<h2 class="mt-4">Win/loses against characters: </h2>'
            result_html += '<p>(Characters with less then 10 matches will be in red)<p>'
            result_html += winloses.to_html(index=False, classes="table table-bordered table-dark gamenumber")
            result_html += '</div>'

            result_html += '<div class="col-md-6">'
            result_html += '<h2 class="mt-4">Winrate against characters: </h2>'
            result_html += '<div class="">Winrate against characters:</div>'
            result_html += winrate.to_html(index=False, classes="table table-bordered table-dark winrate")
            result_html += '</div>'
            result_html += '</div>'

            result_html += '</div>'

    return result_html


