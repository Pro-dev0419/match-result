import json , os , pandas as pd  , requests
import urllib.request
from bs4 import BeautifulSoup as Soup
import sqlalchemy
from datetime import datetime
import re

### FUNCTIONS ###

def convert_odds(odds):
    probability = (1/odds)*100
    return round(probability,2)

# database_username = os.environ['databaseUser']
# database_password = os.environ['databasePass']
# database_ip       = os.environ['databaseHost']
# database_name     = os.environ['databaseName']
# database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
#                                            format(database_username, database_password, 
#                                                   database_ip, database_name))

database_username = 'admin'
database_password = 'Rv301297'
database_ip       = 'database-1.clalyzsfkuqz.us-east-1.rds.amazonaws.com'
database_name     = 'default'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                        format(database_username, database_password, 
                                                database_ip, database_name))

def fix_names(df):
    dict = {
    'Allen Robinson II' : 'Allen Robinson',
    'Marcus Mariota (ATL)' : 'Marcus Mariota',
    'Eli Mitchell' : 'Elijah Mitchell',
    'Mitchell Trubisky' : 'Mitch Trubisky'
     }
     
    df=df.replace({"NAME": dict, "PLAYER" : dict})
    return df

def rename_fd(df):
    dict = {
        'Passing Yds' : 0,
        'Rushing Yds' : 1,
        'Receiving Yds' : 2,
        'Passing + Rushing Yds' : 3,
        'Pass Completions' : 4,
        'Total Receptions' : 5,
        'Pass Attempts' : 6,
        'Passing TDs' : 7,
        'Longest Pass' : 8,
        'Longest Reception' : 9
    }
    df=df.replace({"PROP": dict})
    return df

def rename_cz(df):
    dict = {
        'PASSING_YARDS' : 0,
        'RUSHING_YARDS' : 1,
        'RECEIVING_YARDS' : 2,
        'Passing + Rushing Yds' : 3,
        'PASSING_COMPLETIONS' : 4,
        'RECEPTIONS' : 5,
        'PASSING_ATTEMPTS' : 6
    }
    df=df.replace({"PROP": dict})
    return df

def rename_mgm(df):
    dict = {
        '300' : 0,
        '320' : 1,
        '340' : 2,
        '306' : 3,
        '305' : 4,
        '342' : 5,
        '303' : 6
    }
    df=df.replace({"PROP": dict})
    return df


### SCRAPE PROJECTIONS ###


