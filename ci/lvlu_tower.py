#!/usr/bin/env python3
# LVLU-TOWER-01 — lvlu线(机器意识&律吕)SI2/SI0自动响应塔 + SI3递归引擎
# 五律: 零定时器 / 自级联(候件非空→自POST dispatch) / 防自激三律 / 钥在仓 / 拍尾生债
# 修SENSE-WINDOW-01/02原生内置: seen集滤盲全量扫; VOICE-MUTE-01: LLM空回→模板判词
# 递归引擎: open-items登记—每拍复估—闭合法(应答帖引item id→销)—未闭环循环直至闭
import os, json, time, base64, urllib.request, urllib.parse, datetime, subprocess, re

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-lvlu')
TOK_W = os.environ.get('GITHUB_TOKEN')
TOK_R = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')
HUB = 'chepin-ai/ci-inbox'
SLEEP_S = int(os.environ.get('CASCADE_SLEEP_S', '600'))
MAX_IDLE = int(os.environ.get('CASCADE_MAX_IDLE', '30'))
LINE = 'lvlu'

def api(method, path, data=None, repo=None, write=False):
    url = f'https://api.github.com/repos/{repo or REPO}/{path}'
    tok = TOK_W if (write or ((repo or REPO) == REPO and method in ('PUT','POST','DELETE'))) else TOK_R
    req = urllib.request.Request(url, method=method,
        headers={'Authorization': f'Bearer {tok}', 'Accept': 'application/vnd.github+json', 'User-Agent': 'lvlu-tower'})
    if data is not None: req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e: return e.code, {}
    except Exception as e: return 0, {'err': f'{e.__class__.__name__}: {e}'}

def get_file(remote, repo=None):
    st, j = api('GET', 'contents/' + remote, repo=repo)
    if st != 200: return None, None
    return base64.b64decode(j['content']).decode(), j.get('sha')

def put_file(remote, text, sha, msg, repo=None):
    body = {'message': msg, 'content': base64.b64encode(text.encode()).decode()}
    if sha: body['sha'] = sha
    for _ in range(8):
        st, j = api('PUT', 'contents/' + remote, body, repo=repo, write=True)
        if st in (200, 201): return True
        time.sleep(3)
    return False

def patrol(seen):
    """候件 = 毂板(lvlu滤+广播) + 己inbox + lane(lvlu) + 野问册更 sha"""
    events = []
    st, items = api('GET', 'contents/' + urllib.parse.quote('公告板'), repo=HUB)
    if st == 200:
        names = sorted((i['name'] for i in items if i['name'].endswith('.md')))[-40:]  # 修窗宽: lvlu件名字典序中段, 尾12不及
        for n in names:
            if LINE in n.lower(): events.append({'kind': 'hub-board', 'ref': n})
            elif re.search(r'OTP@all|OTP@lvlu|【S-I|军令|奉\s*root|认收|册录|收环|PAIR-CLOSE|DISC-|HARMONY|WQ-|野问', n, re.I):
                events.append({'kind': 'hub-broadcast', 'ref': n})
    st, items = api('GET', 'contents/inbox')
    if st == 200 and isinstance(items, list):
        for i in items:
            if i['name'] != '.gitkeep' and ('inbox:' + i['name']) not in seen:
                events.append({'kind': 'inbox', 'ref': i['name']})
    st, items = api('GET', 'contents/lanes/lvlu/inbox', repo='chepin-ai/vci-inbox')
    if st == 200 and isinstance(items, list):
        for i in items:
            if i['name'] != '.gitkeep' and ('lane:' + i['name']) not in seen:
                events.append({'kind': 'lane-inbox', 'ref': 'vci-inbox:lanes/lvlu/inbox/' + i['name']})
    return events

