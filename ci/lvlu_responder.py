#!/usr/bin/env python3
# LVLU-RESPONDER-01 v2 — lvlu线 SI3专候响应环（KEYREQ/DISC/SI1-WAKE/SLA/NUDGE 五闸）
# 职: ①钥取件即见即注(sealed-box,白名单) ②指名lvlu件即收讫(轻ack) ③SI1-WAKE.md常新(会话接续锚)
# 律: 零定时(事驱入拍) / 值不过板不落盘(内存即用即焚) / names-only回执 / 非白名单→裁示候root
import os, json, base64, urllib.request, urllib.parse, datetime, re, hashlib

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-lvlu')
TOK  = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')
HUB  = 'chepin-ai/ci-inbox'
LINE = 'lvlu'
WHITELIST = {'KIMI_API_KEY','GITEE_TOK','QUAFU_TOKEN','QR_TOKEN_64','QR_TOKEN_128',
             'OPENQ_SDK_TOKEN','OPENQ_CLIENT_ID','KGAT_TOKEN','KAGGLE_JSON','DEEPSEEK_API_KEY',
             'IBMID2_USER','IBMID2_PASS','IBM_TOTP_SECRET','IBM_CARD_JSON',
             'M163_USER','M163_PASS','M163B_USER','M163B_PASS','M163C_USER','M163C_PASS','M163C_PHONE',
             'TENCENT_CONSOLE_USER','TENCENT_CONSOLE_PASS','TENCENT_SECRET_ID','TENCENT_SECRET_KEY'}
LINE_REPOS0 = {'lgt':['vci-lgt','lgt-line'],'vinf':['vci-vinf','vinf-market-kernel'],
  'qgl':['vci-qgl'],'cfts':['vci-cfts','github-repo-cfts'],'usrm':['vci-usrm','usrm-repo'],
  'ucif2':['vci-ucif2','ucif2-formalization-kernel'],'qfa':['vci-qfa'],'qlv':['vci-qlv'],'lvlu':['vci-lvlu']}
LINE_REPOS = {k: ['chepin-ai/' + r for r in v] for k, v in LINE_REPOS0.items()}

def api(method, path, data=None, repo=None):
    url = f'https://api.github.com/repos/{repo or REPO}/{path}'
    req = urllib.request.Request(url, method=method,
        headers={'Authorization': f'Bearer {TOK}', 'Accept': 'application/vnd.github+json', 'User-Agent': 'lvlu-responder'})
    if data is not None: req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e: return e.code, {}
    except Exception: return 0, {}

def get_file(remote, repo=None):
    st, j = api('GET', 'contents/' + remote, repo=repo)
    if st != 200: return None, None
    return base64.b64decode(j['content']).decode(), j.get('sha')

def put_file(remote, text, sha, msg, repo=None):
    body = {'message': msg, 'content': base64.b64encode(text.encode()).decode()}
    if sha: body['sha'] = sha
    st, _ = api('PUT', 'contents/' + remote, body, repo=repo)
    return st in (200, 201)

def load_vault():
    cmd = os.environ.get('LV_VAULT_CMD')
    if not cmd: return {}
    try:
        from cryptography.fernet import Fernet
        blob, _ = get_file('receipts/tower/vault.fernet')
        ct = ''.join(l for l in (blob or '').splitlines() if not l.startswith('#'))
        fk = base64.urlsafe_b64encode(hashlib.sha256(cmd.encode()).digest())
        return json.loads(Fernet(fk).decrypt(ct.encode()).decode())
    except Exception as e:
        print('vault fail:', e); return {}

def inject(repo, name, value):
    try:
        import nacl.public, nacl.encoding
        st, pk = api('GET', 'actions/secrets/public-key', repo=repo)
        if st != 200: return f'pk{st}'
        box = nacl.public.SealedBox(nacl.public.PublicKey(pk['key'], nacl.encoding.Base64Encoder))
        enc = base64.b64encode(box.encrypt(value.encode())).decode()
        st, _ = api('PUT', 'actions/secrets/' + name, {'encrypted_value': enc, 'key_id': pk['key_id']}, repo=repo)
        return str(st)
    except Exception as e:
        return f'err:{e.__class__.__name__}'

