import json , os , pandas as pd  , requests
from scipy.stats import poisson
import urllib.request
from bs4 import BeautifulSoup as Soup
import sqlalchemy
from datetime import datetime

database_username = 'admin'
database_password = 'Rv301297'
database_ip       = 'database-1.clalyzsfkuqz.us-east-1.rds.amazonaws.com'
database_name     = 'default'



def convert_odds(odds):
    probability = (1/odds)*100
    return round(probability,2)

def get_fanduel():
    proplist = []
    MLB_URL =  'https://canada.sportsbook.fanduel.com/cache/psmg/UK/71916.3.json'
    MLB_REQUEST = requests.get(MLB_URL).json()
    #f = open('test.json')
    #MLB_REQUEST = json.load(f)
    for game in MLB_REQUEST['events']:
        try:
            EVENT_URL = 'https://canada.sportsbook.fanduel.com/cache/psevent/UK/1/false/'+str(game['idfoevent'])+'.json'
            EVENT_REQUEST = requests.get(EVENT_URL).json()
            #f2 = open('test2.json')
            #EVENT_REQUEST = json.load(f2)
            for prop in EVENT_REQUEST['eventmarketgroups'][5]['markets']:
                if 'Strike' in prop['name'] and 'Alt' not in  prop['name']:
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
                    proplist.append([prop['name'].split("-")[0].strip() , prop['selections'][0]['currenthandicap'] ,  odds_over, odds_under, american_over ,  american_under , prob_over , prob_under ])
        except:
            next
    odds_df = pd.DataFrame(proplist, columns=['NAME','LINE_FD','OVERODDS_FD','UNDERODDS_FD', 'AMERICANOVER_FD', 'AMERICANUNDER_FD', 'OVERIMPLIED_FD', 'UNDERIMPLIED_FD'])
    #odds_df.to_csv('fd.csv')
    odds_df.replace('Matthew Swarmer','Matt Swarmer', inplace=True)
    odds_df = fix_names(odds_df)
    return odds_df