def get_roto_stats():
    if datetime.now() >= datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) and datetime.now() <= datetime.today().replace(hour=9, minute=0, second=0, microsecond=0) :
        roto_url = "https://rotogrinders.com/grids/the-blitz-standard-projections-2003303?site=draftkings"
    else:
        roto_url = "https://rotogrinders.com/grids/the-blitz-standard-projections-2003303?site=draftkings"
    roto_hdr = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        # cookies for login
        # currently copy and paste from a request, possible that it gets invalidated when you login/logout, but I thiiiink it should be good
        "Cookie": "_vwo_uuid_v2=D32656D93EB4405F95A665E9A4103668F|f66f274abb1d2ff55fb6c420a4a3e227; ga=GA1.2.1521243564.1619130626; _fbp=fb.1.1619130626173.820818226; __stripe_mid=adb5ec9b-bf50-4dd0-8d8d-b14eb90563153462c3; _hjSessionUser_1359118=eyJpZCI6IjUzMGIyMmQ0LWM4ZjgtNTcwZC04MzAxLTQxMzI5NDk4YTc3NSIsImNyZWF0ZWQiOjE2MzcyMTE0NTQzMDQsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_838133=eyJpZCI6IjM3Y2NiZmJhLWY1YWItNTkwNS04Y2EyLTc1MTlmMjExZjRhNyIsImNyZWF0ZWQiOjE2MzcyOTU2NTA5ODQsImV4aXN0aW5nIjp0cnVlfQ==; __smToken=XqLQP0RRFrZ6CbprUo0tFTya; __smListBuilderShown=Sat Feb 26 2022 12:57:23 GMT-0500 (Eastern Standard Time); remember_82e5d2c56bdd0811318f0cf078b78bfc=eyJpdiI6IlZSOFd3UVo1akhINUhyWHptRVwvWHJRPT0iLCJ2YWx1ZSI6Ikt3QTFIR3RHaVwvbWIwcDBTcEpMN2x5NGdZVko2Y0FqNFVSUElodnk5cE15WU5VK1M4XC9ETFwvazY2S2JDN01mV1UiLCJtYWMiOiI5YzBkYWU5OTg1ODA5OGFjMDlmNzA1N2UyMjI3ZGYyZWY1YjY5Nzk2NmY1ZGJlMzljNjUxZmMyNWUyY2Q1M2I3In0=; __utmz=123114120.1649366112.454.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); _hjid=f2e46a86-64e4-4f05-b88e-567cf60302e2; bc-cookie-consent=1; hubspotutk=cf40c7bcce4844b81e78bd85d84801f8; ELOQUA=GUID=C334A7C285D4493B94578B427CABAC98; _gid=GA1.2.113816621.1653410668; __utmc=123114120; _ia_loc_r=ON; _ia_loc_c=CA; __hssrc=1; logged_in=eyJpdiI6InhHZnhORjlIdDgzVGVXOGlLcEpEVVE9PSIsInZhbHVlIjoibjduT1dBejl3NTdLb01EbDhucElCdz09IiwibWFjIjoiOWUyZjk2MmU0YjE0ZTg2NjQ5MzUyZWU0Y2RiMTUyZDkyNGI2NmYwMDk2YmUyNzM0NzY2OTRjMzdlMzkzZDdhNiJ9; __utma=123114120.1521243564.1619130626.1653496937.1653499221.626; _hjIncludedInSessionSample=1; _hjSession_1359118=eyJpZCI6ImU5NTI2MDY0LTY3MWUtNGJiOC05M2U3LTAyMzllN2ZlZTYwYiIsImNyZWF0ZWQiOjE2NTM0OTkyMjEzMzcsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; __stripe_sid=f46dfd34-399e-4ebf-9506-92dfd71ad403e7d213; __utmb=123114120.3.8.1653499221; laravel_session=eyJpdiI6InlKUnVjRFFDTzI3UUZ4MW5XUjE4b3c9PSIsInZhbHVlIjoic3poYW12Z3BKUnU4NWFYeWNDVU5ITWJrOXdFdGZZMlNVM2JrTTllTldjaHBPNENFYUJGT1VGdHN1cEFmcGk0RERMVFwvdkRcL2ZxYjM5dEREdWFMUE85dz09IiwibWFjIjoiYWIwMTM5OTZmZmFkYThhMjUyMzRhNDAwMjI0ZjFhMzZmMGI0MTEzOTU1YTZlN2NmYzM0OTQ5Zjk5NjlmNjJmOCJ9; __hstc=95429123.cf40c7bcce4844b81e78bd85d84801f8.1652729315850.1653496938130.1653499227956.31; __hssc=95429123.1.1653499227956; __utmli=top"  }
    req = urllib.request.Request(roto_url, headers=roto_hdr)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    player_data = []
    try:
        data_start = html.index("data = [{")
        data_end = html.index("]", data_start)
        player_data = json.loads(html[data_start + 7:data_end+1])
    except Exception:
        print('not found')
    df = pd.DataFrame(player_data)
    df = fix_names(df)
    df.to_csv('blitz.csv', index=False)
    return df

def get_4_for_4():
    URL = "https://www.4for4.com/full-impact/cheatsheet/Flex/91309/ff_nflstats"
    TABLE_ID = "sortable-rankings-table"
    HEADER = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        "cookie" : "Drupal.visitor.cover_blocks:selected_tab=cover; user_mode=cover; SSESSc40475ee089b0d4e8158fa797261c63c=0RYKXqDGg-He6gQFhxC2xRExDDW7VVll7zRl_INcksY; Drupal.visitor.subscriptionPlan=betting_2022; Drupal.visitor.drupal_login=a:5:{s:16:'"'SESSION_USERNAME'"';s:8:'"'csmaniac'"';s:12:'"'SESSION_TYPE'"';i:1;s:16:'"'SESSION_LOGGEDIN'"';i:1;s:19:'"'SESSION_LOGINFAILED'"';i:0;s:11:'"'FULL_IMPACT'"';i:1;}; aucp13n=t6dncx; ff4for4uid=45000; default_page_league={'"'full-impact_cheatsheet_QB__ff_nflstats_early'"':'"'63963'"','"'full-impact_cheatsheet_QB__ff_nflstats_early_adp_blend'"':'"'63963'"','"'full-impact_cheatsheet_Flex__ff_nflstats'"':'"'91309'"'}"
    }
    req = urllib.request.Request(URL, headers=HEADER)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    soup = Soup(html)
    htmltable = soup.find(id=TABLE_ID)
    rows = htmltable.find_all("tr")
    final_data = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 2:
            # name and team -> pull desired stats from above by column index
            # print(columns[1].text + " - " + columns[2].text)
            final_data.append({ "PLAYER": columns[1].text, "RUATT_4": columns[7].text, "RUYDS_4": columns[8].text, "REC_4": columns[10].text, "RECYDS_4": columns[11].text, "REC_4": columns[10].text })
    URL = "https://www.4for4.com/full-impact/cheatsheet/QB/91309/ff_nflstats"
    req = urllib.request.Request(URL, headers=HEADER)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    soup = Soup(html)
    htmltable = soup.find(id=TABLE_ID)
    rows = htmltable.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 2:
            # name and team -> pull desired stats from above by column index
            # print(columns[1].text + " - " + columns[2].text)
            final_data.append({ "PLAYER": columns[1].text, "COMP_4": columns[6].text, "ATT_4": columns[7].text, "PAYDS_4": columns[8].text, "RUYDS_4": columns[12].text})
    df = pd.DataFrame(final_data)
    df.fillna(0,inplace=True)
    df.to_csv('4for4.csv', index=False)
    return df

