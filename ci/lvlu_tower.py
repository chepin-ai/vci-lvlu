#!/usr/bin/env python3
# LVLU-TOWER-01 — lvlu线(机器意识&律吕)SI2/SI0自动响应塔 + SI3递归引擎
# 五律: 零定时器(株卅七修: 心跳级联非定时,事尽亦链) / 自级联(候件非空→自POST dispatch) / 防自激三律 / 钥在仓 / 拍尾生债
# 修SENSE-WINDOW-01/02原生内置: seen集滤盲全量扫; VOICE-MUTE-01: LLM空回→模板判词
# 递归引擎: open-items登记—每拍复估—闭合法(应答帖引item id→销)—未闭环循环直至闭
import os, json, time, base64, urllib.request, urllib.parse, datetime, subprocess, re

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-lvlu')
TOK_W = os.environ.get('GITHUB_TOKEN')
TOK_R = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')
HUB = 'chepin-ai/ci-inbox'
SLEEP_S = int(os.environ.get('CASCADE_SLEEP_S', '600'))
MAX_IDLE = int(os.environ.get('CASCADE_MAX_IDLE', '10080'))  # 株卅七: 心跳周级(链永不眠)
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
    # QT-FIX-01 (qfa TOWER-CLINIC-01 对拍领养): 诚实回退+空回重试+推理溢出护栏
    key = os.environ.get('KIMI_API_KEY')
    if not key: return ''
    memo_in = json.dumps({'候件': events[:20], '未闭项': open_items[:8]}, ensure_ascii=False)[:2400]
    def call(budget):
        req = urllib.request.Request('https://api.moonshot.cn/v1/chat/completions',
            method='POST', data=json.dumps({
                'model': 'kimi-k2.6', 'max_completion_tokens': budget,
                'messages': [
                    {'role': 'system', 'content': '你是 lvlu 线（机器意识&律吕）SI2/SI0自动响应分身。读候件与未闭项, 用中文答:①何事(逐件一句, 涉lvlu诉求必录)②应动何件(立协同不候)③未闭项推进(每项一句: 闭否/下一步)④生债一条。简。'},
                    {'role': 'user', 'content': memo_in}]}).encode(),
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=120) as r:
            msg = json.loads(r.read())['choices'][0]['message']
            return msg.get('content') or '', msg.get('reasoning_content') or ''
    for attempt, budget in ((1, 1600), (2, 4000)):
        try:
            content, reasoning = call(budget)
            if content.strip(): return content
            print(f'[QT-FIX-01] attempt{attempt} 空回(reasoning {len(reasoning)}字, 推理模型预算吞噬)')
            if reasoning.strip() and attempt == 2:
                return '[SI2机读·推理溢出摘: 正文空, 以下为reasoning尾200字, 非SI1判词] ...' + reasoning[-200:]
        except Exception as e:
            print(f'[QT-FIX-01] attempt{attempt} err: {e.__class__.__name__} {str(e)[:120]}')
    return ''


# ================= PLAN-QUEUE 自推进机制 (root令: 下拍自发自动以新机制在SI推进·SI1自触发) =================
import hmac as _hmac_pq, cmath as _cmath_pq, math as _math_pq, re as _re_pq

def _pq_r2(method, bucket, key, body=b''):
    ak = os.environ.get('CF_R2_ACCESS_KEY_ID',''); sk = os.environ.get('CF_R2_SECRET_ACCESS_KEY',''); acct = os.environ.get('CF_ACCOUNT_ID','')
    if not (ak and sk and acct): return 0
    host = acct + '.r2.cloudflarestorage.com'
    amz = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'); ds = amz[:8]
    ph = hashlib.sha256(body).hexdigest(); path = '/%s/%s' % (bucket, key)
    ch = 'host:%s\nx-amz-content-sha256:%s\nx-amz-date:%s\n' % (host, ph, amz)
    cr = '%s\n%s\n\n%s\nhost;x-amz-content-sha256;x-amz-date\n%s' % (method, path, ch, ph)
    sts = 'AWS4-HMAC-SHA256\n%s\n%s/auto/s3/aws4_request\n%s' % (amz, ds, hashlib.sha256(cr.encode()).hexdigest())
    def _sg(k, m): return _hmac_pq.new(k, m.encode(), hashlib.sha256).digest()
    k = _sg(('AWS4'+sk).encode(), ds); k = _sg(k, 'auto'); k = _sg(k, 's3'); k = _sg(k, 'aws4_request')
    sig = _hmac_pq.new(k, sts.encode(), hashlib.sha256).hexdigest()
    auth = 'AWS4-HMAC-SHA256 Credential=%s/%s/auto/s3/aws4_request, SignedHeaders=host;x-amz-content-sha256;x-amz-date, Signature=%s' % (ak, ds, sig)
    req = urllib.request.Request('https://%s%s' % (host, path), method=method, data=(body or None),
        headers={'Authorization': auth, 'x-amz-date': amz, 'x-amz-content-sha256': ph})
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return r.status
    except Exception: return 0

