"""One saved-acquisition chain. No serving, production expansion, or qualification."""
import importlib.util, argparse, copy, hashlib, io, json, os, stat, subprocess, sys, time, traceback, zipfile
from pathlib import Path, PurePosixPath

class Rejected(ValueError): pass
def need(ok, why):
    if not ok: raise Rejected(why)
def enc(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def parse(b):
    def pairs(items):
        d={}
        for k,v in items:
            need(k not in d,'DUPLICATE-KEY');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(Rejected('NONFINITE')))
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def same(a,b,why): need(enc(a)==enc(b),why)
def read(p):
    p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR:'+str(p))
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:return f.read()
def load(p):return parse(read(p))
def write(p,v):
    with Path(p).open('xb') as f:f.write(enc(v)+b'\n')
def pins():
    # A fresh parse prevents returned results from mutating later expectations.
    p=Path(__file__).resolve().parents[1]/'provenance/pins.json';raw=read(p)
    need(ident(raw)['sha256']==PIN_SHA,'INTEGRATION-PINS')
    return parse(raw)
def archive(path,pin):
    raw=read(path);same(ident(raw),pin,'ARCHIVE-PIN')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist();need(len(names)==len(set(names)) and z.testzip() is None,'ARCHIVE-CRC-MEMBERSHIP')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            need(not p.is_absolute() and '..' not in p.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'ARCHIVE-ENTRY')
        m=parse(z.read('MANIFEST.json'));need(set(names)==set(m)|{'MANIFEST.json'},'ARCHIVE-EXACT-MEMBERSHIP')
        for n,v in m.items():same(ident(z.read(n)),v,'ARCHIVE-MEMBER:'+n)
        return {n:z.read(n) for n in names}
def tree(root,m):
    root=Path(root);need(stat.S_ISDIR(root.lstat().st_mode),'ROOT-TYPE')
    dirs={str(p) for n in m for p in Path(n).parents if str(p)!='.'};seen=set()
    def walk(d):
        for f in d.iterdir():
            n=f.relative_to(root).as_posix();mode=f.lstat().st_mode
            if stat.S_ISDIR(mode):need(n in dirs,'EXTRA-DIRECTORY:'+n);walk(f)
            else:
                need(stat.S_ISREG(mode) and n in m,'UNDECLARED-ENTRY:'+n)
                same(ident(read(f)),m[n],'TREE-IDENTITY:'+n);seen.add(n)
    walk(root);need(seen==set(m),'TREE-MEMBERSHIP')