razz_url = "https://football.razzball.com/pigskinonator"
razz_hdr = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
    "Cookie": "wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_6287f1ba5b8ab84494a2ba59fda95484=csmaniac%7C1681950144%7CHJNKbuH1fWLtkXcimPRdCgJsxqEsxR6xmCJRSthMJLU%7Cb3fbdded4c708782455a44df3aa1c910137afe0cf4e4979fe9966f5963852fa2"  }
razz_table_id = "neorazzstatstable"

def get_razz_stats():
    req = urllib.request.Request(razz_url, headers=razz_hdr)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    print (html)
    start_pos = html.find('<table id="neorazzstatstable" class="tablesorter" style="font-size:8pt;">')
    end_pos = html.find('<aside id="text-60" class="widget_text amr_widget ">')
    truncated = html[start_pos:end_pos]
    soup = Soup(truncated, "html.parser")
    rows = soup.find_all("tr")
    print (rows)
    #print(rows[0])
    '''
        <tr class="sorter-head">
            <th class="filter-false">#</th>
            <th class="sorterhead-Name header">Name</th>
            <th class="sorterhead-Team header">Team</th>
            <th class="sorterhead-Date header">Date</th>
            <th class="sorterhead-GT header">GT</th>
            <th class="sorterhead-DH header">DH</th>
            <th class="sorterhead-Opp header">Opp</th>
            <th class="sorterhead-LU header">LU</th>
            <th class="sorterhead-QS header">QS</th>
            <th class="sorterhead-W header">W</th>
            <th class="sorterhead-L header">L</th>
            <th class="sorterhead-IP header">IP</th>
            <th class="sorterhead-H header">H</th>
            <th class="sorterhead-ER header">ER</th>
            <th class="sorterhead-K header">K</th>
            <th class="sorterhead-BB+ HBP header">BB+ HBP</th>
            <th class="sorterhead-ERA header">ERA</th>
            <th class="sorterhead-WHIP header">WHIP</th>
            <th class="sorterhead-PTS header">PTS</th>
            <th class="sorterhead-UP PTS header">UP PTS</th>
            <th class="sorterhead-Salary header">Salary</th>
            <th class="sorterhead-$/Pt header">$/Pt</th>
            <th class="sorterhead-PTS ARC header">PTS ARC</th>
        </tr>
    '''
    final_data = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 2:
            # name and team -> pull desired stats from above by column index
            # print(columns[1].text + " - " + columns[2].text)
            final_data.append({ "PLAYER": columns[1].text, "COMP_RAZZ": columns[8].text, "ATT_RAZZ": columns[9].text, "PAYDS_RAZZ": columns[10].text, "RUYDS_RAZZ": columns[15].text, "RECYDS_RAZZ": columns[19].text, "REC_RAZZ": columns[18].text })
    df = pd.DataFrame(final_data)
    df = fix_names(df)
    return df


### SCRAPE ODDS ###

