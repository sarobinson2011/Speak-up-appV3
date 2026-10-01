# Exact retained source excerpts

Source SHA-256: 697689d376a40d1acde9e34683bf57b4c14d3cad75eb082d229cfbbaa7fd31e7

## schema generation

S70 lines 735–743.

```text
SCHEMAS={
'AUTHORIZATION-HEADER':'serialization-domain successor-generation-id mapping-id mapping-sha256 profile-id profile-sha256 authorization-id transition-occurrence-id determination-id authorized-state-id successor-state-relation-definition-id ordering-coordinate-set-digest dependency-coordinate-set-digest component-count'.split(),
'COMPONENT-BINDING':'component_order component_id binding_mode canonical_type_id authorization_context_digest bound_value'.split(),
'COMPARISON-ATTEMPT':'comparison_attempt_id generation_id mapping_id mapping_sha256 profile_id profile_sha256 authorization_id authorization_sha256 transition_occurrence_id determination_id authorized_state_id authorized_state_sha256 current_state_id current_state_sha256 stage result failure_code'.split(),
'COMPARISON-RESULT':'comparison_attempt_id transition_occurrence_id result failure_code'.split(),
'RECOVERY-RESULT':'transition_occurrence_id comparison_attempt_id stage event unchanged_d_sufficiency disposition'.split(),
'OBSERVABILITY-OUTPUT':'transition_occurrence_id classification'.split(),
}
```

## surface generation

S70 lines 783–799.

```text
        self.schemas={k:list(v) for k,v in SCHEMAS.items()}
        for n,c in enumerate(components,1):
            need(c.mode in MODES and c.privacy in ('PUBLIC','ACTION-BOUNDED','CONFIDENTIAL','PRIVATE-ACTOR'),'component policy')
            self.schemas[f'COMPONENT-{n:04}']=['represented_value','canonical_value','blind','opening']
        self.surfaces=[]
        for schema,fields in self.schemas.items():
            for name in fields:
                exposure='PUBLIC' if schema=='OBSERVABILITY-OUTPUT' and public_output else 'CONFIDENTIAL'
                reuse='NONE';domain='OPAQUE';component=NA
                if name.replace('-','_')=='transition_occurrence_id':domain='ACTION-IDENTITY'
                if name in ('result','classification','failure_code','stage','event','unchanged_d_sufficiency','disposition','binding_mode','serialization-domain','canonical_type_id','component_id','component_order','component-count'):
                    reuse='GENERATION-CONSTANT';domain='CONSTANT:'+schema+'.'+name
                if schema.startswith('COMPONENT-0'):
                    c=components[int(schema[-4:])-1];component=c.id;domain='COMPONENT:'+c.id+'.'+name
                    if name in ('represented_value','canonical_value') and c.privacy in ('PUBLIC','PRIVATE-ACTOR'):exposure=c.privacy
                self.surfaces.append(Surface(len(self.surfaces)+1,schema,name,exposure,reuse,domain,component))
```

## canonical regeneration

S70 lines 1371–1374.

```text
        for name in ('schemas','byfield','byid','relations','expression_dependencies'):
            if getattr(profile,name,None)!=getattr(regenerated,name):
                failures.add('INVALID-PROFILE-SCHEMA')
```

## admission equality rule

S70 lines 914–919.

```text
    for x,y in combinations(tokens,2):
        sx=profile.byid[x.surface];sy=profile.byid[y.surface]
        arbitrary=lambda s:s.domain!='ACTION-IDENTITY' and s.reuse=='NONE'
        possible=admission and (arbitrary(sx) or arbitrary(sy))
        if x.digest==y.digest or possible:links.add((x.id,y.id,'000000','EQUALS'))
```

## correlation rule

S70 lines 944–954.

```text
    else:
        correlation=True;remaining=set(graph)
        while remaining:
            visited=set();todo=[min(remaining)]
            while todo:
                n=todo.pop()
                if n in visited:continue
                visited.add(n);todo.extend(x for x,allowed in graph[n] if not allowed and x not in visited)
            remaining-=visited
            if len({byid[n].context for n in visited if byid[n].exposure=='PUBLIC'})>1:correlation=False;break
```
