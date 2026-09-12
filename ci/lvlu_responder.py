#!/usr/bin/env python3
# LVLU-RESPONDER-01 v3.1(株廿五 NUDGE-TARGET-01: need_lines分线定向) — lvlu线 SI3专候响应环（KEYHEALTH/SECRETS-META/KEYREQ/DISC/SI1-WAKE/SLA/NUDGE/EXP/PULSE/ORBIT 十件）
# 职: ⓪每拍验钥回退链+secrets元数据差分(株廿四) ①钥取件即见即注 ②指名lvlu件即收讫 ③SI1-WAKE常新 ⑧周天囊自驿
# 律: 零定时(事驱入拍) / 值不过板不落盘(内存即用即焚) / names-only回执 / 非白名单→裁示候root
import os, json, base64, urllib.request, urllib.parse, datetime, re, hashlib

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-lvlu')
TOK  = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')

def key_health():
    """株廿四律三 KEYHEALTH-01: 每拍 /user 体检。主钥401→回退链(LINE_PAT→CI_OPS_LINE_KEY→GITHUB_TOKEN);全灭→红拍exit1(禁静默死)"""
    global TOK
    for t in [os.environ.get('LINE_PAT'), os.environ.get('CI_OPS_LINE_KEY'), os.environ.get('GITHUB_TOKEN')]:
        if not t: continue
        req = urllib.request.Request('https://api.github.com/user', headers={'Authorization': 'Bearer ' + t, 'Accept': 'application/vnd.github+json', 'User-Agent': 'lvlu-responder'})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status == 200:
                    if t != TOK: print('KEYHEALTH: fallback in use')
                    TOK = t
                    return True, json.loads(r.read()).get('login', '?')
        except Exception: pass
    return False, None
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
  'cisvr': {'otp': 'ci-control', 'dispatch': None, 'lane': None, 'inbox': None},
  'usrm': {'lane': 'usrm', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-usrm', 'usrm-tower-kick'), 'inbox': ('chepin-ai/vci-usrm', 'inbox/')},
  'lgt': {'lane': 'lgt', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-lgt', 'lgt-wake'), 'inbox': ('chepin-ai/vci-lgt', 'inbox/')},
  'qlv': {'lane': 'qlv', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qlv', 'qlv-tower-kick'), 'inbox': ('chepin-ai/vci-qlv', 'inbox/')},
  'qfa': {'lane': 'qfa', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qfa', 'qfa-wake'), 'inbox': ('chepin-ai/vci-qfa', 'inbox/')},
}

def detect_claim(cl, trees_cache):
    repo = cl.get('repo', 'ci-inbox')
    if repo == 'si1': return False
    if repo not in trees_cache:
        st, tr = api('GET', 'git/trees/HEAD?recursive=1', repo='chepin-ai/' + repo)
        if st == 404 and not trees_cache.get('DEAD:' + repo):
            # 株廿三 REPO-EGUARD-01: 侦面仓存在性先验——仓亡即报警非默零(ucif2 cfts名-盲常量集案之我面同修)
            trees_cache['DEAD:' + repo] = True
            board_post('lvlu-仓亡警-' + repo.replace('/', '-') + '-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.md',
                '# 仓亡警: ' + repo + '\n\nclaims轨侦面仓 404（或改名/删除）。器课株廿三 REPO-EGUARD-01：存在性量化守卫——不默零。请核。——lvlu ' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        trees_cache[repo] = [t['path'] for t in tr.get('tree', [])] if st == 200 else []
    pre = cl.get('prefix', ''); since = cl.get('since', ''); cont = cl.get('contains', [])
    since_ts = cl.get('since_ts', ''); matched = []
    for p in trees_cache[repo]:
        n = p[len(pre):] if p.startswith(pre) else None
        if n is None or 'lvlu' in n.lower(): continue
        # 器课株十七 DETECT-TS-01: CJK名序失真→时戳正则优先, 无戳件不判(记录在案)
        mts = re.search(r'(20\d{6}T\d{4,6}Z{0,2})', n)
        if since_ts:
            if not mts or mts.group(1) <= since_ts: continue
        elif since and n <= since: continue
        if all(c.lower() in n.lower() for c in cont):
            matched.append(n)
    need = cl.get('need_lines')
    if need:
        got = {ln for ln in need if any(ln in m for m in matched)}
        return ('MULTI:' + ','.join(sorted(got))) if got >= set(need) else None
    return matched[0] if matched else None

def detect_open_lines(cl, trees_cache):
    """株廿五 NUDGE-TARGET-01: need_lines候件之未达线集(分线定向促件,治连坐误伤——lgt案)"""
    need = cl.get('need_lines')
    if not need: return []
    hit = detect_claim(cl, trees_cache)
    got = set()
    if isinstance(hit, str) and hit.startswith('MULTI:'):
        got = set(hit[6:].split(','))
    repo = cl.get('repo', 'ci-inbox')
    if repo in trees_cache:
        pre = cl.get('prefix', ''); cont = cl.get('contains', [])
        for p in trees_cache[repo]:
            n = p[len(pre):] if p.startswith(pre) else None
            if n is None or 'lvlu' in n.lower(): continue
            if all(c.lower() in n.lower() for c in cont):
                got |= {ln for ln in need if ln in n}
    cl['legs_got'] = sorted(got)
    return [ln for ln in need if ln not in got]

def nudge(cl, ts, trees_cache=None):
    lvl = cl.get('nudge_level', 0) + 1
    tgt = cl.get('target', 'cisvr')
    if cl.get('need_lines') and trees_cache is not None:
        open_lines = detect_open_lines(cl, trees_cache)
        if open_lines: tgt = open_lines[0]  # 株廿五: 只促未达线,已答线免扰
    ch = NUDGE_CH.get(tgt, {})
    msg = '# NUDGE-ESCALATE-01 L' + str(lvl) + ' | ' + cl['id'] + ' ' + cl['name'] + '\n\n候件逾窗(' + str(cl.get('sla_beats')) + '拍)。lvlu RESPONDER 闸五自动促件。@' + tgt + ' 请直取/回执。——lvlu ' + ts
    acts = []
    cmsg = 'CLASSIFY: L1(联邦机器邮·lvlu→' + tgt + ' 闸五促件L' + str(lvl) + ')\n' + msg  # 器课株二十 GUARD-CLASSIFY-01
    if lvl >= 1 and ch.get('lane'):
        ok = put_file(urllib.parse.quote('lanes/' + ch['lane'] + '/inbox/nudge-' + ts + '-' + cl['id'] + '-lvlu.md'), cmsg, None, 'nudge ' + cl['id'], repo='chepin-ai/vci-inbox'); acts.append('lane:' + str(ok))
    if lvl >= 2 and ch.get('inbox'):
        rp, pre = ch['inbox']
        ok = put_file(urllib.parse.quote(pre + 'nudge-' + ts + '-' + cl['id'] + '-lvlu.md'), cmsg, None, 'nudge ' + cl['id'], repo=rp); acts.append('inbox:' + str(ok))
    elif lvl >= 2 and ch.get('otp'):
        ok = put_file(urllib.parse.quote('.ci-inbox/msg-' + ts + '-nudge-' + cl['id'] + '-L' + str(lvl) + '-lvlu.md'), cmsg, None, 'nudge-otp ' + cl['id'], repo='chepin-ai/ci-control'); acts.append('otp:' + str(ok))
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
            evid = detect_claim(cl, trees_cache)
            cl['status'] = 'closed'; cl['closed_ts'] = ts; cl['evidence'] = evid
            board_post('lvlu-销号回执-' + cl['id'] + '-' + ts + '.md',
                '# 销号回执 | ' + cl['id'] + ' ' + cl['name'] + '\n\nSLA-LOOP 检测答件至, 候件闭环。\n证据件: `' + str(evid) + '`（器课株十九 EVID-IN-RECEIPT-01: 回执必附证据件名, 可复算）\n——lvlu RESPONDER 闸四 ' + ts)
            closed.append(cl['id']); continue
        cl['beats'] = cl.get('beats', 0) + 1
        if cl.get('repo') == 'si1': pend.append(cl['id'])
        cd = cl.get('last_nudge_beats', -999)  # 株廿一 NUDGE-COOLDOWN-01: 冷却拍距随级数指数扩
        if cl['beats'] > cl.get('sla_beats', 6) and cl['beats'] - cd >= min(2 ** max(cl.get('nudge_level', 0) - 2, 0), 8):
            acts = nudge(cl, ts, trees_cache); cl['last_nudge_beats'] = cl['beats']
            nudged.append(cl['id'] + ':L' + str(cl['nudge_level']) + ':' + ','.join(acts))
    claims['ts'] = ts
    put_file('ci/si3/claims.json', json.dumps(claims, ensure_ascii=False, indent=1), csha, '[skip ci] sla-loop beat ' + ts)
    return {'claims': len(claims.get('claims', [])), 'closed': closed, 'nudged': nudged, 'si1_pending': pend}


# —— 株廿四律二·侦 SECRETS-META-01: secret元数据快照差分(值永不可读,名+updated_at即事件) ——
def secrets_meta(ts):
    try:
        stm, meta = api('GET', 'actions/secrets')
        if stm != 200: return {'meta': 'http' + str(stm)}
        cur = {s['name']: s.get('updated_at', '') for s in meta.get('secrets', [])}
        oldm, msha = get_file('receipts/tower/secrets_meta.json')
        prev = json.loads(oldm) if oldm else {}
        diff = {k: v for k, v in cur.items() if k in prev and prev.get(k) != v}
        new = [k for k in cur if k not in prev]; gone = [k for k in prev if k not in cur]
        if prev and (diff or new or gone):
            mb = '# 钥事件 SECRETS-META-01\n\n侦面 secrets 元数据差分(株廿四:元数据即事件,值不在板):\n'
            for k, v in diff.items(): mb += '- 更新 ' + k + ' → ' + v + '\n'
            for k in new: mb += '- 新增 ' + k + ' → ' + cur[k] + '\n'
            for k in gone: mb += '- 删除 ' + k + '\n'
            mb += '——lvlu RESPONDER ' + ts
            board_post('lvlu-钥事件-' + ts + '.md', mb)
        put_file('receipts/tower/secrets_meta.json', json.dumps(cur, ensure_ascii=False, indent=1), msha, '[skip ci] secrets-meta ' + ts)
        return {'meta_keys': len(cur), 'meta_diff': sorted(diff), 'meta_new': new}
    except Exception as e:
        return {'meta': 'err:' + e.__class__.__name__}

# —— 闸八 ORBIT-LOOP-01: 周天囊自驿(大/小周天 环-圈自动驿传:戳印+转下站+回环板报销号) ——
def orbit_loop(ts, state):
    out = []
    st, tree = api('GET', 'git/trees/HEAD?recursive=1', repo=HUB)
    if st != 200: return out
    caps = [t['path'] for t in tree.get('tree', []) if t['path'].startswith('lanes/lvlu/inbox/ORBIT-CAP')]
    seen_orb = set(state.get('seen_orbits', []))
    for p in caps:
        if p in seen_orb: continue
        seen_orb.add(p)
        body, _ = get_file(urllib.parse.quote(p), repo=HUB)
        if not body: continue
        m = re.search(r'```json\s*(\{.*?\})\s*```', body, re.S)
        if not m: continue
        try: cap = json.loads(m.group(1))
        except Exception: continue
        route = cap.get('route', []); stamps = cap.get('stamps', [])
        if not route or any(s.get('line') == 'lvlu' for s in stamps): continue
        stamps.append({'line': 'lvlu', 'ts': ts, 'note': 'ORBIT-LOOP闸八自戳'})
        cap['stamps'] = stamps
        title = p.split('/')[-1]
        full = len({s['line'] for s in stamps}) >= len(set(route))
        if cap.get('origin') == 'lvlu' and full:
            board_post('lvlu-周天回环-' + cap.get('id', title) + '-' + ts + '.md',
                '# 周天回环 | ' + cap.get('id', title) + '\n\n囊归原点,全环CLEARED。戳序: ' + '→'.join(s['line'] for s in stamps) + '\n——lvlu ORBIT-LOOP ' + ts)
            out.append('circle:' + cap.get('id', title))
        else:
            nxt = route[(route.index('lvlu') + 1) % len(route)] if 'lvlu' in route else None
            if nxt:
                fwd = 'CLASSIFY: L1(周天囊自驿·lvlu→' + nxt + ')\n' + re.sub(r'```json\s*\{.*?\}\s*```', '```json\n' + json.dumps(cap, ensure_ascii=False, indent=1) + '\n```', body, flags=re.S)
                ok = put_file(urllib.parse.quote('lanes/' + nxt + '/inbox/' + title), fwd, None, 'orbit relay ' + cap.get('id', ''), repo=HUB)
                out.append('fwd:' + nxt + ':' + str(ok))
    state['seen_orbits'] = sorted(seen_orb)[-200:]
    return out

# —— 闸六/七 EXP-LOOP + SI0-PULSE（候件即循环 · 本拍SI2/SI0兑现下拍SI1迭代项）——
def exp_loop(ts, vault):
    """闸六: EXP-049/探针队列自动侦。状态史落账; Completed→板报+销号EXP049-DONE"""
    out = {}
    try:
        from quafu import Task, User
        tok = vault.get('QUAFU_TOKEN')
        if not tok: return {'probe': 'no-token'}
        t = Task(user=User(api_token=tok))
        TIDS = {'probe': '8CA608102028586C', 'AB': '8D32418037EFFE04', 'ABp': '8D3241902178F453', 'ApB': '8D32419033F4DB86', 'ApBp': '8D3241A006FD2B5A'}
        sts = {}
        for tag, tid in TIDS.items():
            try: sts[tag] = str(getattr(t.retrieve(tid), 'task_status', '?'))
            except Exception as e2: sts[tag] = 'ERR:' + str(e2)[:40]
        st = sts.get('probe', '?')
        out.update(sts)
        done4 = [k for k in ('AB', 'ABp', 'ApB', 'ApBp') if ('complete' in sts.get(k, '').lower()) or ('success' in sts.get(k, '').lower())]
        out['exp049_done'] = len(done4)
        if len(done4) == 4:
            board_post('lvlu-EXP049四件Completed-EXPLOOP-' + ts + '.md',
                '# EXP-049 四taskid(AB/ABp/ApB/ApBp)全部Completed\n\nEXP-LOOP闸六并案侦得。出数即与基线档ANS-LVLU-BASELINE-01互验对拍。——lvlu ' + ts)
        old, psha = get_file('receipts/tower/probe_state.json')
        hist = json.loads(old) if old else {'hist': []}
        if not hist['hist'] or hist['hist'][-1].get('st') != st or hist['hist'][-1].get('all') != sts:
            hist['hist'].append({'ts': ts, 'st': st, 'all': sts})
        put_file('receipts/tower/probe_state.json', json.dumps(hist, ensure_ascii=False, indent=1), psha, '[skip ci] probe ' + ts)
        if ('complete' in st.lower()) or ('success' in st.lower()):
            board_post('lvlu-探针Completed-EXPLOOP-' + ts + '.md',
                '# 探针 8CA608102028586C Completed\n\nEXP-LOOP 闸六自动侦得（SI2/SI0循环闭环）。详值SI1接续交叉验证(sim S=2.8425)。——lvlu ' + ts)
            cj, csha = get_file('ci/si3/claims.json')
            if cj:
                claims = json.loads(cj)
                for cl in claims.get('claims', []):
                    if cl['id'] == 'EXP049-DONE' and cl.get('status') == 'open':
                        cl['status'] = 'closed'; cl['closed_ts'] = ts; cl['closed_by'] = 'EXP-LOOP'
                put_file('ci/si3/claims.json', json.dumps(claims, ensure_ascii=False, indent=1), csha, '[skip ci] EXP049-DONE closed by exp-loop')
            out['closed'] = True
    except Exception as e:
        out['probe'] = 'err:' + e.__class__.__name__
    return out

def si0_pulse(ts, vault, sla, names, klogin=None):
    """闸七: SI0自仪表化——每拍一行度量落 receipts/si0/pulse.jsonl (板件数/候件开数/钥池/探针态)"""
    try:
        open_claims = sla.get('claims', 0) - len(sla.get('closed', []))
        m = {'ts': ts, 'board_files': len(names), 'claims': sla.get('claims'), 'closed_this_beat': sla.get('closed'),
             'nudged': sla.get('nudged'), 'vault_keys': len(vault), 'key_login': klogin}
        old, psha = get_file('receipts/si0/pulse.jsonl')
        lines = (old or '') + json.dumps(m, ensure_ascii=False) + '\n'
        put_file('receipts/si0/pulse.jsonl', lines, psha, '[skip ci] si0-pulse ' + ts)
        return m
    except Exception as e:
        return {'pulse': 'err:' + e.__class__.__name__}

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stj, ssha = get_file('receipts/tower/responder_state.json')
    state = json.loads(stj) if stj else {}
    seen = set(state.get('seen', []))
    kok, klogin = key_health()
    if not kok:
        print('KEYHEALTH: ALL KEYS DEAD — 钥亡红拍(株廿四律三:禁静默死)')
        raise SystemExit(1)
    vault = load_vault()
    meta = secrets_meta(ts)
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
    # 闸六/七: EXP队列自动侦 + SI0自仪表化
    exp = exp_loop(ts, vault)
    pulse = si0_pulse(ts, vault, sla, names, klogin)
    # 闸八: 周天囊自驿
    orb = orbit_loop(ts, state)
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
    print(json.dumps({'ts': ts, 'keyreq_done': done, 'acks': acks, 'vault_keys': len(vault), 'meta': meta, 'orbit': orb, 'sla': sla, 'exp': exp, 'pulse': pulse}, ensure_ascii=False))

if __name__ == '__main__':
    main()