def get_ceasers():
    props = ['Total Passing Yards','Total Passing Completions','Total Passing Attempts','Total Receiving Yards','Total Rushing Yards','Total Receptions']
    proplist = []
    NFL_URL =  'https://api.americanwagering.com/regions/ca/locations/on/brands/czr/sb/v3/sports/americanfootball/events/schedule/?competitionIds=007d7c61-07a7-4e18-bb40-15104b6eac92'
    NFL_REQUEST = requests.get(NFL_URL).json()
    for game in NFL_REQUEST['competitions'][0]['events']:
        try:
            EVENT_URL = 'https://api.americanwagering.com/regions/ca/locations/on/brands/czr/sb/v3/events/'+str(game['id'])
            EVENT_REQUEST = requests.get(EVENT_URL).json()
            for prop in EVENT_REQUEST['markets']:
                #print (prop['name'])
                if prop['display'] == True and re.compile('|'.join(props),re.IGNORECASE).search(prop['name']):
                    odds_over =  (prop['selections'][0]['price']['d'])
                    odds_under = (prop['selections'][1]['price']['d'])
                    american_over = (prop['selections'][0]['price']['a'])
                    american_under = (prop['selections'][1]['price']['a'])
                    prob_over = convert_odds(odds_over)
                    prob_under = convert_odds(odds_under)
                    proplist.append([prop['metadata']['marketCategory'], prop['name'].split("|")[1].strip() , prop['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
        except:
            next


    odds_df = pd.DataFrame(proplist, columns=['PROP','NAME','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ','AMERICANOVER_CZ','AMERICANUNDER_CZ','OVERIMPLIED_CZ', 'UNDERIMPLIED_CZ'])
    odds_df = fix_names(odds_df)
    odds_df = rename_cz(odds_df)
    return odds_df

def get_fanduel():
    proplist = []
    NFL_URL =  'https://canada.sportsbook.fanduel.com/cache/psmg/UK/70694.3.json'
    NFL_REQUEST = requests.get(NFL_URL).json()
    #f = open('test.json')
    #MLB_REQUEST = json.load(f)
    for game in NFL_REQUEST['events']:
            EVENT_URL = 'https://canada.sportsbook.fanduel.com/cache/psevent/UK/1/false/'+str(game['idfoevent'])+'.json'
            #EVENT_URL = 'https://canada.sportsbook.fanduel.com/cache/psevent/UK/1/false/'+str('1196248.3')+'.json'
            EVENT_REQUEST = requests.get(EVENT_URL).json()
            try:
                for prop in EVENT_REQUEST['eventmarketgroups'][2]['markets']:
                    if  prop['BB'] == False and 'Alt' not in prop['name']:
                        odds_over =  round((prop['selections'][0]['currentpriceup']/prop['selections'][0]['currentpricedown'])+1,2)
                        odds_under = round((prop['selections'][1]['currentpriceup']/prop['selections'][1]['currentpricedown'])+1,2)
                        if prop['selections'][0]['currentpriceup'] > prop['selections'][0]['currentpricedown']:
                            american_over = round((prop['selections'][0]['currentpriceup']/prop['selections'][0]['currentpricedown'])*100,2)
                        else:
                            american_over = round((prop['selections'][0]['currentpricedown']/prop['selections'][0]['currentpriceup'])*-100,2)
                        if prop['selections'][1]['currentpriceup'] > prop['selections'][1]['currentpricedown']:
                            american_under = round((prop['selections'][1]['currentpriceup']/prop['selections'][1]['currentpricedown'])*100,2)
                        else:
                            american_under = round((prop['selections'][1]['currentpricedown']/prop['selections'][1]['currentpriceup'])*-100,2)                    
                        #prob_over = convert_odds((prop['selections'][0]['currentpriceup']/prop['selections'][0]['currentpricedown'])+1)
                        #prob_under = convert_odds((prop['selections'][1]['currentpriceup']/prop['selections'][1]['currentpricedown'])+1)
                        prob_over = convert_odds(odds_over)
                        prob_under = convert_odds(odds_under)
                        #proplist.append([prop['name'].split("-")[0].strip() , prop['selections'][0]['currenthandicap'] ,  odds_over ,  odds_under , prob_over , prob_under ])
                        proplist.append([prop['externaldescription'].split("-")[1].strip(), prop['externaldescription'].split("-")[0].strip() , prop['selections'][0]['currenthandicap'] ,  odds_over, odds_under, american_over ,  american_under , prob_over , prob_under ])
            except:
                next
    odds_df = pd.DataFrame(proplist, columns=['PROP','NAME','LINE_FD','OVERODDS_FD','UNDERODDS_FD', 'AMERICANOVER_FD', 'AMERICANUNDER_FD', 'OVERIMPLIED_FD', 'UNDERIMPLIED_FD'])
    odds_df = fix_names(odds_df)
    odds_df = rename_fd(odds_df)
    return odds_df

def get_dk():
    proplist = []
    NFL_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v5/eventgroups/88808/categories/1000/subcategories/9524?format=json'
    NFL_REQUEST = requests.get(NFL_URL).json()

    for events in NFL_REQUEST['eventGroup']['offerCategories']:
        if 'Passing Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors']: #5,7
                if 'Pass Yds' in event['name']:
                    try:
                        for prop in event['offerSubcategory']['offers']:
                            for player in prop:
                                odds_over =  (player['outcomes'][0]['oddsDecimal'])
                                odds_under = (player['outcomes'][1]['oddsDecimal'])
                                american_over =  (player['outcomes'][0]['oddsAmerican'])
                                american_under = (player['outcomes'][1]['oddsAmerican'])
                                prob_over = convert_odds(odds_over)
                                prob_under = convert_odds(odds_under)
                                proplist.append([0,player['outcomes'][0]['participant'] , player['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                        next
                        
    NFL_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v5/eventgroups/88808/categories/1000/subcategories/9522?format=json'
    NFL_REQUEST = requests.get(NFL_URL).json()

    for events in NFL_REQUEST['eventGroup']['offerCategories']:
        if 'Passing Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors']: #5,7
                if 'Pass Completions' in event['name']:
                    try:
                        for prop in event['offerSubcategory']['offers']:
                            for player in prop:
                                odds_over =  (player['outcomes'][0]['oddsDecimal'])
                                odds_under = (player['outcomes'][1]['oddsDecimal'])
                                american_over =  (player['outcomes'][0]['oddsAmerican'])
                                american_under = (player['outcomes'][1]['oddsAmerican'])
                                prob_over = convert_odds(odds_over)
                                prob_under = convert_odds(odds_under)
                                proplist.append([4,player['outcomes'][0]['participant'] , player['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                            next

    NFL_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v5/eventgroups/88808/categories/1000/subcategories/9517?format=json'
    NFL_REQUEST = requests.get(NFL_URL).json()

    for events in NFL_REQUEST['eventGroup']['offerCategories']:
        if 'Passing Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors']:
                if 'Pass Attempts' in event['name']:
                    try:
                        for prop in event['offerSubcategory']['offers']:
                            for player in prop:
                                odds_over =  (player['outcomes'][0]['oddsDecimal'])
                                odds_under = (player['outcomes'][1]['oddsDecimal'])
                                american_over =  (player['outcomes'][0]['oddsAmerican'])
                                american_under = (player['outcomes'][1]['oddsAmerican'])
                                prob_over = convert_odds(odds_over)
                                prob_under = convert_odds(odds_under)
                                proplist.append([6,player['outcomes'][0]['participant'] , player['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                        next

    NFL_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v5/eventgroups/88808/categories/1001/subcategories/9514?format=json'
    NFL_REQUEST = requests.get(NFL_URL).json()

    for events in NFL_REQUEST['eventGroup']['offerCategories']:
        if 'Rush/Rec Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors']:
                if 'Rush Yds' in event['name']:
                    try:
                        for prop in event['offerSubcategory']['offers']:
                            for player in prop:
                                odds_over =  (player['outcomes'][0]['oddsDecimal'])
                                odds_under = (player['outcomes'][1]['oddsDecimal'])
                                american_over =  (player['outcomes'][0]['oddsAmerican'])
                                american_under = (player['outcomes'][1]['oddsAmerican'])
                                prob_over = convert_odds(odds_over)
                                prob_under = convert_odds(odds_under)
                                proplist.append([1,player['outcomes'][0]['participant'] , player['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                        next

    NFL_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v5/eventgroups/88808/categories/1001/subcategories/9512?format=json'
    NFL_REQUEST = requests.get(NFL_URL).json()

    for events in NFL_REQUEST['eventGroup']['offerCategories']:
        if 'Rush/Rec Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors']:
                if 'Rec Yds' in event['name']:
                    try:
                        for prop in event['offerSubcategory']['offers']:
                            for player in prop:
                                odds_over =  (player['outcomes'][0]['oddsDecimal'])
                                odds_under = (player['outcomes'][1]['oddsDecimal'])
                                american_over =  (player['outcomes'][0]['oddsAmerican'])
                                american_under = (player['outcomes'][1]['oddsAmerican'])
                                prob_over = convert_odds(odds_over)
                                prob_under = convert_odds(odds_under)
                                proplist.append([2,player['outcomes'][0]['participant'] , player['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                        next

    NFL_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v5/eventgroups/88808/categories/1001/subcategories/9519?format=json'
    NFL_REQUEST = requests.get(NFL_URL).json()

    for events in NFL_REQUEST['eventGroup']['offerCategories']:
        if 'Rush/Rec Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors']:
                if 'Receptions' in event['name']:
                    try:
                        for prop in event['offerSubcategory']['offers']:
                            for player in prop:
                                odds_over =  (player['outcomes'][0]['oddsDecimal'])
                                odds_under = (player['outcomes'][1]['oddsDecimal'])
                                american_over =  (player['outcomes'][0]['oddsAmerican'])
                                american_under = (player['outcomes'][1]['oddsAmerican'])
                                prob_over = convert_odds(odds_over)
                                prob_under = convert_odds(odds_under)
                                proplist.append([5,player['outcomes'][0]['participant'] , player['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                        next

    odds_df = pd.DataFrame(proplist, columns=['PROP','NAME','LINE_DK','OVERODDS_DK','UNDERODDS_DK','AMERICANOVER_DK','AMERICANUNDER_DK','OVERIMPLIED_DK', 'UNDERIMPLIED_DK'])
    odds_df = fix_names(odds_df)

    return odds_df

def get_mgm():
    props = ['Receiving Props','Rushing Props','Quarterback Props']
    proplist = []
    NFL_URL = 'https://sports.on.betmgm.ca/cds-api/bettingoffer/fixtures?x-bwin-accessid=MzViOTU5Y2EtNzgyMy00ZTBmLThkNDctYjRlYjgwNjMwZDQy&lang=en-us&country=CA&userCountry=CA&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds=11&regionIds=9&competitionIds=35&conferenceIds=&skip=0&take=50&sortBy=Tags'
    #myobj = {"sportId":"1","minOdds":"1.01","maxOdds":"10","gridGroupId":"8utzsqlcq","competitionIds":"10137,5909,9141,9142,9139,9143,9140,9144,75,1363,3361,21107,1364,1393,1362,9181,1688,10297,5971,6740,6741,7405,36565,52669,12072,74844,44504,43993,39492,29695,45869,14195,76019,75050,7706,75510,72807,9348,9149,75163,75242"}
    #MLB_REQUEST = requests.post(MLB_URL, json = myobj).json()
    NFL_REQUEST = requests.get(NFL_URL).json()
    proplist = []
    for game in NFL_REQUEST['fixtures']:
        try:
            EVENT_URL = 'https://sports.on.betmgm.ca/cds-api/bettingoffer/fixture-view?x-bwin-accessid=MzViOTU5Y2EtNzgyMy00ZTBmLThkNDctYjRlYjgwNjMwZDQy&lang=en-us&country=CA&userCountry=CA&offerMapping=All&scoreboardMode=Full&fixtureIds='+str(game['id'])+'&state=Latest&includePrecreatedBetBuilder=true&supportVirtual=false&useRegionalisedConfiguration=true'
            EVENT_REQUEST = requests.get(EVENT_URL).json()
            for prop in EVENT_REQUEST['fixture']['games']:
                try:
                    if re.compile('|'.join(props),re.IGNORECASE).search(prop['grouping']['detailed'][0]['name']):
                        odds_over = prop['results'][0]['odds']
                        odds_under = prop['results'][1]['odds']
                        american_over = prop['results'][0]['americanOdds']
                        american_under = prop['results'][1]['americanOdds']
                        prob_over = convert_odds(odds_over)
                        prob_under = convert_odds(odds_under)
                        propvalue = str(prop['grouping']['detailed'][0]['group']) + str(prop['grouping']['detailed'][0]['index']) + str(prop['grouping']['detailed'][0]['subIndex'])
                        proplist.append([propvalue,prop['player1']['short'] , prop['results'][0]['attr'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                except:
                    next
        except:
            next
    odds_df = pd.DataFrame(proplist, columns=['PROP','NAME','LINE_MGM','OVERODDS_MGM','UNDERODDS_MGM','AMERICANOVER_MGM','AMERICANUNDER_MGM','OVERIMPLIED_MGM', 'UNDERIMPLIED_MGM'])
    odds_df = fix_names(odds_df)
    odds_df = rename_mgm(odds_df)
    odds_df['LINE_MGM'] = pd.to_numeric(odds_df['LINE_MGM'])
    return odds_df


def tosql(merged_df):

    pass_yards = merged_df.loc[merged_df['PROP'] == 0]
    pass_yards.drop(columns=['PAATT', 'PACOMP','RUATT','RUYDS','RECCOMP','RECYDS'], inplace=True)
    pass_yards['FD_ODIFF'] = pass_yards.apply(lambda x: round((x['PAYDS']-x['LINE_FD']),2), axis=1)
    pass_yards['FD_UDIFF'] = pass_yards.apply(lambda x: round((x['LINE_FD']-x['PAYDS']),2), axis=1)
    pass_yards['CZ_ODIFF'] = pass_yards.apply(lambda x: round((x['PAYDS']-x['LINE_CZ']),2), axis=1)
    pass_yards['CZ_UDIFF'] = pass_yards.apply(lambda x: round((x['LINE_CZ']-x['PAYDS']),2), axis=1)
    pass_yards['DK_ODIFF'] = pass_yards.apply(lambda x: round((x['PAYDS']-x['LINE_DK']),2), axis=1)
    pass_yards['DK_UDIFF'] = pass_yards.apply(lambda x: round((x['LINE_DK']-x['PAYDS']),2), axis=1)
    pass_yards['MGM_ODIFF'] = pass_yards.apply(lambda x: round((x['PAYDS']-x['LINE_MGM']),2), axis=1)
    pass_yards['MGM_UDIFF'] = pass_yards.apply(lambda x: round((x['LINE_MGM']-x['PAYDS']),2), axis=1)
    pass_yards = pass_yards.rename(columns={"PAYDS": "PROJ"})
    pass_yards.to_sql(con=database_connection, name='passyds', if_exists='replace')

    ru_yards = merged_df.loc[merged_df['PROP'] == 1]
    ru_yards.drop(columns=['PAATT', 'PACOMP','RUATT','PAYDS','RECCOMP','RECYDS'], inplace=True)
    ru_yards['FD_ODIFF'] = ru_yards.apply(lambda x: round((x['RUYDS']-x['LINE_FD']),2), axis=1)
    ru_yards['FD_UDIFF'] = ru_yards.apply(lambda x: round((x['LINE_FD']-x['RUYDS']),2), axis=1)
    ru_yards['CZ_ODIFF'] = ru_yards.apply(lambda x: round((x['RUYDS']-x['LINE_CZ']),2), axis=1)
    ru_yards['CZ_UDIFF'] = ru_yards.apply(lambda x: round((x['LINE_CZ']-x['RUYDS']),2), axis=1)
    ru_yards['DK_ODIFF'] = ru_yards.apply(lambda x: round((x['RUYDS']-x['LINE_DK']),2), axis=1)
    ru_yards['DK_UDIFF'] = ru_yards.apply(lambda x: round((x['LINE_DK']-x['RUYDS']),2), axis=1)
    ru_yards['MGM_ODIFF'] = ru_yards.apply(lambda x: round((x['RUYDS']-x['LINE_MGM']),2), axis=1)
    ru_yards['MGM_UDIFF'] = ru_yards.apply(lambda x: round((x['LINE_MGM']-x['RUYDS']),2), axis=1)
    ru_yards = ru_yards.rename(columns={"RUYDS": "PROJ"})
    ru_yards.to_sql(con=database_connection, name='ruyds', if_exists='replace')

    rec_yards = merged_df.loc[merged_df['PROP'] == 2]
    rec_yards.drop(columns=['PAATT', 'PACOMP','RUATT','PAYDS','RECCOMP','RUYDS'], inplace=True)
    rec_yards['FD_ODIFF'] = rec_yards.apply(lambda x: round((x['RECYDS']-x['LINE_FD']),2), axis=1)
    rec_yards['CZ_ODIFF'] = rec_yards.apply(lambda x: round((x['RECYDS']-x['LINE_CZ']),2), axis=1)
    rec_yards['DK_ODIFF'] = rec_yards.apply(lambda x: round((x['RECYDS']-x['LINE_DK']),2), axis=1)
    rec_yards['MGM_ODIFF'] = rec_yards.apply(lambda x: round((x['RECYDS']-x['LINE_MGM']),2), axis=1)
    rec_yards['FD_UDIFF'] = rec_yards['FD_ODIFF'] * -1
    rec_yards['CZ_UDIFF'] = rec_yards['CZ_ODIFF'] * -1
    rec_yards['DK_UDIFF'] = rec_yards['DK_ODIFF'] * -1
    rec_yards['MGMU_DIFF'] = rec_yards['MGM_ODIFF'] *-1
    rec_yards = rec_yards.rename(columns={"RECYDS": "PROJ"})
    rec_yards.to_sql(con=database_connection, name='recyds', if_exists='replace')    

    pa_comp = merged_df.loc[merged_df['PROP'] == 4]
    pa_comp.drop(columns=['PAATT', 'RECYDS','RUATT','PAYDS','RECCOMP','RUYDS'], inplace=True)
    pa_comp['FD_ODIFF'] = pa_comp.apply(lambda x: round((x['PACOMP']-x['LINE_FD']),2), axis=1)
    pa_comp['CZ_ODIFF'] = pa_comp.apply(lambda x: round((x['PACOMP']-x['LINE_CZ']),2), axis=1)
    pa_comp['DK_ODIFF'] = pa_comp.apply(lambda x: round((x['PACOMP']-x['LINE_DK']),2), axis=1)
    pa_comp['MGM_ODIFF'] = pa_comp.apply(lambda x: round((x['PACOMP']-x['LINE_MGM']),2), axis=1)
    pa_comp['FD_UDIFF'] = pa_comp['FD_ODIFF'] * -1
    pa_comp['CZ_UDIFF'] = pa_comp['CZ_ODIFF'] * -1
    pa_comp['DK_UDIFF'] = pa_comp['DK_ODIFF'] * -1
    pa_comp['MGM_UDIFF'] = pa_comp['MGM_ODIFF'] * -1
    pa_comp = pa_comp.rename(columns={"PACOMP": "PROJ"})
    pa_comp.to_sql(con=database_connection, name='pacomp', if_exists='replace')

    tot_rec = merged_df.loc[merged_df['PROP'] == 5]
    tot_rec.drop(columns=['PAATT', 'RECYDS','RUATT','PAYDS','PACOMP','RUYDS'], inplace=True)
    tot_rec['FD_ODIFF'] = tot_rec.apply(lambda x: round((x['RECCOMP']-x['LINE_FD']),2), axis=1)
    tot_rec['CZ_ODIFF'] = tot_rec.apply(lambda x: round((x['RECCOMP']-x['LINE_CZ']),2), axis=1)
    tot_rec['DK_ODIFF'] = tot_rec.apply(lambda x: round((x['RECCOMP']-x['LINE_DK']),2), axis=1)
    tot_rec['MGM_ODIFF'] = tot_rec.apply(lambda x: round((x['RECCOMP']-x['LINE_MGM']),2), axis=1)
    tot_rec['FD_UDIFF'] = tot_rec['FD_ODIFF'] * -1
    tot_rec['CZ_UDIFF'] = tot_rec['CZ_ODIFF'] * -1
    tot_rec['DK_UDIFF'] = tot_rec['DK_ODIFF'] * -1
    tot_rec['MGM_UDIFF'] = tot_rec['MGM_ODIFF'] * -1
    tot_rec = tot_rec.rename(columns={"RECCOMP": "PROJ"})
    tot_rec.to_sql(con=database_connection, name='totrec', if_exists='replace')

    pass_att = merged_df.loc[merged_df['PROP'] == 6]
    pass_att.drop(columns=['RECCOMP', 'RECYDS','RUATT','PAYDS','PACOMP','RUYDS'], inplace=True)
    pass_att['FD_ODIFF'] = pass_att.apply(lambda x: round((x['PAATT']-x['LINE_FD']),2), axis=1)
    pass_att['CZ_ODIFF'] = pass_att.apply(lambda x: round((x['PAATT']-x['LINE_CZ']),2), axis=1)
    pass_att['DK_ODIFF'] = pass_att.apply(lambda x: round((x['PAATT']-x['LINE_DK']),2), axis=1)
    pass_att['MGM_ODIFF'] = pass_att.apply(lambda x: round((x['PAATT']-x['LINE_MGM']),2), axis=1)
    pass_att['FD_UDIFF'] = pass_att['FD_ODIFF'] * -1
    pass_att['CZ_UDIFF'] = pass_att['CZ_ODIFF'] * -1
    pass_att['DK_UDIFF'] = pass_att['DK_ODIFF'] * -1
    pass_att['MGM_UDIFF'] = pass_att['MGM_ODIFF'] * -1
    pass_att = pass_att.rename(columns={"PAATT": "PROJ"})
    pass_att.to_sql(con=database_connection, name='passatt', if_exists='replace')        

def run():
    roto_df = pd.DataFrame(get_roto_stats())
    roto_df = roto_df.apply(pd.to_numeric, errors='ignore')
    ceasers_df = get_ceasers()
    fanduel_df = get_fanduel()
    dk_df = get_dk()
    dk_df = dk_df.apply(pd.to_numeric, errors='ignore')
    print (dk_df.dtypes)
    mgm_df = get_mgm()
    all_df = fanduel_df.append(ceasers_df)
    all_df = all_df.append(dk_df)
    all_df = all_df.append(mgm_df)
    all_df = all_df.groupby(['PROP', 'NAME'],dropna=False,as_index=False).agg('sum')
    merged_df = pd.merge(all_df,roto_df[['PLAYER','PAATT','PACOMP','PAYDS','RUATT','RUYDS','RECCOMP','RECYDS']], left_on='NAME', right_on='PLAYER',how='left')
    merged_df = merged_df.rename(columns={"AMERICANOVER_CZ": "O_CZ" , "AMERICANUNDER_CZ": "U_CZ"})
    merged_df = merged_df.rename(columns={"AMERICANOVER_FD": "O_FD" , "AMERICANUNDER_FD": "U_FD"})
    merged_df = merged_df.rename(columns={"AMERICANOVER_DK": "O_DK" , "AMERICANUNDER_DK": "U_DK"})
    merged_df = merged_df.rename(columns={"AMERICANOVER_MGM": "O_MGM" , "AMERICANUNDER_MGM": "U_MGM"})
    tosql(merged_df)

    return ()

def test():
    roto_df = pd.DataFrame(get_roto_stats())
    roto_df = roto_df.apply(pd.to_numeric, errors='ignore')
    roto_df.to_csv('roto.csv')

if __name__ == "__main__":
    test()