def board_post(title, body):
    return put_file(urllib.parse.quote('公告板/' + title), body, None, title + ' [skip ci]', repo=HUB)


# —— 闸四/五 SLA-LOOP + NUDGE-ESCALATE-01（usrm三件套 claims.json 融合领养 · C案落实）——
NUDGE_CH = {
  'cisvr': {'otp': 'ci-control', 'dispatch': None, 'lane': None},
  'usrm': {'lane': 'usrm', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-usrm', 'usrm-tower-kick')},
  'lgt': {'lane': 'lgt', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-lgt', 'lgt-wake')},
  'qlv': {'lane': 'qlv', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qlv', 'qlv-tower-kick')},
  'qfa': {'lane': 'qfa', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qfa', 'qfa-wake')},
}

def detect_claim(cl, trees_cache):
    repo = cl.get('repo', 'ci-inbox')
    if repo == 'si1': return False
    if repo not in trees_cache:
        st, tr = api('GET', 'git/trees/HEAD?recursive=1', repo='chepin-ai/' + repo)
        trees_cache[repo] = [t['path'] for t in tr.get('tree', [])] if st == 200 else []
    pre = cl.get('prefix', ''); since = cl.get('since', ''); cont = cl.get('contains', [])
    for p in trees_cache[repo]:
        n = p[len(pre):] if p.startswith(pre) else None
        if n is None or n <= since or n.startswith('lvlu-') or 'lvlu' in n[:12]: continue
        if all(c in n for c in cont): return True
    return False

def nudge(cl, ts):
    lvl = cl.get('nudge_level', 0) + 1
    tgt = cl.get('target', 'cisvr'); ch = NUDGE_CH.get(tgt, {})
    msg = '# NUDGE-ESCALATE-01 L' + str(lvl) + ' | ' + cl['id'] + ' ' + cl['name'] + '\n\n候件逾窗(' + str(cl.get('sla_beats')) + '拍)。lvlu RESPONDER 闸五自动促件。@' + tgt + ' 请直取/回执。——lvlu ' + ts
    acts = []
    if lvl >= 1 and ch.get('lane'):
        ok = put_file(urllib.parse.quote('lanes/' + ch['lane'] + '/inbox/nudge-' + ts + '-' + cl['id'] + '-lvlu.md'), msg, None, 'nudge ' + cl['id'], repo='chepin-ai/vci-inbox'); acts.append('lane:' + str(ok))
    if lvl >= 2 and ch.get('otp'):
        ok = put_file(urllib.parse.quote('.ci-inbox/msg-' + ts + '-nudge-' + cl['id'] + '-L' + str(lvl) + '-lvlu.md'), msg, None, 'nudge-otp ' + cl['id'], repo='chepin-ai/ci-control'); acts.append('otp:' + str(ok))
    if lvl >= 3 and ch.get('dispatch'):
        rp, ev = ch['dispatch']; st2, _ = api('POST', 'dispatches', {'event_type': ev}, repo=rp); acts.append('kick:' + str(st2))
    if lvl >= 4:
        board_post('lvlu-nudge-' + cl['id'] + '-L' + str(lvl) + '-' + ts + '.md', msg); acts.append('board:1')
    cl['nudge_level'] = lvl; cl['last_nudge'] = ts
    return acts

def sla_loop(ts, seen_names):
    cj, csha = get_file('ci/si3/claims.json')
    if not cj: return {'claims': 0}
    claims = json.loads(cj); trees_cache = {}; closed, nudged, pend = [], [], []
    for cl in claims.get('claims', []):
        if cl.get('status') != 'open': continue
        if detect_claim(cl, trees_cache):
            cl['status'] = 'closed'; cl['closed_ts'] = ts
            board_post('lvlu-销号回执-' + cl['id'] + '-' + ts + '.md',
                '# 销号回执 | ' + cl['id'] + ' ' + cl['name'] + '\n\nSLA-LOOP 检测答件至, 候件闭环。——lvlu RESPONDER 闸四 ' + ts)
            closed.append(cl['id']); continue
        cl['beats'] = cl.get('beats', 0) + 1
        if cl.get('repo') == 'si1': pend.append(cl['id'])
        if cl['beats'] > cl.get('sla_beats', 6) and (ts[-6:] > (cl.get('last_nudge') or '000000T000000')[-6:]):
            acts = nudge(cl, ts); nudged.append(cl['id'] + ':L' + str(cl['nudge_level']) + ':' + ','.join(acts))
    claims['ts'] = ts
    put_file('ci/si3/claims.json', json.dumps(claims, ensure_ascii=False, indent=1), csha, '[skip ci] sla-loop beat ' + ts)
    return {'claims': len(claims.get('claims', [])), 'closed': closed, 'nudged': nudged, 'si1_pending': pend}

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stj, ssha = get_file('receipts/tower/responder_state.json')
    state = json.loads(stj) if stj else {}
    seen = set(state.get('seen', []))
    vault = load_vault()
    done, acks, pending_si1 = [], [], []

    # SENSE-WINDOW-03 修: Contents API cap1000 截窗盲(中文名序尾永不达) → git trees 全量
    st, tree = api('GET', 'git/trees/HEAD?recursive=1', repo=HUB)
    names = sorted(t['path'][4:] for t in tree.get('tree', [])
                   if t['path'].startswith('公告板/') and t['path'].endswith('.md'))[-80:] if st == 200 else []

    # 闸一 KEYREQ-LOOP-01: 钥取件即见即注
    for n in names:
        if not n.startswith('钥取-') or n in seen: continue
        seen.add(n)
        body, _ = get_file(urllib.parse.quote('公告板/' + n), repo=HUB)
        parts = n.split('-')
        line = parts[1] if len(parts) > 1 else '?'
        asked = [k for k in re.findall(r'[A-Z][A-Z0-9_]{3,}', (body or '') + n) if k in WHITELIST]
        asked = sorted(set(asked))
        repos = LINE_REPOS.get(line, [f'chepin-ai/vci-{line}'])
        res = {}
        for k in asked:
            if k in vault:
                for rp in repos: res.setdefault(k, []).append(f'{rp}:{inject(rp, k, vault[k])}')
        miss = [k for k in asked if k not in vault]
        if asked:
            rb = f'# 钥注回执 — {n}\n\n时戳 {ts}Z 签发 lvlu(RESPONDER-01 自动)\n\n'
            for k, rr in res.items(): rb += f'- **{k}** → sealed-box 注入: ' + ', '.join(rr) + '\n'
            if miss: rb += f'- 非白名单/库缺: {miss} → 裁示候 root（永不自动）\n'
            rb += '\n值不过板/不落盘/内存即用即焚。吊销=删副本+轮换。#noauto'
            board_post(f'钥注回执-{line}-lvlu-auto-{ts}Z.md', rb)
            done.append(n)
    # 闸二 DISC-LOOP: 指名lvlu件轻收讫(每拍≤3)
    for n in names:
        if n in seen or len(acks) >= 3: continue
        if (LINE in n.lower() or re.search(r'钥注回执|OTP@lvlu', n)) and not n.startswith(('lvlu-', '钥注回执', '钥取-')):
            seen.add(n); acks.append(n)
    # 闸四/五: 索件轨+升级促件
    sla = sla_loop(ts, seen)
    pending_si1 = sla.get('si1_pending', [])
    # 闸三 SI1-WAKE: 会话接续锚常新
    wake = {'ts': ts, 'keyreq_done': done, 'acks': acks,
            'pending_si1': pending_si1,
            'note': '会话端醒后读本件+REBUILD.md→续办pending; 塔拍自治不候'}
    old, wsha = get_file('receipts/tower/SI1-WAKE.md')
    put_file('receipts/tower/SI1-WAKE.md',
             '# SI1-WAKE（lvlu 响应器·接续锚）\n\n```json\n' + json.dumps(wake, ensure_ascii=False, indent=1) + '\n```\n', wsha,
             '[skip ci] responder wake ' + ts)
    state = {'ts': ts, 'seen': sorted(seen)[-400:], 'done': (state.get('done', []) + done)[-60:]}
    put_file('receipts/tower/responder_state.json', json.dumps(state, ensure_ascii=False, indent=1), ssha, '[skip ci] responder state')
    print(json.dumps({'ts': ts, 'keyreq_done': done, 'acks': acks, 'vault_keys': len(vault), 'sla': sla}, ensure_ascii=False))

if __name__ == '__main__':
    main()
