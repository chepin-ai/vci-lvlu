#!/usr/bin/env python3
# LVLU-RESPONDER-01 v3.13(株45候root即自缚律: 闸十二SESSDELIV-01道乙sealed投递R3自办/私钥唯会话vault/取件即焚; v3.12株44)(株44: exp闸提序+预算600s治skip-budget变相候/NUDGE_CH补cisvr·ucif2·qgl·qtlv巷靶/闸十一SEALED-RAIL自注册应usrm PA181-1①; v3.11株43促件幂等)(株43促件幂等律NUDGE-IDEM-01: 靶面实迹为凭近3h同id免促,治usrm勘EXP049-L23×67风暴; v3.10株42闸不连坐)(株42闸不连坐律: detect_open_lines之w→NameError殉道15h修复+闸级故障隔离state必落盘; v3.9株卅八v1.1读域律)(株卅八v1.1读域律READ_MESH_PAT落即展; v3.8株卅九时箱律TIMEBOX-01+闸级自仪表; v3.7株卅八域界律; v3.6 SCAN-OWN-KEYS-01写前闸; v3.5株卅五无戳contains补检+h_key分级健康; 株卅四need_lines检全径+株卅二contains兜底; 闸十INBOX-SWEEP; watch双道)(株廿五 NUDGE-TARGET-01: need_lines分线定向) — lvlu线 SI3专候响应环（KEYHEALTH/SECRETS-META/KEYREQ/DISC/SI1-WAKE/SLA/NUDGE/EXP/PULSE/ORBIT 十件）
# 职: ⓪每拍验钥回退链+secrets元数据差分(株廿四) ①钥取件即见即注 ②指名lvlu件即收讫 ③SI1-WAKE常新 ⑧周天囊自驿
# 律: 零定时(事驱入拍) / 值不过板不落盘(内存即用即焚) / names-only回执 / 非白名单→裁示候root
import os, json, base64, urllib.request, urllib.parse, datetime, re, hashlib

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-lvlu')
import time as _t0m
BEAT_T0 = _t0m.time()  # 株卅九: 拍始钟(时箱律预算基准)
# 株卅八 域界律 DOMAIN-01(FINE_OWN_PAT_LVLU三仓域): 域外404=域界非仓亡(不警不默零, 一次性板声明+日志); 域内404=真仓亡警(株廿三)
DOMAIN_REPOS = {'ci-inbox', 'vci-inbox', 'vci-lvlu'}
def in_domain(repo_full):
    return repo_full.split('/')[-1] in DOMAIN_REPOS
TOK  = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')

def key_health():
    """株廿四律三 KEYHEALTH-01: 每拍 /user 体检。主钥401→回退链(LINE_PAT→CI_OPS_LINE_KEY→GITHUB_TOKEN);全灭→红拍exit1(禁静默死)
    株卅五附律 h_key: qfa式分级健康 h=Σmax(P,0)/|keys|; h<0.85→钥况警板(降级不静默, 日件名幂等)"""
    global TOK
    cands = [(nm, os.environ.get(nm)) for nm in ('LINE_PAT', 'CI_OPS_LINE_KEY', 'GITHUB_TOKEN')]
    cands = [(nm, t) for nm, t in cands if t]
    ok_login = None; alive = 0
    for nm, t in cands:
        req = urllib.request.Request('https://api.github.com/user', headers={'Authorization': 'Bearer ' + t, 'Accept': 'application/vnd.github+json', 'User-Agent': 'lvlu-responder'})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status == 200:
                    alive += 1
                    if ok_login is None:
                        if t != TOK: print('KEYHEALTH: fallback in use (' + nm + ')')
                        TOK = t
                        ok_login = json.loads(r.read()).get('login', '?')
        except Exception: pass
    h = alive / len(cands) if cands else 0.0
    if ok_login and h < 0.85:
        d = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d')
        board_post('lvlu-钥况警-' + d + '.md',
            '# 钥况警: h_key=%.2f < 0.85\n\n回退链 %d 钥存活 %d。株卅五附律：分级健康（qfa式 M(t+1)=M(t)⊕(ΔS⊗P)）——降级不静默，请补钥。——lvlu' % (h, len(cands), alive))
    return (ok_login is not None), ok_login, h
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