def members(a): return {n:ident(b) for n,b in a.items()}
def preflight(config):
    p=pins();same(sorted(config),sorted(p['configuration_keys']),'CONFIGURATION-SCHEMA')
    c={k:Path(v).absolute() for k,v in config.items()};a={}
    for name in ('inputs','consumer','ledger'):
        a[name]=archive(c[name+'_archive'],p['archives'][name]);tree(c[name+'_root'],members(a[name]))
    counts_raw=a['inputs']['inputs/Engineering-288C-I164-evidence-count-receipts.zip']
    same(ident(read(c['counts_archive'])),ident(counts_raw),'COUNT-DEPENDENCY')
    a['counts']=archive(c['counts_archive'],ident(counts_raw));tree(c['counts_root'],members(a['counts']))
    for name in ('candidate','draft'):
        m=parse(a['inputs']['provenance/'+name+'-members.json']);tree(c[name],m)
    for role,owner,member in [('bundle','inputs','outputs/bundle.json'),('model','consumer','outputs/native.json'),('saved_ledger','ledger','outputs/ledger.json')]:
        need(read(c[role])==a[owner][member],'SELECTED-SAVED-STAGE:'+role)
    b=load(c['bundle']);n=load(c['model']);l=load(c['saved_ledger'])
    same([x['context'] for x in b['contexts']],['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'CONTEXT-ORDER')
    same([x['context'] for x in n['contexts']],[x['context'] for x in b['contexts']],'MODEL-CONTEXT')
    same([x['context'] for x in l['contexts']],[x['context'] for x in b['contexts']],'LEDGER-CONTEXT')
    same(b['obligations'],n['obligations'],'MODEL-OBLIGATIONS');same(b['obligations'],l['obligations'],'LEDGER-OBLIGATIONS')
    same([x['id'] for x in b['obligations']['source_only']],['O%02d'%i for i in range(1,12)],'ELEVEN-OBLIGATIONS')
    for obj in (b,n,l):
        same(obj['classification'],'UNKNOWN','UNKNOWN');same(obj['final_binding'],'BLOCKED','FINAL-BINDING');need(obj['actual_admission'] is False,'ADMISSION')
    same(l['binding'],{'finite_model':ident(read(c['model'])),'acquisition':b['acquisition_id']},'MODEL-LEDGER-BINDING')
    # The reviewed count component owns exact acquisition/evaluation archives.
    sources={k:ident(read(v)) for k,v in c.items() if k.endswith('_archive') or k in ('bundle','model','saved_ledger')}
    for name in ('candidate','draft'):sources[name+'_members']=ident(a['inputs']['provenance/'+name+'-members.json'])
    for n,raw in a['counts'].items():
        if n.startswith('inputs/') and n.endswith('.zip'):sources['count-component/'+n]=ident(raw)
    code={}
    for name in ('inputs','consumer','ledger','counts'):
        for n,raw in a[name].items():
            if n.startswith('code/') and n.endswith('.py'):code[name+'/'+n]=ident(raw)
    same(ident(read(Path(__file__).with_name('copies.py'))),COPY_PIN,'COPY-VALIDATOR-PIN')
    same(ident(read(Path(__file__).with_name('multiplicity.py'))),EXPRESSION_PIN,'EXPRESSION-VALIDATOR-PIN')
    for n in ('connect.py','worker.py','copies.py','multiplicity.py'):code['integration/'+n]=ident(read(Path(__file__).with_name(n)))
    return {'inputs':sources,'code':code,'acquisition':b['acquisition_id'],'contexts':[x['context'] for x in b['contexts']],
            'obligations':copy.deepcopy(b['obligations']),'scope':'FINITE-SAVED-ACQUISITION-ONLY',
            'classification':'UNKNOWN','assessment':'SOURCE-ONLY','production_cardinalities':None,'global_lifetime_bound':None,
            'canonical_ledger_rebound':False,'canonical_registration':False,'complete_native_model':False,
            'full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY'}
def stage(output,name,script,args):
    target=output/name
    cmd=[sys.executable,'-I','-B',str(Path(__file__).with_name('worker.py')),str(script),*map(str,args),'--output',str(target)]
    print('Running '+name+' (saved files only)',flush=True);start=time.monotonic()
    with (output/(name+'.log')).open('xb') as log:
        proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
        while True:
            try:rc=proc.wait(timeout=30);break
            except subprocess.TimeoutExpired:print(name+': '+str(int(time.monotonic()-start))+' seconds; no retry',flush=True)
    write(output/(name+'-execution.json'),{'command':cmd,'returncode':rc,'seconds':time.monotonic()-start})
    need(rc==0,'STAGE-FAILED:'+name)
def output_bindings(config,output,basis):
    """Internal linkage check; public run always executes all reviewed validators."""
    o=Path(output)
    files={'bundle':o/'01-inputs/bundle.json','input_validation':o/'01-inputs/validation.json',
      'model':o/'02-consumer/native.json','verification':o/'03-verification/result.json',
      'ledger':o/'04-ledger/ledger.json','ledger_result':o/'04-ledger/result.json'}
    for n,source in [('bundle','bundle'),('model','model'),('ledger','saved_ledger')]:need(read(files[n])==read(config[source]),'ACTUAL-OUTPUT-CORRESPONDENCE:'+n)
    verification=load(files['verification']);ledger_raw=read(files['ledger']);ledger=parse(ledger_raw);validation=load(files['input_validation'])
    need(ledger_raw==read(config['saved_ledger']),'ACTUAL-OUTPUT-CORRESPONDENCE:ledger')
    same(verification['submitted'],ident(read(files['model'])),'VERIFIED-MODEL-BYTES')
    same(ledger['verification_receipt'],verification,'LEDGER-CONSUMES-VERIFICATION')
    same(ledger['binding'],{'finite_model':ident(read(files['model'])),'acquisition':basis['acquisition']},'LEDGER-MODEL-ACQUISITION')
    same(ledger['obligations'],basis['obligations'],'ACTUAL-LEDGER-OBLIGATIONS')
    need(validation['all_eleven_obligations_preserved'] is True,'INPUT-OBLIGATIONS')
    for obj in (verification,ledger,validation):same([x['context'] for x in obj['contexts']],basis['contexts'],'ACTUAL-CONTEXT-ORDER')
    # ledger.py::summary/main defines this redundant result envelope. Derive all
    # claims from the exact validated ledger, never from the submitted summary.
    expected_ledger_result={
        'status':'PASS finite mechanical ledger correspondence',
        'binding':copy.deepcopy(ledger['binding']),
        'contexts':[{'context':c['context'],
                     'node_duties':len(c['node_duties']),
                     'relation_duties':len(c['relation_duties']),
                     'fold_duties':len(c['fold_duties']),
                     'token_members':sum(len(d['occurrence_keys']) for d in c['node_duties']),
                     'edge_members':sum(len(d['ordered_edges']) for d in c['relation_duties'])}
                    for c in ledger['contexts']],
        'source_only_obligations':len(ledger['obligations']['source_only']),
        'qualification_established':ledger['qualification_established'],
        'canonical_ledger_rebound':ledger['canonical_ledger_rebound'],
        'final_binding':ledger['final_binding'],
        'actual_admission':ledger['actual_admission'],
        'ledger':ident(ledger_raw)}
    ledger_result_raw=read(files['ledger_result'])
    same(parse(ledger_result_raw),expected_ledger_result,'LEDGER-RESULT-CORRESPONDENCE')
    bound_raw={'ledger':ledger_raw,'ledger_result':ledger_result_raw}
    return {'artifacts':{k:ident(bound_raw[k] if k in bound_raw else read(v)) for k,v in files.items()},
            'contexts':copy.deepcopy(verification['contexts']),
            'ledger_contexts':copy.deepcopy(expected_ledger_result['contexts'])}
COPY_PIN={'bytes':12631,'sha256':'9e8934ce5b74b525cb141df21c7b95c7f167c5fb4b7e93e6d284f0975d265271'}
STAGES=['saved-acquisition/finite-inputs','finite-consumer','finite-output-verification','mechanical-ledger-validation','carrier-copy-validation','carrier-expression-validation']
FORMAT='I164-CONNECTED-FINITE-RECEIPT-3'
def copy_config(config):
    return {'count_archive':str(config['counts_archive']),'count_root':str(config['counts_root']),
            'candidate':str(config['candidate']),'draft':str(config['draft'])}
def copy_bindings(config,output,basis):
    """Post-stage linkage; revalidate the actual receipt with the pinned public API."""
    path=Path(__file__).with_name('copies.py');raw=read(path);same(ident(raw),COPY_PIN,'COPY-VALIDATOR-PIN')
    spec=importlib.util.spec_from_file_location('connected_o09_validator',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    sys.addaudithook(module.denied)
    receipt_path=Path(output)/'05-copies/receipt.json';receipt_raw=read(receipt_path)
    submitted=load(receipt_path);need(type(submitted) is dict,'COPY-RECEIPT-TYPE')
    # The submitted receipt supplies no expected claims. The original public API
    # recomputes from exact current inputs, including the retained count consumer.
    checked=module.run(copy_config(config),submitted)
    same(parse(receipt_raw),checked,'COPY-CHECKED-BYTES')
    same(checked['acquisition_id'],basis['acquisition'],'COPY-ACQUISITION-BINDING')
    same(checked['obligations'],basis['obligations'],'COPY-OBLIGATIONS')
    same([c['context'] for c in checked['contexts']],basis['contexts'],'COPY-CONTEXTS')
    same(checked['bindings']['count_component'],basis['inputs']['counts_archive'],'COPY-COUNT-COMPONENT')
    for ar in checked['archives']:
        pin=ar['identity']
        need(pin in [v for k,v in basis['inputs'].items() if k.startswith('count-component/inputs/')], 'COPY-EVIDENCE-BINDING')
    summary_raw=read(Path(output)/'05-copies/result.json')
    expected_summary={'status':'PASS bounded O09 copy correspondence','receipt':ident(receipt_raw),
        'contexts':[c['context'] for c in checked['contexts']],
        'selected_database_payload_bytes':sum(p['identity']['bytes'] for p in checked['selected_database_payloads']),
        'obligations':len(checked['obligations']['source_only']),'full_expansion_ready':False}
    same(checked['selected_database_payload_bytes'],expected_summary['selected_database_payload_bytes'],'COPY-PAYLOAD-SUM')
    same(parse(summary_raw),expected_summary,'COPY-SUMMARY-CORRESPONDENCE')
    # Return selected payloads only, not an invented aggregate over archive,
    # export and member roles. Contexts never multiply physical bytes.
    return {'receipt':ident(receipt_raw),'result':ident(summary_raw),'validator':COPY_PIN.copy(),
        'acquisition':checked['acquisition_id'],'evidence':copy.deepcopy(checked['archives']),
        'source_bindings':copy.deepcopy(checked['bindings']),
        'contexts':copy.deepcopy(checked['contexts']),
        'selected_database_payload_bytes':expected_summary['selected_database_payload_bytes'],
        'byte_total_scope':checked['byte_total_scope'],
        'recorded_assertions':ident(enc(checked['capture_assertions'])),
        'obligations':ident(enc(checked['obligations'])),
        'physical_container_count':checked['physical_container_count'],
        'physical_storage_bytes':checked['physical_storage_bytes'],
        'global_lifetime_bound':checked['global_lifetime_bound'],
        'global_O09_closed':False,'assessment':checked['assessment'],
        'classification':checked['classification'],'operational_assurance':checked['operational_assurance'],
        'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False}

EXPRESSION_PIN = {'bytes': 13520, 'sha256': '91d9db56aef8b622ae823b8e63ed52c971a3223fb736c5a27d2cf5800ab939ae'}
def expression_config(config,output):
    return {**copy_config(config),'copy_receipt':str(Path(output)/'05-copies/receipt.json')}
def expression_bindings(config,output,basis,copy_links):
    """Validate current stage bytes, then derive all reported counts and bindings."""
    path=Path(__file__).with_name('multiplicity.py')
    same(ident(read(path)),EXPRESSION_PIN,'EXPRESSION-VALIDATOR-PIN')
    spec=importlib.util.spec_from_file_location('connected_o06_validator',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    raw=read(Path(output)/'06-expressions/receipt.json')
    checked=module.run(expression_config(config,output),parse(raw))
    same(checked['acquisition_id'],basis['acquisition'],'EXPRESSION-ACQUISITION')
    same(checked['bindings']['copy_receipt'],copy_links['receipt'],'EXPRESSION-ACTUAL-COPY')
    same(checked['bindings']['count_and_procedure'],copy_links['source_bindings'],'EXPRESSION-COUNT-PROCEDURE')
    same(checked['contexts'],copy_links['contexts'],'EXPRESSION-COPY-CONTEXTS')
    same([c['context'] for c in checked['contexts']],basis['contexts'],'EXPRESSION-CONTEXTS')
    same(checked['obligations'],basis['obligations'],'EXPRESSION-OBLIGATIONS')
    rows=checked['expressions'];known=sum(r['selected']['value'] is not None for r in rows)
    unknown=sum(r['lifetime']['value'] is None for r in rows)
    summary={'status':'PASS bounded carrier expression evaluation','expressions':len(rows),
             'selected_known':known,'lifetime_unknown':unknown,'receipt':ident(raw),
             'obligations':len(checked['obligations']['source_only'])}
    summary_raw=read(Path(output)/'06-expressions/result.json')
    same(parse(summary_raw),summary,'EXPRESSION-SUMMARY-CORRESPONDENCE')
    return {'receipt':ident(raw),'result':ident(summary_raw),'validator':copy.deepcopy(EXPRESSION_PIN),
            'bindings':copy.deepcopy(checked['bindings']),'acquisition':checked['acquisition_id'],
            'contexts':copy.deepcopy(checked['contexts']),'context_use':checked['context_use'],
            'expression_count':len(rows),'selected_known':known,'inventory_gaps':len(rows)-known,
            'lifetime_unknown':unknown,'expressions':copy.deepcopy(rows),
            'obligations':ident(enc(checked['obligations'])),
            'assessment':checked['assessment'],'classification':checked['classification'],
            'physical_storage_bytes':checked['physical_storage_bytes'],
            'global_lifetime_bound':checked['global_lifetime_bound'],
            'global_O06_closed':checked['global_O06_closed'],'global_O09_closed':checked['global_O09_closed'],
            'full_expansion_ready':checked['full_expansion_ready'],'final_binding':checked['final_binding'],
            'actual_admission':checked['actual_admission']}
def validate_final(submitted,expected):
    same(submitted,expected,'DETACHED-OR-ALTERED-RECEIPT')

def run(config,output,submitted=None):
    need(sys.version_info[:3]==(3,12,14) and sys.flags.optimize==0,'INTERPRETER-APPLICABILITY')
    output=Path(output).absolute();need(not os.path.lexists(output) and '/tmp' not in str(output),'NEW-PERSISTENT-OUTPUT')
    protected=[Path(__file__).resolve().parents[1]]
    need(type(config) is dict,'CONFIGURATION-TYPE')
    for key in ('inputs_root','consumer_root','ledger_root','counts_root','candidate','draft'):
        need(key in config and type(config[key]) is str,'REQUIRED-PROTECTED-ROOT:'+key)
        protected.append(Path(config[key]).resolve())
    resolved=output.resolve()
    need(all(resolved!=root and root not in resolved.parents for root in protected),'OUTPUT-INSIDE-PROTECTED-INPUT')
    output.mkdir(parents=True)
    try:
        basis=preflight(config)
        if submitted is not None:
            same(submitted.get('basis'),basis,'RECEIPT-CURRENT-BASIS')
            same(submitted.get('format'),FORMAT,'RECEIPT-FORMAT')
            same(submitted.get('stages'),STAGES,'RECEIPT-STAGES')
            same(sorted(submitted),['basis','format','outputs','stages'],'RECEIPT-SCHEMA')
        c={k:Path(v).absolute() for k,v in config.items()}
        stage(output,'01-inputs',c['inputs_root']/'code/finite_inputs.py',['validate','--component',c['counts_root'],'--root',c['candidate'],'--draft',c['draft'],'--bundle',c['bundle']])
        # The consumer API takes an authenticated archive, not a bundle path.
        # Require exact equality to this just-validated output before that API call.
        need(read(output/'01-inputs/bundle.json')==read(c['bundle']),'CONSUMER-INPUT-BRIDGE')
        stage(output,'02-consumer',c['consumer_root']/'code/consumer.py',['--component',c['inputs_archive'],'--submitted',c['model']])
        stage(output,'03-verification',c['ledger_root']/'code/verify_finite.py',['--component',c['inputs_archive'],'--consumer',c['consumer_archive'],'--submitted',output/'02-consumer/native.json'])
        stage(output,'04-ledger',c['ledger_root']/'code/ledger.py',['--component',c['inputs_archive'],'--consumer',c['consumer_archive'],'--model',output/'02-consumer/native.json','--submitted',c['saved_ledger']])
        write(output/'copy-config.json',copy_config(config))
        stage(output,'05-copies',Path(__file__).with_name('copies.py'),['--config',output/'copy-config.json'])
        links=output_bindings(c,output,basis)
        links['carrier_copy']=copy_bindings(config,output,basis)
        write(output/'expression-config.json',expression_config(config,output))
        stage(output,'06-expressions',Path(__file__).with_name('multiplicity.py'),['--config',output/'expression-config.json'])
        links['carrier_expressions']=expression_bindings(config,output,basis,links['carrier_copy'])
        same(preflight(config),basis,'INPUTS-CHANGED-DURING-VALIDATION')
        receipt={'format':FORMAT,'basis':basis,'stages':list(STAGES),'outputs':links}
        if submitted is not None:validate_final(submitted,receipt)
        write(output/'receipt.json',receipt)
        print('PASS bounded connected finite correspondence; readiness/final binding BLOCKED; admission disabled',flush=True)
        return copy.deepcopy(receipt)
    except BaseException:
        (output/'failure.txt').write_text(traceback.format_exc());raise

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);ap.add_argument('--receipt');a=ap.parse_args()
    submitted=load(a.receipt) if a.receipt is not None else None
    if a.receipt is not None:need(type(submitted) is dict,'RECEIPT-TYPE')
    run(load(a.config),a.output,submitted)
PIN_SHA = '290d5211d90932476ec5f93ea60de5089b3445fe34caa6e287e4f772224e989e'
if __name__=='__main__':main()