def get_dk():
    proplist = []
    MLB_URL =  'https://sportsbook-ca-on.draftkings.com//sites/CA-ON-SB/api/v4/eventgroups/88670847/categories/1031/subcategories/9885?format=json'
    MLB_REQUEST = requests.get(MLB_URL).json()

    for events in MLB_REQUEST['eventGroup']['offerCategories']:
        if 'Pitcher Props' in  events['name']:
            for event in events['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']: #5,7
                    try:
                        for prop in event:
                            odds_over =  (prop['outcomes'][0]['oddsDecimal'])
                            odds_under = (prop['outcomes'][1]['oddsDecimal'])
                            american_over =  (prop['outcomes'][0]['oddsAmerican'])
                            american_under = (prop['outcomes'][1]['oddsAmerican'])
                            prob_over = convert_odds(odds_over)
                            prob_under = convert_odds(odds_under)
                            proplist.append([prop['outcomes'][0]['participant'] , prop['outcomes'][0]['line'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
                    except:
                        next

    odds_df = pd.DataFrame(proplist, columns=['NAME','LINE_DK','OVERODDS_DK','UNDERODDS_DK','AMERICANOVER_DK','AMERICANUNDER_DK','OVERIMPLIED_DK', 'UNDERIMPLIED_DK'])
    odds_df.replace('Luis Garcia (HOU)','Luis Garcia', inplace=True)
    odds_df = fix_names(odds_df)
    return odds_df

def get_mgm():
    proplist = []
    MLB_URL = 'https://sports.on.betmgm.ca/cds-api/random-multi-generator/random-events?x-bwin-accessid=MzViOTU5Y2EtNzgyMy00ZTBmLThkNDctYjRlYjgwNjMwZDQy&lang=en-us&country=CA&userCountry=CA'
    myobj = {"sportId":"23","minOdds":"1.01","maxOdds":"10","gridGroupId":"8utzsqlcq","competitionIds":"10137,5909,9141,9142,9139,9143,9140,9144,75,1363,3361,21107,1364,1393,1362,9181,1688,10297,5971,6740,6741,7405,36565,52669,12072,74844,44504,43993,39492,29695,45869,14195,76019,75050,7706,75510,72807,9348,9149,75163,75242"}
    MLB_REQUEST = requests.post(MLB_URL, json = myobj).json()
    proplist = []
    for game in MLB_REQUEST['fixtures']:
        try:
            EVENT_URL = 'https://sports.on.betmgm.ca/cds-api/bettingoffer/fixture-view?x-bwin-accessid=MzViOTU5Y2EtNzgyMy00ZTBmLThkNDctYjRlYjgwNjMwZDQy&lang=en-us&country=CA&userCountry=CA&offerMapping=All&scoreboardMode=Full&fixtureIds='+str(game['id'])+'&state=Latest&includePrecreatedBetBuilder=true&supportVirtual=false&useRegionalisedConfiguration=true'
            EVENT_REQUEST = requests.get(EVENT_URL).json()
            for prop in EVENT_REQUEST['fixture']['games']:
                if 'How many strikeouts' in prop['name']['value']:
                    odds_over = prop['results'][0]['odds']
                    odds_under = prop['results'][1]['odds']
                    american_over = prop['results'][0]['americanOdds']
                    american_under = prop['results'][1]['americanOdds']
                    prob_over = convert_odds(odds_over)
                    prob_under = convert_odds(odds_under)
                    proplist.append([prop['player1']['short'] , prop['results'][0]['attr'] ,  odds_over ,  odds_under , american_over, american_under,  prob_over , prob_under ])
        except:
            next
    odds_df = pd.DataFrame(proplist, columns=['NAME','LINE_MGM','OVERODDS_MGM','UNDERODDS_MGM','AMERICANOVER_MGM','AMERICANUNDER_MGM','OVERIMPLIED_MGM', 'UNDERIMPLIED_MGM'])
    odds_df.replace('Luis Garcia (HOU)','Luis Garcia', inplace=True)
    odds_df.replace('Frambler Valdez', 'Framber Valdez', inplace=True)
    odds_df = fix_names(odds_df)
    return odds_df


def agg(thebat_df,razz_df):
    merged_df = fix_names(thebat_df)
    razz_df = fix_names(razz_df)
    #team_l = pd.read_csv('Team_L.csv')
    #team_r = pd.read_csv('Team_R.csv')
    #merged_df =  pd.merge(thebat_df,razz_df[['Name','K','IP']],left_on='NAME', right_on='Name')
    #merged_df = pd.merge(merged_df,team_l[['Team','K%']], left_on='OPP', right_on='Team')
    #merged_df = pd.merge(merged_df,team_r[['Team','K%']], left_on='OPP', right_on='Team')
    #merged_df = merged_df.rename(columns={"K%_x": "K% vs. L","K%_y": "K% vs. R"})
    #merged_df = merged_df[['Name','OL','K_x','K_y','IP_x','IP_y','PPC','OPP','HAND','K% vs. L','K% vs. R']]
    if 'OL' not in merged_df.columns:
        merged_df['OL'] = 'False'
    merged_df = merged_df[['NAME','OL','K','IP','PPC','OPP','HAND']]
    #merged_df['K'] = merged_df.apply(lambda x: round((x['K_x']+x['K_y'])/2,2), axis=1)
    #merged_df['IP_x'] = merged_df['IP_x'] * 3
    #merged_df['IP_y'] = merged_df['IP_y'] * 3
    #merged_df['OUTS'] = merged_df.apply(lambda x: round((x['IP_x']+x['IP_y'])/2,2), axis=1)
    merged_df = merged_df.rename(str.upper, axis='columns')
    merged_df = merged_df.astype({'K': 'float64'})
    return merged_df
    
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                           format(database_username, database_password, 
                                                  database_ip, database_name))

def create_finaldk(dk_df,agg_df):
    #merged_df = pd.merge(fd_df,cz_df,on='NAME', how='inner')
    #merged_df = pd.merge(merged_df,dk_df,on='NAME', how='left')
    final_df =  pd.merge(dk_df,agg_df,on='NAME', how='left')
    final_df = final_df.rename(columns={"OL": "LINEUP"})
    final_df['OVERPOISSON_DK'] = 1- final_df.apply(lambda x: round(poisson.cdf(x['LINE_DK'],x['K']),2) , axis = 1 )
    final_df['UNDERPOISSON_DK'] = final_df.apply(lambda x: round(poisson.cdf(x['LINE_DK'],x['K']),2) , axis = 1 )
    final_df['EVOVER_DK'] = final_df.apply(lambda x: round((((100*x['OVERODDS_DK'])-100)*x['OVERPOISSON_DK'])+(-100*(1-x['OVERPOISSON_DK'])),2), axis=1)
    final_df['EVUNDER_DK'] = final_df.apply(lambda x: round((((100*x['UNDERODDS_DK'])-100)*x['UNDERPOISSON_DK'])+(-100*(1-x['UNDERPOISSON_DK'])),2), axis=1)
    final_df['KELLYOVER_DK'] = final_df.apply(lambda x: round(250*(((x['OVERPOISSON_DK']*x['OVERODDS_DK'])-1)/(x['OVERODDS_DK']-1)),2) , axis=1)
    final_df['KELLYUNDER_DK'] = final_df.apply(lambda x: round(250*(((x['UNDERPOISSON_DK']*x['UNDERODDS_DK'])-1)/(x['UNDERODDS_DK']-1)),2) , axis=1)
    #final_df = final_df[['NAME','K','LINE_FD','OVERODDS_FD','UNDERODDS_FD','EVOVER_FD','EVUNDER_FD','KELLYOVER_FD','KELLYUNDER_FD','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ','EVOVER_CZ','EVUNDER_CZ','KELLYOVER_CZ','KELLYUNDER_CZ']]
    #final_df = final_df[['NAME','K','LINEUP','LINE_FD','OVERODDS_FD','UNDERODDS_FD', 'KELLYOVER_FD','KELLYUNDER_FD','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ', 'KELLYOVER_CZ','KELLYUNDER_CZ']]
    final_df = final_df[['NAME','K','PPC','OPP','HAND','LINEUP','LINE_DK','AMERICANOVER_DK','AMERICANUNDER_DK', 'KELLYOVER_DK','KELLYUNDER_DK']]
    final_df.drop_duplicates(subset ="NAME",
                     keep = 'first', inplace = True)
    #                 
    #final_df.to_sql(con=database_connection, name='DK', if_exists='replace')
    return final_df

def create_finalfd(fd_df,agg_df):
    #merged_df = pd.merge(fd_df,cz_df,on='NAME', how='inner')
    #merged_df = pd.merge(merged_df,dk_df,on='NAME', how='left')
    final_df =  pd.merge(fd_df,agg_df,on='NAME', how='left')
    final_df = final_df.rename(columns={"OL": "LINEUP"})
    final_df['OVERPOISSON_FD'] = 1- final_df.apply(lambda x: round(poisson.cdf(x['LINE_FD'],x['K']),2) , axis = 1 )
    final_df['UNDERPOISSON_FD'] = final_df.apply(lambda x: round(poisson.cdf(x['LINE_FD'],x['K']),2) , axis = 1 )
    final_df['EVOVER_FD'] = final_df.apply(lambda x: round((((100*x['OVERODDS_FD'])-100)*x['OVERPOISSON_FD'])+(-100*(1-x['OVERPOISSON_FD'])),2), axis=1)
    final_df['EVUNDER_FD'] = final_df.apply(lambda x: round((((100*x['UNDERODDS_FD'])-100)*x['UNDERPOISSON_FD'])+(-100*(1-x['UNDERPOISSON_FD'])),2), axis=1)
    final_df['KELLYOVER_FD'] = final_df.apply(lambda x: round(250*(((x['OVERPOISSON_FD']*x['OVERODDS_FD'])-1)/(x['OVERODDS_FD']-1)),2) , axis=1)
    final_df['KELLYUNDER_FD'] = final_df.apply(lambda x: round(250*(((x['UNDERPOISSON_FD']*x['UNDERODDS_FD'])-1)/(x['UNDERODDS_FD']-1)),2) , axis=1)

    #final_df = final_df[['NAME','K','LINE_FD','OVERODDS_FD','UNDERODDS_FD','EVOVER_FD','EVUNDER_FD','KELLYOVER_FD','KELLYUNDER_FD','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ','EVOVER_CZ','EVUNDER_CZ','KELLYOVER_CZ','KELLYUNDER_CZ']]
    #final_df = final_df[['NAME','K','LINEUP','LINE_FD','OVERODDS_FD','UNDERODDS_FD', 'KELLYOVER_FD','KELLYUNDER_FD','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ', 'KELLYOVER_CZ','KELLYUNDER_CZ']]
    final_df = final_df[['NAME','K','PPC','LINEUP','OPP','HAND','LINE_FD','AMERICANOVER_FD','AMERICANUNDER_FD', 'KELLYOVER_FD','KELLYUNDER_FD']]
    final_df.drop_duplicates(subset ="NAME",
                     keep = 'first', inplace = True)
    #final_df.to_sql(con=database_connection, name='FD', if_exists='replace')
    return final_df

def create_finalmgm(mgm_df,agg_df):
    #merged_df = pd.merge(fd_df,cz_df,on='NAME', how='inner')
    #merged_df = pd.merge(merged_df,dk_df,on='NAME', how='left')
    final_df =  pd.merge(mgm_df,agg_df,on='NAME', how='left')
    final_df = final_df.rename(columns={"OL": "LINEUP"})
    final_df["LINE_MGM"] = pd.to_numeric(final_df["LINE_MGM"])
    #print (final_df.dtypes)
    final_df['OVERPOISSON_MGM'] = 1- final_df.apply(lambda x: round(poisson.cdf(x['LINE_MGM'],x['K']),2) , axis = 1 )
    final_df['UNDERPOISSON_MGM'] = final_df.apply(lambda x: round(poisson.cdf(x['LINE_MGM'],x['K']),2) , axis = 1 )
    final_df['EVOVER_MGM'] = final_df.apply(lambda x: round((((100*x['OVERODDS_MGM'])-100)*x['OVERPOISSON_MGM'])+(-100*(1-x['OVERPOISSON_MGM'])),2), axis=1)
    final_df['EVUNDER_MGM'] = final_df.apply(lambda x: round((((100*x['UNDERODDS_MGM'])-100)*x['UNDERPOISSON_MGM'])+(-100*(1-x['UNDERPOISSON_MGM'])),2), axis=1)
    final_df['KELLYOVER_MGM'] = final_df.apply(lambda x: round(250*(((x['OVERPOISSON_MGM']*x['OVERODDS_MGM'])-1)/(x['OVERODDS_MGM']-1)),2) , axis=1)
    final_df['KELLYUNDER_MGM'] = final_df.apply(lambda x: round(250*(((x['UNDERPOISSON_MGM']*x['UNDERODDS_MGM'])-1)/(x['UNDERODDS_MGM']-1)),2) , axis=1)

    #final_df = final_df[['NAME','K','LINE_MGM','OVERODDS_MGM','UNDERODDS_MGM','EVOVER_MGM','EVUNDER_MGM','KELLYOVER_MGM','KELLYUNDER_MGM','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ','EVOVER_CZ','EVUNDER_CZ','KELLYOVER_CZ','KELLYUNDER_CZ']]
    #final_df = final_df[['NAME','K','LINEUP','LINE_MGM','OVERODDS_MGM','UNDERODDS_MGM', 'KELLYOVER_MGM','KELLYUNDER_MGM','LINE_CZ','OVERODDS_CZ','UNDERODDS_CZ', 'KELLYOVER_CZ','KELLYUNDER_CZ']]
    final_df = final_df[['NAME','K','PPC','LINEUP','OPP','HAND','LINE_MGM','AMERICANOVER_MGM','AMERICANUNDER_MGM', 'KELLYOVER_MGM','KELLYUNDER_MGM']]
    final_df.drop_duplicates(subset ="NAME",
                     keep = 'first', inplace = True)
    #final_df.to_sql(con=database_connection, name='FD', if_exists='replace')
    return final_df

def fix_names(df):
    dict = {
    'Hyun' : 'Hyun Jin Ryu',
    'Hyun-Jin Ryu' : 'Hyun Jin Ryu',
    'Luis Garcia (HOU)' : 'Luis Garcia',
    'Jonathan Heasley' : 'Jon Heasley',
    'Matthew Swarmer' : 'Matt Swarmer',
    'Frambler Valdez' : 'Framber Valdez'
     }
     
    df2=df.replace({"NAME": dict})
    df2=df.replace({"Name": dict})
    return df2

def get_roto_stats():
    if datetime.now() >= datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) and datetime.now() <= datetime.today().replace(hour=9, minute=0, second=0, microsecond=0) :
        roto_url = "https://rotogrinders.com/grids/tomorrow-projections-the-bat-x-3375509?site=draftkings"
    else:
        roto_url = "https://rotogrinders.com/grids/standard-projections-the-bat-x-3372510?site=draftkings"
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
    return df

razz_url = "https://razzball.com/dfsbot-draftkings-pitch/"
razz_hdr = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
    "Cookie": "wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_6287f1ba5b8ab84494a2ba59fda95484=csmaniac%7C1681950144%7CHJNKbuH1fWLtkXcimPRdCgJsxqEsxR6xmCJRSthMJLU%7Cb3fbdded4c708782455a44df3aa1c910137afe0cf4e4979fe9966f5963852fa2"  }
