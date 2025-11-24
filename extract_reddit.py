# pip install praw
import praw, json, time

R = praw.Reddit(client_id="V1d1FA2Pc77JBo3YBsQ12g",
                client_secret="d6jg7gHDIeK8Gw6aBcOAowoEgRlrmw",
                user_agent="sicilian-corpus/0.1 by mome4401")

SUB = "Sicilianu"
AUTHOR = "totu44"

def posts_by_author_in_sub(sub, author, limit=1000):
    # usa l'operatore di ricerca author:"..."
    for s in R.subreddit(sub).search(query=f'author:"{author}"', sort="new", time_filter="all", limit=limit):
        if str(s.author).lower() == author.lower():
            yield s

with open("sicilianu_totu44_posts.json","w",encoding="utf-8") as f:
    for p in posts_by_author_in_sub(SUB, AUTHOR, limit=1000):
        row = {
            "source":"reddit",
            "subreddit": SUB,
            "id": p.id,
            "url": f"https://reddit.com{p.permalink}",
            "created_utc": int(p.created_utc),
            "author": str(p.author),
            "title": p.title or "",
            "selftext": p.selftext or ""
        }
        f.write(json.dumps(row, ensure_ascii=False)+"\n")
        time.sleep(0.5)  # gentile coi rate limit