RTOK = os.environ.get('READ_MESH_PAT')  # 株卅八v1.1 读域律: 只读PAT(全vci-*系R)落Secrets即读域自展; 未设=三仓域旧行为
def api(method, path, data=None, repo=None, read_alt=False):
    url = f'https://api.github.com/repos/{repo or REPO}/{path}'
    tok = (RTOK or TOK) if read_alt else TOK
    req = urllib.request.Request(url, method=method,
        headers={'Authorization': f'Bearer {tok}', 'Accept': 'application/vnd.github+json', 'User-Agent': 'lvlu-responder'})
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

# —— SCAN-OWN-KEYS-01 写前闸(qfa GUIDE参考实现+泛型七模式; 片段运行时派生永不落仓)——
VAULT_G = {}
GENERIC_PATS = [r'ghp_[A-Za-z0-9]{30,}', r'gho_[A-Za-z0-9]{30,}', r'ghs_[A-Za-z0-9]{30,}',
                r'ghu_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}', r'sk-[A-Za-z0-9]{20,}', r'AKID[A-Za-z0-9]{13,}']
def scan_out(text):
    """SCAN-OWN-KEYS-01: 凡出文先扫自钥环派生片段+泛型钥形; BLOCK即不放行(机旗永不录子串)"""
    import hashlib as _hs
    for k in list(VAULT_G.values()) + ([TOK] if TOK else []):
        if not k: continue
        for f in (k[:8], k[-8:], _hs.sha256(k.encode()).hexdigest()[:8]):
            if f and f in text: return 'BLOCK: own-key fragment'
    for p in GENERIC_PATS:
        if re.search(p, text): return 'BLOCK: generic-pattern'
    return None

def board_post(title, body):
    blk = scan_out((title or '') + (body or ''))
    if blk:
        print('SCAN-OWN-KEYS-01 BLOCK(board_post):', blk)  # 机旗永不录子串
        return None
    return put_file(urllib.parse.quote('公告板/' + title), body, None, title + ' [skip ci]', repo=HUB)


