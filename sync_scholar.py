"""Refresh the complete Scholar list; keep the previous file on any failure.

Set SERPAPI_API_KEY in the environment. Credentials never enter the website.
API documentation: https://serpapi.com/google-scholar-author-api
"""
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

AUTHOR_ID = 'W9brBMQAAAAJ'
DESTINATION = Path(__file__).parent / 'dist' / 'publications.json'


def collect(fetch):
    articles = []
    seen = set()
    start = 0
    for _ in range(30):
        data = fetch(start)
        if data.get('error'):
            raise RuntimeError('Scholar provider returned an error; previous data preserved.')
        if start == 0:
            name = data.get('author', {}).get('name', '')
            if 'asghar' not in name.lower():
                raise RuntimeError('Unexpected Scholar author; previous data preserved.')
        batch = data.get('articles')
        if not isinstance(batch, list) or not batch:
            raise RuntimeError('Missing Scholar articles; previous data preserved.')
        for item in batch:
            identity = item.get('citation_id') or item.get('link') or item.get('title')
            if not identity or identity in seen:
                raise RuntimeError('Repeated or invalid Scholar page; previous data preserved.')
            seen.add(identity)
            if not item.get('title'):
                raise RuntimeError('Missing publication title; previous data preserved.')
            total = item.get('cited_by', {}).get('value')
            articles.append({
                'title': item['title'], 'authors': item.get('authors', ''),
                'publication': item.get('publication', ''), 'year': str(item.get('year', '')),
                'link': item.get('link', f'https://scholar.google.com/citations?user={AUTHOR_ID}'),
                'citations': total,
            })
        pagination = data.get('serpapi_pagination', {})
        if not pagination.get('next'):
            return articles
        next_query = urllib.parse.parse_qs(urllib.parse.urlparse(pagination['next']).query)
        next_start = next_query.get('start', next_query.get('cstart', [str(start + len(batch))]))[0]
        new_start = int(next_start)
        if new_start <= start:
            raise RuntimeError('Invalid pagination; previous data preserved.')
        start = new_start
    raise RuntimeError('Pagination limit reached; previous data preserved.')


def main():
    key = os.environ.get('SERPAPI_API_KEY')
    if not key:
        print('Set SERPAPI_API_KEY to enable Scholar updates. Existing publications unchanged.', file=sys.stderr)
        return 2

    def fetch(start):
        params = {'engine': 'google_scholar_author', 'author_id': AUTHOR_ID,
                  'hl': 'en', 'num': 100, 'start': start, 'api_key': key}
        request = urllib.request.Request('https://serpapi.com/search.json?' + urllib.parse.urlencode(params))
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)

    try:
        articles = collect(fetch)
        previous = json.loads(DESTINATION.read_text(encoding='utf-8'))
        if previous.get('mode') == 'scholar' and len(articles) < len(previous['articles']) * .8:
            raise RuntimeError('Unexpected large reduction in publications; review before replacing.')
        result = {'source': 'Google Scholar', 'mode': 'scholar',
                  'updated': datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
                  'author_id': AUTHOR_ID, 'articles': articles}
        temporary = DESTINATION.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(DESTINATION)
        print(f'Updated {len(articles)} publications from Google Scholar.')
        return 0
    except Exception:
        # urllib errors may contain the authenticated URL: never print them.
        print('Scholar refresh failed. Previous publications preserved; check provider/account and retry.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
