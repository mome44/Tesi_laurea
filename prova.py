import pandas as pd
import requests
from urllib.parse import urlparse, unquote
import json
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from functools import lru_cache
import time
import random
import os


#Constants

FILE_NAME = 'test'
NUM_WORKERS= 14

NATION_MAP = {
    'afghan': 'Afghanistan',
    'albanian': 'Albania',
    'algerian': 'Algeria',
    'american': 'USA',
    'andorran': 'Andorra',
    'angolan': 'Angola',
    'argentine': 'Argentina',
    'armenian': 'Armenia',
    'australian': 'Australia',
    'austrian': 'Austria',
    'azerbaijani': 'Azerbaijan',
    'bahraini': 'Bahrain',
    'bangladeshi': 'Bangladesh',
    'belarusian': 'Belarus',
    'belgian': 'Belgium',
    'belizean': 'Belize',
    'beninese': 'Benin',
    'bhutanese': 'Bhutan',
    'bolivian': 'Bolivia',
    'bosnian': 'Bosnia and Herzegovina',
    'botswanan': 'Botswana',
    'brazilian': 'Brazil',
    'british': 'United Kingdom',
    'bruneian': 'Brunei',
    'bulgarian': 'Bulgaria',
    'burkinabe': 'Burkina Faso',
    'burmese': 'Myanmar',
    'burundian': 'Burundi',
    'cambodian': 'Cambodia',
    'cameroonian': 'Cameroon',
    'canadian': 'Canada',
    'cape verdean': 'Cape Verde',
    'central african': 'Central African Republic',
    'chadian': 'Chad',
    'chilean': 'Chile',
    'chinese': 'China',
    'colombian': 'Colombia',
    'congolese': 'Congo',
    'croatian': 'Croatia',
    'cuban': 'Cuba',
    'cypriot': 'Cyprus',
    'czech': 'Czech Republic',
    'danish': 'Denmark',
    'djiboutian': 'Djibouti',
    'dominican': 'Dominican Republic',
    'dutch': 'Netherlands',
    'ecuadorean': 'Ecuador',
    'egyptian': 'Egypt',
    'emirati': 'United Arab Emirates',
    'english': 'United Kingdom',
    'equatoguinean': 'Equatorial Guinea',
    'eritrean': 'Eritrea',
    'estonian': 'Estonia',
    'ethiopian': 'Ethiopia',
    'fijian': 'Fiji',
    'filipino': 'Philippines',
    'finnish': 'Finland',
    'french': 'France',
    'gabonese': 'Gabon',
    'gambian': 'Gambia',
    'georgian': 'Georgia',
    'german': 'Germany',
    'ghanaian': 'Ghana',
    'greek': 'Greece',
    'guatemalan': 'Guatemala',
    'guinean': 'Guinea',
    'haitian': 'Haiti',
    'honduran': 'Honduras',
    'hungarian': 'Hungary',
    'icelandic': 'Iceland',
    'indian': 'India',
    'indonesian': 'Indonesia',
    'iranian': 'Iran',
    'iraqi': 'Iraq',
    'irish': 'Ireland',
    'israeli': 'Israel',
    'italian': 'Italy',
    'jamaican': 'Jamaica',
    'japanese': 'Japan',
    'jordanian': 'Jordan',
    'kazakh': 'Kazakhstan',
    'kenyan': 'Kenya',
    'korean': 'South Korea',
    'kuwaiti': 'Kuwait',
    'kyrgyz': 'Kyrgyzstan',
    'laotian': 'Laos',
    'latvian': 'Latvia',
    'lebanese': 'Lebanon',
    'liberian': 'Liberia',
    'libyan': 'Libya',
    'lithuanian': 'Lithuania',
    'luxembourgish': 'Luxembourg',
    'macedonian': 'North Macedonia',
    'malagasy': 'Madagascar',
    'malawian': 'Malawi',
    'malaysian': 'Malaysia',
    'maldivian': 'Maldives',
    'malian': 'Mali',
    'maltese': 'Malta',
    'mauritanian': 'Mauritania',
    'mauritian': 'Mauritius',
    'mexican': 'Mexico',
    'moldovan': 'Moldova',
    'mongolian': 'Mongolia',
    'moroccan': 'Morocco',
    'mozambican': 'Mozambique',
    'namibian': 'Namibia',
    'nepalese': 'Nepal',
    'new zealander': 'New Zealand',
    'nicaraguan': 'Nicaragua',
    'nigerien': 'Niger',
    'nigerian': 'Nigeria',
    'north korean': 'North Korea',
    'norwegian': 'Norway',
    'omani': 'Oman',
    'pakistani': 'Pakistan',
    'palestinian': 'Palestine',
    'panamanian': 'Panama',
    'paraguayan': 'Paraguay',
    'peruvian': 'Peru',
    'polish': 'Poland',
    'portuguese': 'Portugal',
    'qatari': 'Qatar',
    'romanian': 'Romania',
    'russian': 'Russia',
    'rwandan': 'Rwanda',
    'saudi': 'Saudi Arabia',
    'scottish': 'United Kingdom',
    'senegalese': 'Senegal',
    'serbian': 'Serbia',
    'sierra leonean': 'Sierra Leone',
    'singaporean': 'Singapore',
    'slovak': 'Slovakia',
    'slovenian': 'Slovenia',
    'somali': 'Somalia',
    'south african': 'South Africa',
    'spanish': 'Spain',
    'sri lankan': 'Sri Lanka',
    'sudanese': 'Sudan',
    'surinamese': 'Suriname',
    'swazi': 'Eswatini',
    'swedish': 'Sweden',
    'swiss': 'Switzerland',
    'syrian': 'Syria',
    'taiwanese': 'Taiwan',
    'tajik': 'Tajikistan',
    'tanzanian': 'Tanzania',
    'thai': 'Thailand',
    'togolese': 'Togo',
    'tunisian': 'Tunisia',
    'turkish': 'Turkey',
    'ugandan': 'Uganda',
    'ukrainian': 'Ukraine',
    'uruguayan': 'Uruguay',
    'uzbek': 'Uzbekistan',
    'venezuelan': 'Venezuela',
    'vietnamese': 'Vietnam',
    'welsh': 'United Kingdom',
    'yemeni': 'Yemen',
    'zambian': 'Zambia',
    'zimbabwean': 'Zimbabwe'
}