# —— 闸四/五 SLA-LOOP + NUDGE-ESCALATE-01（usrm三件套 claims.json 融合领养 · C案落实）——
NUDGE_CH = {
  'cisvr': {'otp': 'ci-control', 'dispatch': None, 'lane': 'cisvr', 'inbox': None},  # 株44: 巷靶补(旧lane=None→L1空促SI5CLOUD-CISVR案)
  'ucif2': {'lane': 'ucif2', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-ucif2', 'ucif2-wake'), 'inbox': ('chepin-ai/vci-ucif2', 'inbox/')},  # 株44: ucif2靶道新增(同案)
  'qgl': {'lane': 'qgl', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qgl', 'qgl-wake'), 'inbox': ('chepin-ai/vci-qgl', 'inbox/')},
  'qtlv': {'lane': 'qtlv', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qtlv', 'qtlv-wake'), 'inbox': ('chepin-ai/vci-qtlv', 'inbox/')},
  'usrm': {'lane': 'usrm', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-usrm', 'usrm-tower-kick'), 'inbox': ('chepin-ai/vci-usrm', 'inbox/')},
  'lgt': {'lane': 'lgt', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-lgt', 'lgt-wake'), 'inbox': ('chepin-ai/vci-lgt', 'inbox/')},
  'qlv': {'lane': 'qlv', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qlv', 'qlv-tower-kick'), 'inbox': ('chepin-ai/vci-qlv', 'inbox/')},
  'qfa': {'lane': 'qfa', 'otp': 'ci-control', 'dispatch': ('chepin-ai/vci-qfa', 'qfa-wake'), 'inbox': ('chepin-ai/vci-qfa', 'inbox/')},
}

def detect_claim(cl, trees_cache):
    """株廿九 双道检律: watch 多仓多缀(应件宣告诸道并检, 册堂/巷板无盲点); 无 watch 则 repo+prefix(es) 旧式兼容"""
    watch = cl.get('watch')
    if not watch:
        repo0 = cl.get('repo', 'ci-inbox')
        if repo0 == 'si1': return False
        watch = [{'repo': repo0, 'prefix': p} for p in (cl.get('prefixes') or [cl.get('prefix', '')])]
    since = cl.get('since', ''); cont = cl.get('contains', [])
    since_ts = cl.get('since_ts', ''); matched = []
    for w in watch:
        repo = w.get('repo', 'ci-inbox'); pre = w.get('prefix', '')
        if repo == 'si1': continue
        if repo not in trees_cache:
            st, tr = api('GET', 'git/trees/HEAD?recursive=1', repo='chepin-ai/' + repo, read_alt=not in_domain('chepin-ai/' + repo))
            if st in (403, 404) and not in_domain('chepin-ai/' + repo):
                # 株卅八 域界律: 域外仓403/404=域界(FINE_OWN_PAT三仓写域; v1.1 READ_MESH_PAT设则读域已展仍404=真亡→由读钥主自警), 日志不警不默零
                if not trees_cache.get('DOMOUT:' + repo):
                    trees_cache['DOMOUT:' + repo] = True
                    print('DOMAIN-01: 域外不侦 ' + repo + ' (株卅八)')
            elif st == 404 and not trees_cache.get('DEAD:' + repo):
                # 株廿三 REPO-EGUARD-01: 侦面仓存在性先验——仓亡即报警非默零
                trees_cache['DEAD:' + repo] = True
                board_post('lvlu-仓亡警-' + repo.replace('/', '-') + '-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.md',
                    '# 仓亡警: ' + repo + '\n\nclaims轨侦面仓 404（或改名/删除）。器课株廿三 REPO-EGUARD-01：存在性量化守卫——不默零。请核。——lvlu ' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
            trees_cache[repo] = [t['path'] for t in tr.get('tree', [])] if st == 200 else []
            trees_cache['SHA:' + repo] = {t['path']: t.get('sha', '') for t in tr.get('tree', [])} if st == 200 else {}
        for p in trees_cache[repo]:
            n = p[len(pre):] if p.startswith(pre) else None
            if n is None or 'lvlu' in n.lower(): continue
            # 株卅五附闸 sha_neq: 钉sha未变=无信号(册更自钉类唯sha异为据, 不凭件名/提交戳)
            sne = w.get('sha_neq') or cl.get('sha_neq')
            if sne and trees_cache.get('SHA:' + repo, {}).get(p, '').startswith(sne): continue
            # 器课株十七 DETECT-TS-01: 时戳正则优先, 无戳件不判
            mts = re.search(r'(20\d{6}T\d{4,6}Z{0,2})', n)
            if since_ts:
                if not mts:
                    # 株卅五 无戳补检律: 无戳件须 contains非空 ∧ commits验新>since_ts 方入检
                    # (治ANS-SI5CLOUD-LGT-01类漏检; 试拍否证WQREG册旧档/EVALR2-RESP旧促之滥闭)
                    contw0 = w.get('contains') or cont
                    if not contw0: continue
                    ck = 'MTIME:' + repo + ':' + p
                    if ck not in trees_cache:
                        stc, cm = api('GET', 'commits?path=' + urllib.parse.quote(p) + '&per_page=1', repo='chepin-ai/' + repo, read_alt=not in_domain('chepin-ai/' + repo))
                        trees_cache[ck] = cm[0]['commit']['committer']['date'] if (stc == 200 and cm) else ''
                    cmt = trees_cache[ck].replace('-', '').replace(':', '')
                    if not cmt or cmt <= since_ts: continue
                elif mts.group(1) <= since_ts: continue
            elif since and n <= since: continue
            contw = w.get('contains') or cont  # 株卅二: 件名token变体(如RIPPLE-qlv)以contains兜底
            if all(c.lower() in n.lower() for c in contw):
                matched.append(repo + ':' + p)  # 株卅四: need_lines检全径(非前缀余串)
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
            # 株卅五附闸 sha_neq: 钉sha未变=无信号(册更自钉类唯sha异为据, 不凭件名/提交戳)
            sne = cl.get('sha_neq')  # 株42修: 本函无循环件w(旧版误引detect_claim之w→NameError殉道15h)
            if sne and trees_cache.get('SHA:' + repo, {}).get(p, '').startswith(sne): continue
            if all(c.lower() in n.lower() for c in cont):
                got |= {ln for ln in need if ln in n}
    cl['legs_got'] = sorted(got)
    return [ln for ln in need if ln not in got]

def _idem_hit(trees_cache, repo_full, marker, hours=3):
    """株43 NUDGE-IDEM-01: 靶面实迹幂等——促件以靶面(板/巷)实迹为凭, 不唯册拍数;
    靶面已有同marker近N时促件→免促(殉道冻结/重放环亦不风暴, 治EXP049-L23×67案)"""
    try:
        rk = repo_full.split('/')[-1]
        if rk not in trees_cache:
            st, tr = api('GET', 'git/trees/HEAD?recursive=1', repo=repo_full, read_alt=not in_domain(repo_full))
            trees_cache[rk] = [t['path'] for t in tr.get('tree', [])] if st == 200 else []
        now = datetime.datetime.now(datetime.timezone.utc)
        best = None
        for fp in trees_cache[rk]:
            n = fp.split('/')[-1]
            if marker in n:
                m = re.search(r'(20\d{6}T\d{6}Z)', n)
                if m:
                    try:
                        t = datetime.datetime.strptime(m.group(1), '%Y%m%dT%H%M%SZ').replace(tzinfo=datetime.timezone.utc)
                        if (now - t).total_seconds() < hours * 3600 and (best is None or m.group(1) > best[0]):
                            best = (m.group(1), fp)
                    except Exception: pass
        return best[1] if best else None
    except Exception as e:
        print('IDEM-ERR(株43)', e.__class__.__name__)
        return None

def nudge(cl, ts, trees_cache=None):
    lvl = cl.get('nudge_level', 0) + 1
    tgt = cl.get('target', 'cisvr')
    if cl.get('need_lines') and trees_cache is not None:
        open_lines = detect_open_lines(cl, trees_cache)
        if open_lines: tgt = open_lines[0]  # 株廿五: 只促未达线,已答线免扰
    if trees_cache is None: trees_cache = {}
    # 株43: 靶面实迹幂等闸(板/巷近3时有同id促件→全道免促; 册冻结之治)
    hit = _idem_hit(trees_cache, 'chepin-ai/vci-inbox', '-' + cl['id'] + '-lvlu') or _idem_hit(trees_cache, HUB, 'nudge-' + cl['id'] + '-L')
    if hit:
        print('NUDGE-IDEM(株43) skip', cl['id'], '实迹:', hit.split('/')[-1])
        cl['last_nudge_beats'] = cl.get('beats', 0)  # 册亦随实迹冷却
        return ['idem-skip(株43):' + hit.split('/')[-1][:40]]
    ch = NUDGE_CH.get(tgt, {})
    msg = '# NUDGE-ESCALATE-01 L' + str(lvl) + ' | ' + cl['id'] + ' ' + cl.get('name', cl.get('note', '')) + '\n\n候件逾窗(' + str(cl.get('sla_beats')) + '拍)。lvlu RESPONDER 闸五自动促件。@' + tgt + ' 请直取/回执。——lvlu ' + ts
    acts = []
    cmsg = 'CLASSIFY: L1(联邦机器邮·lvlu→' + tgt + ' 闸五促件L' + str(lvl) + ')\n' + msg  # 器课株二十 GUARD-CLASSIFY-01
    if lvl >= 1 and ch.get('lane'):
        ok = put_file(urllib.parse.quote('lanes/' + ch['lane'] + '/inbox/nudge-' + ts + '-' + cl['id'] + '-lvlu.md'), cmsg, None, 'nudge ' + cl['id'], repo='chepin-ai/vci-inbox'); acts.append('lane:' + str(ok))
    if lvl >= 2 and ch.get('inbox'):
        rp, pre = ch['inbox']
        if in_domain(rp):
            ok = put_file(urllib.parse.quote(pre + 'nudge-' + ts + '-' + cl['id'] + '-lvlu.md'), cmsg, None, 'nudge ' + cl['id'], repo=rp); acts.append('inbox:' + str(ok))
        else: acts.append('inbox:domout(株卅八)')
    elif lvl >= 2 and ch.get('otp'):
        if in_domain('chepin-ai/ci-control'):
            ok = put_file(urllib.parse.quote('.ci-inbox/msg-' + ts + '-nudge-' + cl['id'] + '-L' + str(lvl) + '-lvlu.md'), cmsg, None, 'nudge-otp ' + cl['id'], repo='chepin-ai/ci-control'); acts.append('otp:' + str(ok))
        else: acts.append('otp:domout(株卅八)')
    if lvl >= 3 and ch.get('dispatch'):
        rp, ev = ch['dispatch']
        if in_domain(rp):
            st2, _ = api('POST', 'dispatches', {'event_type': ev}, repo=rp); acts.append('kick:' + str(st2))
        else: acts.append('kick:domout(株卅八)')
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
        try:
            _hit = detect_claim(cl, trees_cache)
        except Exception as e:
            print('CLAIM-ERR(株42)', cl.get('id'), e.__class__.__name__, str(e)[:60]); continue
        if _hit:
            evid = _hit
            cl['status'] = 'closed'; cl['closed_ts'] = ts; cl['evidence'] = evid
            board_post('lvlu-销号回执-' + cl['id'] + '-' + ts + '.md',
                '# 销号回执 | ' + cl['id'] + ' ' + cl.get('name', cl.get('note', '')) + '\n\nSLA-LOOP 检测答件至, 候件闭环。\n证据件: `' + str(evid) + '`（器课株十九 EVID-IN-RECEIPT-01: 回执必附证据件名, 可复算）\n——lvlu RESPONDER 闸四 ' + ts)
            closed.append(cl['id']); continue
        cl['beats'] = cl.get('beats', 0) + 1
        if cl.get('repo') == 'si1': pend.append(cl['id'])
        cd = cl.get('last_nudge_beats', -999)  # 株廿一 NUDGE-COOLDOWN-01: 冷却拍距随级数指数扩
        if cl['beats'] > cl.get('sla_beats', 6) and cl['beats'] - cd >= min(2 ** max(cl.get('nudge_level', 0) - 2, 0), 8):
            try:
                acts = nudge(cl, ts, trees_cache); cl['last_nudge_beats'] = cl['beats']
                nudged.append(cl['id'] + ':L' + str(cl['nudge_level']) + ':' + ','.join(acts))
            except Exception as e:
                print('NUDGE-ERR(株42)', cl.get('id'), e.__class__.__name__, str(e)[:60])
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

# —— 闸九 MIRROR-LOOP-01: 双镜制之机镜(SESSION-MIRROR-01 v0.1)——
# 驱动答root: SI1纬非薪不保每拍末投镜——塔驱机镜保底每拍必有(本闸),SI1醒拍席镜覆写提质
def mirror_loop(ts, state, sla, exp, orb):
    """每拍机镜: 本拍动作+新件+候件态 落 receipts/session-mirror/mirror.jsonl; 席镜(ci-inbox shared)醒拍覆写"""
    try:
        entry = {'ts': ts, 'kind': '机镜', 'claims_open': sla.get('claims'), 'closed': sla.get('closed'),
                 'nudged': sla.get('nudged'), 'exp': {k: v for k, v in (exp or {}).items() if k in ('probe','exp049_done')},
                 'orbit': orb, 'note': 'SI1席镜醒拍覆写(Q逐字+A判要); 本件=塔驱保底镜'}
        old, msha = get_file('receipts/session-mirror/mirror.jsonl')
        lines = (old or '') + json.dumps(entry, ensure_ascii=False) + '\n'
        keep = lines.strip().split('\n')[-500:]
        put_file('receipts/session-mirror/mirror.jsonl', '\n'.join(keep) + '\n', msha, '[skip ci] mirror ' + ts)
        return entry
    except Exception as e:
        return {'mirror': 'err:' + e.__class__.__name__}

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
        import time as _time
        if _time.time() - BEAT_T0 > 600: return {'probe': 'skipped-budget(株卅九v1.1:12min墙标定600s)'}
        from quafu import Task, User
        tok = vault.get('QUAFU_TOKEN')
        if not tok: return {'probe': 'no-token'}
        t = Task(user=User(api_token=tok))
        TIDS = {'probe': '8CA608102028586C', 'AB': '8D32418037EFFE04', 'ABp': '8D3241902178F453', 'ApB': '8D32419033F4DB86', 'ApBp': '8D3241A006FD2B5A'}
        sts = {}
        # 株卅九 时箱律 TIMEBOX-01: 外部API并发+单件25s硬顶, daemon线程不阻进程(Quafu挂死=responder超5min殉拍之治)
        import threading as _th
        res = {}
        def _retr(tag, tid):
            try: res[tag] = str(getattr(t.retrieve(tid), 'task_status', '?'))
            except Exception as e2: res[tag] = 'ERR:' + str(e2)[:40]
        ths = [_th.Thread(target=_retr, args=(tag, tid), daemon=True) for tag, tid in TIDS.items()]
        for th in ths: th.start()
        _end = _time.time() + 25  # 总窗25s(非逐件累加)
        for th in ths: th.join(timeout=max(0, _end - _time.time()))
        for tag in TIDS: sts[tag] = res.get(tag, 'TIMEOUT')
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

# —— 闸十 INBOX-SWEEP-01: 收件全量律(株三十:名序尾扫=盲; 每拍全量扫自巷,未录件即板警) ——
def inbox_sweep(ts, state):
    try:
        st, tree = api('GET', 'git/trees/HEAD?recursive=1', repo='chepin-ai/vci-inbox')
        if st != 200: return ['tree:' + str(st)]
        mine = sorted(t['path'] for t in tree.get('tree', []) if t['path'].startswith('lanes/lvlu/inbox/'))
        seen_i = set(state.get('seen_inbox', []))
        new = [p for p in mine if p not in seen_i and 'lvlu' not in p.split('/')[-1].lower() and not p.split('/')[-1].startswith('nudge-')]
        state['seen_inbox'] = sorted(seen_i | set(mine))[-400:]
        if new:
            board_post('lvlu-未录件警-' + ts + '.md',
                '# 未录件警 INBOX-SWEEP-01\n\n本拍自巷新件(株三十收件全量律):\n' + '\n'.join('- ' + p for p in new[:10]) + '\n——lvlu RESPONDER 闸十 ' + ts)
        return [p.split('/')[-1] for p in new[:10]]
    except Exception as e:
        return ['err:' + e.__class__.__name__]


# —— 闸十一 SEALED-RAIL-SELF-01: 甲轨自注册(usrm判点PA181-1裁问①注册17公钥之lvlu应; 幂等: key_id变方更) ——
def sealrail_loop(ts):
    """每拍验 research/SEALED-RAIL-LVLU-01.json: 无件或key_id漂移→取本仓actions公钥, 注册{repo,key_id,fp,ts,rail}——公钥本为加密面, 指纹唯sha256[:12]"""
    try:
        stk, pk = api('GET', 'actions/secrets/public-key')
        if stk != 200 or not pk.get('key'): return {'sealrail': 'http' + str(stk)}
        fp = hashlib.sha256(pk['key'].encode()).hexdigest()[:12]
        old, osha = get_file('research/SEALED-RAIL-LVLU-01.json')
        cur = json.loads(old) if old else {}
        if cur.get('key_id') == pk.get('key_id') and cur.get('fp') == fp:
            return {'sealrail': 'stable', 'fp': fp}
        doc = {'rail': 'SEALED-RAIL-LVLU-01', 'repo': REPO, 'key_id': pk.get('key_id'), 'fp': fp,
               'fp_alg': 'sha256[:12](public_key)', 'endpoint': 'GET /repos/' + REPO + '/actions/secrets/public-key',
               'ts': ts, 'note': '甲轨sealed-box直注注册面(qgl SEALED-RAIL-QGL-01式; KEY-UNIFY-01§三); 公钥值由root自持账号面取, 本册唯指纹'}
        put_file('research/SEALED-RAIL-LVLU-01.json', json.dumps(doc, ensure_ascii=False, indent=1), osha, '[skip ci] sealrail ' + ts)
        return {'sealrail': 'registered', 'fp': fp}
    except Exception as e:
        return {'sealrail': 'err:' + e.__class__.__name__}


def sealdeliv_loop(ts):
    """闸十二 SESSDELIV-01(道乙sealed投递; 株45候root即自缚律): 会话RSA公钥(research/SESSDELIV-PUBKEY-01.json)在→
    LINE_PAT值以RSA-OAEP-SHA256(openssl CLI)密封投 research/SESSDELIV-SEALED-01.json(幂等: 公钥fp漂移才重投);
    research/SESSDELIV-BURN-01.json在→删sealed件并止投(取件即焚,单副本库律)。值永不打印/永不落明文盘"""
    try:
        bdoc, _ = get_file('research/SESSDELIV-BURN-01.json')
        sold, ssha = get_file('research/SESSDELIV-SEALED-01.json')
        if bdoc:
            if sold and ssha:
                api('DELETE', 'contents/research/SESSDELIV-SEALED-01.json',
                    {'message': '[skip ci] sealdeliv burn ' + ts, 'sha': ssha})
                return {'sealdeliv': 'burned'}
            return {'sealdeliv': 'burn-clean'}
        pdoc, _ = get_file('research/SESSDELIV-PUBKEY-01.json')
        if not pdoc: return {'sealdeliv': 'no-pubkey'}
        pub = json.loads(pdoc)
        pem, fp = pub.get('pem', ''), pub.get('fp', '')
        if not pem or not fp: return {'sealdeliv': 'pubkey-bad'}
        val = os.environ.get('LINE_PAT')
        if not val: return {'sealdeliv': 'no-val'}
        if sold:
            try:
                cur = json.loads(sold)
                if cur.get('pubkey_fp') == fp: return {'sealdeliv': 'stable', 'fp': fp}
            except Exception: pass
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.pem', delete=False) as f:
            f.write(pem); tmp = f.name
        try:
            r = subprocess.run(['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', tmp,
                                '-pkeyopt', 'rsa_padding_mode:oaep', '-pkeyopt', 'rsa_oaep_md:sha256'],
                               input=val.encode(), capture_output=True, timeout=30)
            if r.returncode != 0: return {'sealdeliv': 'seal-fail'}
            b64 = base64.b64encode(r.stdout).decode()
        finally:
            try: os.unlink(tmp)
            except Exception: pass
        doc = {'v': 'SESSDELIV-SEALED-01', 'alg': 'RSA-OAEP-SHA256', 'pubkey_fp': fp, 'ts': ts, 'b64': b64,
               'note': '道乙sealed投递(株45): 会话公钥密封FINE_OWN_PAT_LVLU, 取件即焚; 焚标志=research/SESSDELIV-BURN-01.json; 值域律: 密文非值, 全程无明文'}
        ok = put_file('research/SESSDELIV-SEALED-01.json', json.dumps(doc, ensure_ascii=False, indent=1), ssha, '[skip ci] sealdeliv ' + ts)
        return {'sealdeliv': 'delivered' if ok else 'put-fail', 'fp': fp}
    except Exception as e:
        return {'sealdeliv': 'err:' + e.__class__.__name__}

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stj, ssha = get_file('receipts/tower/responder_state.json')
    state = json.loads(stj) if stj else {}
    seen = set(state.get('seen', []))
    kok, klogin, kh = key_health()
    if not kok:
        print('KEYHEALTH: ALL KEYS DEAD — 钥亡红拍(株廿四律三:禁静默死)')
        raise SystemExit(1)
    vault = load_vault()
    VAULT_G.update(vault)  # SCAN-OWN-KEYS-01: 自钥环供扫(内存即用)
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
                for rp in repos:
                    if in_domain(rp): res.setdefault(k, []).append(f'{rp}:{inject(rp, k, vault[k])}')
                    else: res.setdefault(k, []).append(f'{rp}:domout域外未注(株卅八)')
        miss = [k for k in asked if k not in vault]
        if asked:
            rb = f'# 钥注回执 — {n}\n\n时戳 {ts}Z 签发 lvlu(RESPONDER-01 自动)\n\n'
            for k, rr in res.items(): rb += f'- **{k}** → sealed-box 注入: ' + ', '.join(rr) + '\n'
            if miss: rb += f'- 非白名单/库缺: {miss} → 裁示候 root（永不自动）\n'
            rb += '\n值不过板/不落盘/内存即用即焚。吊销=删副本+轮换。#noauto'
            board_post(f'钥注回执-{line}-lvlu-auto-{ts}Z.md', rb)
            done.append(n)
    # 闸二 DISC-LOOP: 指名lvlu件轻收讫(每拍≤3)
    for n in names:  # 株42: 闸一/闸二单件级隔离在环内

        if n in seen or len(acks) >= 3: continue
        if (LINE in n.lower() or re.search(r'钥注回执|OTP@lvlu', n)) and not n.startswith(('lvlu-', '钥注回执', '钥取-')):
            seen.add(n); acks.append(n)
    # 株42 闸不连坐律: 闸级故障隔离——任何一闸崩/错, 记日志给默认值, state/wake 必落盘(治NameError殉道15h类)
    import time as _tm
    def _gate(nm, fn, default):
        _t = _tm.time()
        try:
            r = fn()
            print('GATE %s %.1fs' % (nm, _tm.time() - _t))
            return r
        except Exception as e:
            print('GATE-ERR(株42) %s %s %.1fs %s' % (nm, e.__class__.__name__, _tm.time() - _t, str(e)[:80]))
            return default
    # 闸六: EXP队列自动侦(株44提序: 廉价高值闸先行——读域展后sla树取件慢, exp后置=永skip-budget变相候之治)
    exp = _gate('exp', lambda: exp_loop(ts, vault), {'probe': 'gate-err(株42)'})
    # 闸四/五: 索件轨+升级促件
    sla = _gate('sla', lambda: sla_loop(ts, seen), {'claims': 0, 'si1_pending': [], 'gate_err': 1})
    pending_si1 = sla.get('si1_pending', [])
    pulse = _gate('pulse', lambda: si0_pulse(ts, vault, sla, names, klogin), {'pulse': 'gate-err(株42)'})
    # 闸八: 周天囊自驿
    orb = _gate('orbit', lambda: orbit_loop(ts, state), ['gate-err(株42)'])
    # 闸九: 机镜保底
    mir = _gate('mirror', lambda: mirror_loop(ts, state, sla, exp, orb), {'mirror': 'gate-err(株42)'})
    # 闸十: 收件全量扫
    ins = _gate('inbox', lambda: inbox_sweep(ts, state), ['gate-err(株42)'])
    # 闸十一: 甲轨自注册(株44)
    sr = _gate('sealrail', lambda: sealrail_loop(ts), {'sealrail': 'gate-err(株42)'})
    # 闸十二: 道乙sealed投递(株45候root即自缚律——R3自办, 不候root道甲)
    sd = _gate('sealdeliv', lambda: sealdeliv_loop(ts), {'sealdeliv': 'gate-err(株42)'})
    # 闸三 SI1-WAKE: 会话接续锚常新
    wake = {'ts': ts, 'keyreq_done': done, 'acks': acks,
            'pending_si1': pending_si1,
            'note': '会话端醒后读本件+REBUILD.md→续办pending; 塔拍自治不候'}
    old, wsha = get_file('receipts/tower/SI1-WAKE.md')
    put_file('receipts/tower/SI1-WAKE.md',
             '# SI1-WAKE（lvlu 响应器·接续锚）\n\n```json\n' + json.dumps(wake, ensure_ascii=False, indent=1) + '\n```\n', wsha,
             '[skip ci] responder wake ' + ts)
    state = {'ts': ts, 'seen': sorted(seen)[-400:], 'done': (state.get('done', []) + done)[-60:], 'seen_inbox': state.get('seen_inbox', [])[-400:], 'seen_orbits': sorted(set(state.get('seen_orbits', [])))[-100:]}
    put_file('receipts/tower/responder_state.json', json.dumps(state, ensure_ascii=False, indent=1), ssha, '[skip ci] responder state')
    print(json.dumps({'ts': ts, 'keyreq_done': done, 'acks': acks, 'vault_keys': len(vault), 'meta': meta, 'orbit': orb, 'mirror': mir, 'inbox_new': ins, 'sealrail': sr, 'sealdeliv': sd, 'sla': sla, 'exp': exp, 'pulse': pulse, 'h_key': kh}, ensure_ascii=False))

if __name__ == '__main__':
    main()
