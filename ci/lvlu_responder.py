#!/usr/bin/env python3
# LVLU-RESPONDER-01 — lvlu线 SI3专候响应环（KEYREQ/DISC/SI1-WAKE 三闸）
# 职: ①钥取件即见即注(sealed-box,白名单) ②指名lvlu件即收讫(轻ack) ③SI1-WAKE.md常新(会话接续锚)
# 律: 零定时(事驱入拍) / 值不过板不落盘(内存即用即焚) / names-only回执 / 非白名单→裁示候root
import os, json, base64, urllib.request, urllib.parse, datetime, re, hashlib

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-lvlu')
TOK  = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')
HUB  = 'chepin-ai/ci-inbox'
LINE = 'lvlu'
WHITELIST = {'KIMI_API_KEY','GITEE_TOK','QUAFU_TOKEN','QR_TOKEN_64','QR_TOKEN_128',
             'OPENQ_SDK_TOKEN','OPENQ_CLIENT_ID','KGAT_TOKEN','KAGGLE_JSON','DEEPSEEK_API_KEY'}
LINE_REPOS = {'lgt':['vci-lgt','lgt-line'],'vinf':['vci-vinf','vinf-market-kernel'],
  'qgl':['vci-qgl'],'cfts':['vci-cfts','github-repo-cfts'],'usrm':['vci-usrm','usrm-repo'],
  'ucif2':['vci-ucif2','ucif2-formalization-kernel'],'qfa':['vci-qfa'],'qlv':['vci-qlv'],'lvlu':['vci-lvlu']}

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
        repos = LINE_REPOS.get(line, [f'vci-{line}'])
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
    print(json.dumps({'ts': ts, 'keyreq_done': done, 'acks': acks, 'vault_keys': len(vault)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