LANG_MAP = {
        'zh_yue': 'zh-yue',        
        'be_x_old': 'be-tarask',     
        'simple': 'en',       
        'roa_rup': 'roa-rup',     
        'nds_nl': 'nds-nl', 
        'bat_smg': 'bat-smg', 
        'zh_min_nan': 'zh-min-nan',
        'zh_classical': 'zh', 
        'roa_tara': 'roa-tara',
        'fiu_vro': 'fiu-vro',
        'cbk_zam': 'cbk-zam',
        'map_bms': 'map-bms'
    }

LANG_MAP_2 = {
        'zh_yue': 'zh-yue',        
        'be_x_old': 'be-tarask',     
        'simple': 'en',       
        'roa_rup': 'roa-rup',     
        'nds_nl': 'nds-nl', 
        'bat_smg': 'bat-smg', 
        'zh_min_nan': 'zh-min-nan',
        'zh_classical': 'zh', 
        'roa_tara': 'roa-tara',
        'fiu_vro': 'fiu-vro',
        'cbk_zam': 'cbk-zam',
        'map_bms': 'map-bms'
    }

# Utility to extract the page title from a Wikipedia URL
def get_title_from_url(url):
    try:
        return unquote(urlparse(url).path.split('/wiki/')[-1])
    except:
        return None
    
    