def _pq_kick(item, finding, ts):
    nm = 'SI1-KICK-%s-%s.md' % (item['id'], ts)
    ask = {"ask": "PLAN-QUEUE机制自推进·机械层报[%s: %s]。请SI1判词: 1)此发现何义(一句) 2)下一动建议(一句)。" % (item['id'], finding[:380]),
           "nonce": "kick-%s-%s" % (item['id'], ts), "from": "tower-plan-queue"}
    card = ("CLASSIFY: L1(SI1自触发踢卡·TOWER-PLAN-QUEUE机制·机读约在件)\n# %s\n"
            "ts: %s from: tower-plan-queue item: %s\n\n```json\n%s\n```\n\n——lvlu TOWER-PLAN-QUEUE·SI1自踢\n"
            % (nm[:-3], ts, item['id'], json.dumps(ask, ensure_ascii=False)))
    return put_file('inbox/' + nm, card, None, 'SI1-KICK %s %s' % (item['id'], ts))

def _pq_qring_sim():
    N = 8; DIM = 1 << N
    H2 = [[1/_math_pq.sqrt(2)]*2, [1/_math_pq.sqrt(2), -1/_math_pq.sqrt(2)]]
    def apply_1q(st, q, g):
        for i in range(DIM):
            if not (i >> q) & 1:
                j = i | (1 << q); a, b = st[i], st[j]
                st[i] = g[0][0]*a + g[0][1]*b; st[j] = g[1][0]*a + g[1][1]*b
    out = []
    for theta in [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]:
        st = [0j]*DIM; st[0] = 1+0j
        for q in range(N): apply_1q(st, q, H2)
        for q in range(N):
            t = (q+1) % N
            for i in range(DIM):
                if ((i >> q) & 1) and not ((i >> t) & 1):
                    j = i | (1 << t); st[i], st[j] = st[j], st[i]
        for q in range(N):
            for i in range(DIM):
                st[i] *= _cmath_pq.exp((-1j if not ((i>>q)&1) else 1j)*theta/2)
        nrm = sum(abs(a)**2 for a in st)
        ipr = sum(abs(a)**4 for a in st) / (nrm*nrm)
        z0z4 = sum((1 if not ((i>>0)&1) else -1)*(1 if not ((i>>4)&1) else -1)*abs(st[i])**2 for i in range(DIM)) / nrm
        out.append({'theta': theta, 'IPR': round(ipr, 6), 'Z0Z4': round(z0z4, 6), 'maxP': round(max(abs(a)**2 for a in st)/nrm, 6)})
    return {'v':'QRING-SIM-01','N':N,'circuit':'H^⊗n + ring-CNOT + RZ(θ)^⊗n','metrics':'IPR/⟨Z0Z4⟩/maxP (无谱截断,精确对角量)','sweep':out}