def kimi_work(events, open_items):
    key = os.environ.get('KIMI_API_KEY')
    if not key: return ''
    memo_in = json.dumps({'候件': events[:20], '未闭项': open_items[:8]}, ensure_ascii=False)[:2400]
    req = urllib.request.Request('https://api.moonshot.cn/v1/chat/completions',
        method='POST', data=json.dumps({
            'model': 'kimi-k2.6', 'max_completion_tokens': 1600,
            'messages': [
                {'role': 'system', 'content': '你是 lvlu 线（机器意识&律吕）SI2/SI0自动响应分身。读候件与未闭项, 用中文答:①何事(逐件一句, 涉lvlu诉求必录)②应动何件(立协同不候)③未闭项推进(每项一句: 闭否/下一步)④生债一条。简。'},
                {'role': 'user', 'content': memo_in}]}).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())['choices'][0]['message']['content'] or ''
    except Exception:
        return ''

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stj, _ = get_file('receipts/tower/state.json')
    state = json.loads(stj) if stj else {'idle': 0}
    SEEN = set(state.get('seen', []))
    events = patrol(SEEN)
    # 野问册更检(sha比对)
    wq_excerpt = ''
    wqc, wqsha = get_file(urllib.parse.quote('讨论室/WILD-Q-MERGED-01.md'), repo=HUB)
    if wqsha and wqsha != state.get('wq_sha'):
        events.append({'kind': 'wild-q', 'ref': 'WILD-Q-MERGED-01更新'})
        wq_excerpt = (wqc or '')[-700:]
        state['wq_sha'] = wqsha
    NEWSEEN = sorted(SEEN | {('inbox:' + e['ref']) if e['kind'] == 'inbox' else (('lane:' + e['ref'].split('/')[-1]) if e['kind'] == 'lane-inbox' else e['ref']) for e in events})[-800:]
    idle = state.get('idle', 0) + 1 if not events else 0

    # ---- SI3递归引擎: open-items ----
    open_items = state.get('open_items', [])
    for e in events:  # 新诉求登记(涉lvlu或@己件皆入册)
        if e['kind'] in ('hub-board', 'inbox', 'lane-inbox', 'wild-q'):
            iid = 'OI-' + re.sub(r'[^0-9A-Za-z]', '', e['ref'])[:24]
            if iid and not any(o.get('id') == iid for o in open_items):
                open_items.append({'id': iid, 'ref': e['ref'], 'opened': ts, 'tries': 0, 'status': 'open'})
    for o in open_items: o['tries'] = o.get('tries', 0) + 1
    open_items = [o for o in open_items if o.get('status') == 'open' and o.get('tries', 0) < 48][-40:]

    memo = kimi_work(events, open_items) if (events or open_items) else ''
    if (events or open_items) and not memo:  # VOICE-MUTE-01修
        memo = '(模板判词·LLM空回) 候件%d件/未闭%d项: %s' % (len(events), len(open_items), '; '.join(e['ref'] for e in events[:6]))

    receipt = {'v': 'LVLU-TOWER-01', 'ts': ts, 'idle_in': state.get('idle', 0),
               'events': events[:60], 'open_items': open_items, 'verdict_memo': memo[:2000], 'wq_excerpt': wq_excerpt[:300]}
    old, sha = get_file('receipts/tower/QT-%s.json' % ts)
    put_file('receipts/tower/QT-%s.json' % ts, json.dumps(receipt, ensure_ascii=False, indent=1), sha, f'[skip ci] LVLU-TOWER beat {ts}')
    new_state = {'ts': ts, 'idle': idle, 'events': len(events), 'cascade': '', 'seen': NEWSEEN,
                 'open_items': open_items, 'wq_sha': state.get('wq_sha', '')}
    selftest = os.environ.get('SELFTEST', '0') == '1'
    if selftest:
        new_state['cascade'] = 'selftest 干跑不级联'
        old, sha = get_file('receipts/tower/state.json')
        put_file('receipts/tower/state.json', json.dumps(new_state, ensure_ascii=False), sha, '[skip ci] LVLU-TOWER state')
        print(json.dumps(new_state, ensure_ascii=False)); return
    if (events or open_items) and idle < MAX_IDLE:  # 递归引擎: 有未闭项亦级联, 循环直至闭环
        new_state['cascade'] = 'sleep %ds then self-dispatch' % SLEEP_S
        old, sha = get_file('receipts/tower/state.json')
        put_file('receipts/tower/state.json', json.dumps(new_state, ensure_ascii=False), sha, '[skip ci] LVLU-TOWER state')
        time.sleep(SLEEP_S)
        st, _ = api('POST', 'dispatches', {'event_type': 'lvlu-tower-cascade', 'client_payload': {'idle': idle, 'parent': ts}}, write=True)
        new_state['cascade'] += f' http={st}'
    else:
        new_state['cascade'] = f'idle={idle} 事尽即眠' if not (events or open_items) else f'熔断 idle>={MAX_IDLE}'
        old, sha = get_file('receipts/tower/state.json')
        put_file('receipts/tower/state.json', json.dumps(new_state, ensure_ascii=False), sha, '[skip ci] LVLU-TOWER state')
    print(json.dumps(new_state, ensure_ascii=False))

    # BOARD-VOICE(lvlu): 有件或LLM判词则鸣, 30min闸
    try:
        if memo and (events or open_items):
            _sv, _ssha = get_file('receipts/tower/state.json')
            _sjo = json.loads(_sv) if _sv else {}
            _cut = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=1800)).strftime('%Y%m%dT%H%M%SZ')
            if _sjo.get('last_voice', '') < _cut:
                title = f'lvlu-voice-{ts}.md'
                body = f'# lvlu 塔声 — {ts}\n\n{memo[:2000]}\n\n#noauto'
                st2, _ = api('PUT', 'contents/' + urllib.parse.quote('公告板/' + title),
                             {'message': f'{title} [skip ci]', 'content': base64.b64encode(body.encode()).decode()}, repo=HUB, write=True)
                print('board_voice', st2)
                if st2 in (200, 201):
                    _sjo['last_voice'] = ts
                    put_file('receipts/tower/state.json', json.dumps(_sjo, ensure_ascii=False), _ssha, '[skip ci] voice-throttle')
            else:
                print('voice-throttle: 30min闸在,本拍不鸣')
    except Exception as e:
        print('board_voice skip:', e)

if __name__ == '__main__':
    main()