def safe_request(session, url, params, retries=3, backoff=2, label=""):
    for attempt in range(retries):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Too Many Requests
                wait_time = backoff * (2 ** attempt) + random.uniform(0, 1)
                print(f"[RETRY] {label} — 429 error, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                print(f"[ERROR] {label} — {e}")
                return None
        except Exception as e:
            print(f"[ERROR] {label} — {e}")
            return None
    return None

#function to extract the first sentence of the english wikipedia page
def extract_first_sentence(text):
    #removing html tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    #geting the first sentence (it could end with .!? followed by a space or a string)
    match = re.search(r'^(.*?[.!?])(?:\s|$)', clean_text)
    if match:
        return match.group(1).strip()
    #if there is no sentence that ends with a punctuation, it returns the first 100 characters
    return clean_text[:100].strip() + "..."

@lru_cache(maxsize=None)
def get_wikidata(idx,title, language):
    #The id of some language are not the same as the one found in the
    #url so I had to map them
    
    language = LANG_MAP.get(language, language)
    #I initialize the wiki url endpoint for the selected languages
    WIKI_URL = f"https://{language}.wikipedia.org/w/api.php"
    Req_session = requests.Session()

    #This query gets everything that is not related to the content of the page
    #It is useful to get information about the views, the age of the page and
    #other metadata
    wiki_metadata = {
        "action": "query",
        "format": "json",
        "prop": "info|revisions|pageviews",
        "rvprop": "timestamp",
        "rvlimit": 1,  #These two lines get the first 
        "rvdir": "newer", #revision so to determine the page age
        "titles": title
    }

    #This query gets the physical content of the pages

    wiki_page_structure = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text|links|images"
    }

    result = {}

    #RESPONSE OF THE FIRST REQUEST
    try:

        response = Req_session.get(WIKI_URL, params=wiki_metadata)
        response.raise_for_status()
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        result["page_length"] = page.get("length")
        revisions = page.get("revisions", [])
        result["creation_date"] = revisions[0]['timestamp'] if revisions else None
        pageviews = page.get("pageviews", {})
        result["num_visits"] = sum([v for v in pageviews.values() if isinstance(v, int)])
    except Exception as e:
        print(f"[ERROR] Metadata request first failed for {title} ({language}): {e}")
        return idx, {}

    try:
        #RESPONSE OF THE SECOND REQUEST
        response = Req_session.get(WIKI_URL, params=wiki_page_structure)
        response.raise_for_status()
        data = response.json().get("parse", {})
        html_text = data.get("text", {}).get("*", "")

        ##extracting the first sentence of the english pages
        #if language == 'en':
        #    result["first_sentence"] = extract_first_sentence(html_text)
        
        #extracting all the other info
        #result["text"] = json.dumps(html_text)
        result["num_words"] = len(re.findall(r'\w+', html_text))
        result["num_images"] = len(data.get("images", []))
        result["links"] = json.dumps([link['*'] for link in data.get("links", []) if not link.get('exists') is False])
        #result["templates"] = json.dumps(data.get("templates", []))
        #result["categories"] = json.dumps(data.get("categories", []))
    except Exception as e:
        print(f"[ERROR] Metadata request second failed for {title} ({language}): {e}")
        return idx, {}
    # See Also section
    #see_also_index = next((s['index'] for s in data.get("sections", []) if 'see also' in s['line'].lower()), None)
    #see_also_links = []
    
    #Number of edits

    total_edits = 0
    cont = None
    while True:
        get_edits = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "revisions",
            "rvlimit": "500",
            "rvprop": "ids",
        }
        if cont:
            get_edits["rvcontinue"] = cont
        try:

            response = Req_session.get(WIKI_URL, params=get_edits)
            response.raise_for_status()
            data = response.json()
            page = next(iter(data["query"]["pages"].values()))
            revisions = page.get("revisions", [])
            total_edits += len(revisions)
            cont = data.get("continue", {}).get("rvcontinue")
        except Exception as e:
            print(f"[ERROR] Metadata request edit failed for {title} ({language}): {e}")
            break
        if not cont:
            break
    result['total_edits'] = total_edits

    #Result is a dictionary that contains the name of the column as key and the respective value as value
    return idx, result

