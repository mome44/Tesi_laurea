# pip install praw
import praw, json, time

R = praw.Reddit(client_id="V1d1FA2Pc77JBo3YBsQ12g",client_secret="d6jg7gHDIeK8Gw6aBcOAowoEgRlrmw", user_agent="sicilian-corpus/0.1 by mome4401")

SUB = "Sicilianu"
AUTHOR = "totu44"

def posts_by_author_in_sub(sub, author, limit=1000):
    for s in R.subreddit(sub).search(query=f'author:"{author}"', sort="new", time_filter="all", limit=limit):
        if str(s.author).lower() == author.lower():
            yield s

POSTS = posts_by_author_in_sub(SUB, AUTHOR, limit=1000)
data = []

for p in POSTS:
    if len(p.selftext.strip())>3:
        data.append({
            "text": p.selftext.strip()
        })

with open(f"corpus_tesi/siciliano/prosa/reddit_{AUTHOR}_posts.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