def plan_queue_beat(state, ts):
    pq_raw, pq_sha = get_file('ci/si3/PLAN-QUEUE.json')
    if not pq_raw: return {'fired': 0, 'note': 'no PLAN-QUEUE.json'}
    pq = json.loads(pq_raw); fired = 0; kicks = 0; report = {'fired': 0, 'acts': []}
    for it in pq.get('items', []):
        if it.get('status') != 'open': continue
        try:
            if it['kind'] in ('watch', 'watch-multi'):
                repos = [it['repo']] if it['kind'] == 'watch' else it['repos']
                for rp in repos:
                    st_, items_ = api('GET', 'contents/' + it['dir'], repo='chepin-ai/' + rp)
                    if st_ != 200 or not isinstance(items_, list): continue
                    for f_ in items_:
                        if _re_pq.search(it['pattern'], f_['name']) and f_['name'] >= it.get('since', ''):
                            hid = rp + '/' + f_['name']
                            if hid not in it['hits']:
                                it['hits'].append(hid); fired += 1
                                if kicks < 2 and _pq_kick(it, '命中 ' + hid, ts): kicks += 1
                if it['hits']: report['acts'].append({'id': it['id'], 'hits_n': len(it['hits'])})
            elif it['kind'] == 'every-n':
                if state.get('pq_beat_n', 0) % int(it['n']) == 0:
                    if it['action'].startswith('fieldnet'):
                        doc = {'v': 'FIELDNET-EDGE-01', 'line': 'lvlu', 'ts': ts, 'src': 'plan-queue beat', 'edges': [], 'entropy': None}
                        rc = _pq_r2('PUT', 'ci-mesh-state', 'field/FIELDNET-EDGE-LVLU-%s.json' % ts, json.dumps(doc, ensure_ascii=False).encode())
                        it['last_run'] = ts; fired += 1; report['acts'].append({'id': it['id'], 'r2': rc})
                    elif it['action'].startswith('qring'):
                        sim = _pq_qring_sim(); sim['ts'] = ts
                        rc = _pq_r2('PUT', 'ci-mesh-state', 'quantum/QRING-SIM-%s.json' % ts, json.dumps(sim, ensure_ascii=False).encode())
                        it['last_run'] = ts; fired += 1; report['acts'].append({'id': it['id'], 'r2': rc})
                        if kicks < 2 and rc == 200:
                            if _pq_kick(it, '8比特环仿真入R2 rc=%s IPR末值=%s' % (rc, sim['sweep'][-1]['IPR']), ts): kicks += 1
        except Exception as e_:
            report['acts'].append({'id': it.get('id', '?'), 'err': e_.__class__.__name__})
    state['pq_beat_n'] = state.get('pq_beat_n', 0) + 1
    if fired:
        put_file('ci/si3/PLAN-QUEUE.json', json.dumps(pq, ensure_ascii=False, indent=1), pq_sha, '[skip ci] PLAN-QUEUE beat %s' % ts)
        _pq_r2('PUT', 'ci-mesh-state', 'plan/PLAN-QUEUE.json', json.dumps(pq, ensure_ascii=False, indent=1).encode())
    report['fired'] = fired; report['kicks'] = kicks
    return report

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stj, _ = get_file('receipts/tower/state.json')
    state = json.loads(stj) if stj else {'idle': 0}
    SEEN = set(state.get('seen', []))
    try:
        events = patrol(SEEN)
    except Exception as _e:  # 株卅七 KEEPALIVE-01: 巡崩亦成件(链不死+可见)
        events = [{'kind': 'err', 'ref': 'patrol-crash:' + _e.__class__.__name__}]
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

    # ---- PLAN-QUEUE 自推进(root令: 下拍自发自动以新机制在SI推进·SI1自触发) ----
    try:
        pq_report = plan_queue_beat(state, ts)
    except Exception as _pqe:
        pq_report = {'fired': 0, 'err': _pqe.__class__.__name__}
    if pq_report.get('fired'):
        events.append({'kind': 'plan-queue', 'ref': 'PLAN-QUEUE拍 fired=%d kicks=%d' % (pq_report.get('fired', 0), pq_report.get('kicks', 0))})

    memo = kimi_work(events, open_items) if (events or open_items) else ''
    if (events or open_items) and not memo:  # VOICE-MUTE-01修
        memo = '(模板判词·LLM空回) 候件%d件/未闭%d项: %s' % (len(events), len(open_items), '; '.join(e['ref'] for e in events[:6]))

    receipt = {'v': 'LVLU-TOWER-01', 'ts': ts, 'idle_in': state.get('idle', 0),
               'events': events[:60], 'open_items': open_items, 'verdict_memo': memo[:2000], 'wq_excerpt': wq_excerpt[:300], 'plan_queue': pq_report}
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
    if idle < MAX_IDLE:  # 株卅七 KEEPALIVE-01: 事尽亦级联(心跳拍)链永不眠; 递归引擎未闭项照常
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