def get_wikipage_metadata(df, max_workers=20):
    #since it was a lot of data I used threads to speed up the execution

    #Initialize the list that contains the result for each row, which can be filled during 
    #the thread computation
    result_list = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #I do a loop throughout all the rows
        for idx, row in df.iterrows():
            title = row['title']
            lang = row['language']
            #I compute the result
            result= executor.submit(get_wikidata, idx, title, lang)
            #I append it in the list
            result_list.append(result)

        for i, result_list in enumerate(tqdm(as_completed(result_list), total=len(result_list), desc="Processing Wikipedia pages")):
            #I print the percentage of completion of the result list
            idx, data = result_list.result()
            for key, value in data.items():
                #I put the value of the key at the specified index
                df.at[idx, key] = value

    return df

def get_nation_language_map():
    #This function does a sparql request to wikidata to get all the languages and their relative countries
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT DISTINCT ?languageCode ?languageLabel ?countryLabel ?countryISO WHERE {
      ?language wdt:P31 wd:Q1288568.
      {
        ?language wdt:P37 ?country.     # official language of
      }
      UNION
      {
        ?language wdt:P495 ?country.    # country of origin
      }
      UNION
      {
        ?language wdt:P17 ?country.     # country
      }
      OPTIONAL { ?language wdt:P218 ?languageCode. }
      OPTIONAL { ?country wdt:P297 ?countryISO. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """)

    #The result is in json format
    sparql.setReturnFormat(JSON)

    #Since the wikidata server could be busy, the request is repeated after a timeout
    num_calls = 5
    for i in range(num_calls):
        try:
            result_query = sparql.query().convert()
            break
        except Exception as e:
            print(f"The call number {i+1}/{num_calls} failed: {e}")
            #I stop for some seconds and then retry the call
            time.sleep(5 * (i+1))  # Exponential backoff
    else:
        raise RuntimeError("SPARQL query failed after multiple retries")
    

    rows = []
    #Extracting the result from the request, which are stored in the result bindings
    #part
    for result in result_query["results"]["bindings"]:
        lang_code = result.get("languageCode", {}).get("value")

        nation_name = result["countryLabel"]["value"]
        
        if lang_code:
            rows.append((lang_code,  nation_name))
    
    #I write the result in a json file

    df_lang_nation = pd.DataFrame(rows, columns=["lang_code", "country"])
    
    #I group by language code to get the list of nations for each language
    df_lang_nation =df_lang_nation.groupby("lang_code")["country"].apply(list).reset_index()
    df_lang_nation.rename(columns={"country": "nations"}, inplace=True)

    # Save as a structured JSON
    df_lang_nation.to_json("utils/map_lang_nation.json", orient="records", lines=True, force_ascii=False)

    print("Saved the language mapping to utils/map_lang_nation.json")

#This function uses the dictionary which contains the nationalities and nations names
#to return the country name given the description
def extract_country(description):
    #putting the description into lowercase
    desc_lower = description.lower()

    #Iterating through the dictionary
    for nationality, country in NATION_MAP.items():
        if nationality in desc_lower or country.lower() in desc_lower:
            return country
    return "Unknown"



if __name__ == '__main__':
    #Open the saved file
    df = pd.read_json(f'utils/query_{FILE_NAME}.json', lines=True)  # use lines=True if your file is line-delimited

    ##getting only english pages
    #english_pages = df[df['language'] == 'en'].copy()
    ##for each item, I get the first english page
    #first_english_pages = english_pages.loc[english_pages.groupby('item')['creation_date'].idxmin()]

    #Adding the column title that is going to be useful for the requests
    df['title'] = df['wikipedia_url'].apply(get_title_from_url)

    if not os.path.exists(f"utils/processed_{FILE_NAME}.json"):
        #Extract the wikipedia metadata for each page only if the file does not exists
        df = get_wikipage_metadata(df, NUM_WORKERS)
        #create the number of links column
        df['num_links'] = df['links'].apply(lambda x: len(json.loads(x)) if pd.notnull(x) else 0)
        print(df.columns)
        #Save the file
        df.to_json(f'utils/processed_{FILE_NAME}.json', orient='records', lines=True)

    #Open the file
    df = pd.read_json(f'utils/processed_{FILE_NAME}.json', lines=True)
    if not os.path.exists(f'utils/{FILE_NAME}_with_avg_cosine.json'):
        #computing cosine similarities
        df_cosine = df[df['language'] == 'en']
        run_cosine_similarity(df_cosine, FILE_NAME)
    
    df_cosine = pd.read_json(f'utils/{FILE_NAME}_with_avg_cosine.json', orient='records', lines=True)

    df_cosine = df_cosine[['item', 'avg_cosine_similarity']]
    print(df_cosine)
    #print(df[['categories']])

    # Convert creation_date to datetime for comparison
    df['creation_date'] = pd.to_datetime(df['creation_date'])
    df = df[df['creation_date'].notnull()]

    #Compute the first aggregation with all the language related wikipedia article according to the rules below

    #Used for computing the number of languages
    df['num_languages'] = 1

    print(df.columns)
    #I want to regroup everything so that it is easier to compute

    aggregation_rules = {
        'num_words': 'mean',
        'num_visits': 'mean',
        'total_edits': 'mean',
        'creation_date': 'min', 
        'num_images': 'mean',
        'num_links': 'mean',
        'page_length': 'mean',
        'num_languages': 'sum', 
    }

    #group by item
    df_group = df.groupby(['item', 'name', 'description', 'type', 'category', 'subcategory']).agg(aggregation_rules).reset_index()
    #Renaming the column so they can be distinguished from the next ones
    df_group = df_group.rename(columns={col: f"{col}_mean" for col in df_group.columns if col not in ['item', 'name', 'description', 'type', 'category', 'subcategory','label']})
    

    #Computing the first language by computing the minimum of the creation date of wikipedia pages
    df['language'] = df['language'].map(LANG_MAP).fillna(df['language'])
    first_langs = df.loc[df.groupby('item')['creation_date'].idxmin(), ['item', 'language']]
    first_langs = first_langs.rename(columns={'language': 'first_language_wiki'})

    # Merge to get the row that matches the first language per item
    df_first_lang_info = df.merge(first_langs, left_on=['item', 'language'], right_on=['item', 'first_language_wiki'], how='inner')

    
    cols_to_keep = ['item', 'first_language_wiki', 'num_words', 'num_links', 'creation_date', 'num_visits', 'total_edits', 'num_images', 'page_length']
    df_first_lang_info = df_first_lang_info[cols_to_keep]


    #Rename the related attributes for the first language with the suffix _first
    df_first_lang_info = df_first_lang_info.rename(columns={col: f"{col}_first" for col in df_first_lang_info.columns if col not in ['item', 'first_language_wiki']})

    print(df_first_lang_info)

    # --- SPARQL only if file doesn't exist ---
    if not os.path.exists("utils/map_lang_nation.json"):
        get_nation_language_map()
    #I load the 
    lang_to_nations = pd.read_json(f'utils/map_lang_nation.json', lines=True)  # use lines=True if your file is line-delimited

    #Merge the dataset about first language with the one that has the 
    df_first_lang_info = df_first_lang_info.merge(lang_to_nations,left_on="first_language_wiki", right_on="lang_code", how="left")

    #merge the dataset about first language and the other about average
    merged_df = df_group.merge(df_first_lang_info, on='item', how='inner')  # or 'left', 'right', 'outer'

    merged_df = merged_df.merge(df_cosine, on='item', how='inner')  # or 'left', 'right', 'outer'
    print(merged_df.columns)

    #Extract country from the description
    merged_df['country_description'] = merged_df['description'].apply(extract_country)

    #Checks if the country in the description is present in one of the country of the first language
    merged_df['country_in_list'] = merged_df.apply( lambda row: row['country_description'] in row['nations'] if isinstance(row['nations'], list) else False, axis=1)

    #print(merged_df)

    merged_df.to_json(f'utils/processed_{FILE_NAME}_2.json', orient='records', lines=True)


    
    
    