razz_table_id = "neorazzstatstable"

    
def get_razz_stats():
    req = urllib.request.Request(razz_url, headers=razz_hdr)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    #soup = Soup(html, "html5lib")
    soup = Soup(html)
    htmltable = soup.find(id=razz_table_id)

    rows = htmltable.find_all("tr")
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
            final_data.append({ "Name": columns[1].text, "team": columns[2].text, "K": columns[14].text, "IP": columns[11].text })
    df = pd.DataFrame(final_data)
    return df

def tosql(agg_df,final_dffd,final_dfdk,final_dfmgm):
    sql_df = pd.merge(agg_df,final_dffd, how='left')
    sql_df = pd.merge(sql_df,final_dfdk, left_on='NAME', right_on='NAME' , how='left')
    sql_df = pd.merge(sql_df,final_dfmgm, left_on='NAME', right_on='NAME' , how='left')
    sql_df.drop_duplicates(subset ="NAME",
                     keep = 'first', inplace = True)
    sql_df.drop(columns=['K_y', 'PPC_y','OPP_y','HAND_y','LINEUP_y'], inplace=True)
    sql_df = sql_df.rename(columns={"K_x": "K" , "PPC_x": "PPC" , "OPP_x": "OPP", "HAND_x": "HAND", "LINEUP_x": "LINEUP"})
    sql_df = sql_df.rename(columns={"AMERICANOVER_DK": "O_DK" , "AMERICANUNDER_DK": "U_DK" , "KELLYOVER_DK": "KO_DK", "KELLYUNDER_DK": "KU_DK"})
    sql_df = sql_df.rename(columns={"AMERICANOVER_FD": "O_FD" , "AMERICANUNDER_FD": "U_FD" , "KELLYOVER_FD": "KO_FD", "KELLYUNDER_FD": "KU_FD"})
    sql_df.dropna(subset=['LINE_FD', 'LINE_DK'], how='all', inplace=True)
    sql_df.to_sql(con=database_connection, name='DK', if_exists='replace')    
    

def run():
    roto_df = pd.DataFrame(get_roto_stats())
    razz_df = pd.DataFrame()
    fd_df = get_fanduel()
    dk_df = get_dk()
    mgm_df = get_mgm()
    agg_df = agg(roto_df,razz_df)
    final_dffd = create_finalfd(fd_df,agg_df)
    final_dfdk = create_finaldk(dk_df,agg_df)
    final_dfmgm = create_finalmgm(mgm_df,agg_df)
    tosql(agg_df,final_dffd,final_dfdk,final_dfmgm)

    return ()