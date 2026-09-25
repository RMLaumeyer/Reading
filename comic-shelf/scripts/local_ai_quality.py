"""Pure source/quality helpers for the local benchmark; no network or model calls."""
import copy
import re
import unicodedata


def surface(text):
    text=unicodedata.normalize('NFKC',text).translate(str.maketrans({'’':"'",'‘':"'",'–':'-','—':'-'}))
    return ' '.join(text.split())


def normalize_characters(claims):
    """Merge spelling/format variants only, never first names or secret identities."""
    merged={};changes=[]
    for original in claims:
        c=copy.deepcopy(original)
        name=re.sub(r'^the\s+','',surface(c['value']),flags=re.I)
        key=name.casefold()
        if not key: continue
        if key not in merged:
            c['value']=name;merged[key]=c
        else:
            for e in c['evidence']:
                if e not in merged[key]['evidence'] and len(merged[key]['evidence'])<2:
                    merged[key]['evidence'].append(e)
        if name!=original['value'] or merged[key] is not c:
            changes.append(dict(original=original['value'],normalized=merged[key]['value']))
    return list(merged.values()),changes


def possible_short_names(claims):
    names=[c['value'] for c in claims]
    result=[]
    for name in names:
        if ' ' in surface(name): continue
        matches=[other for other in names
                 if surface(other).casefold().startswith(surface(name).casefold()+' ')
                 and not re.search(r'&|\b(?:and|of|the)\b',other,re.I)]
        if matches: result.append(dict(short=name,possibleFullNames=matches))
    return result


def plot_score(text):
    """Transparent relevance heuristic, not a fact checker or confidence score."""
    score=0
    for pattern in [r'\b(?:threat\w*|danger\w*|enemies|enemy|villain\w*)\b',
                    r'\b(?:kill\w*|destroy\w*|save|rescue\w*|attack\w*|battle\w*|fight\w*|corruption)\b',
                    r'\b(?:secret\w*|myster\w*|mission|assignment|identity|decision|ritual|trial)\b']:
        score+=3*bool(re.search(pattern,text,re.I))
    if re.search(r"\bisn.t (?:their|his|her) only problem\b",text,re.I): score-=3
    if score<=0 and re.search(r'\b(?:not alone|is back)\b',text,re.I): score-=3
    if re.search(r'\b(?:proud tradition|storytelling|sensational era|record books|you won.t want to miss)\b',text,re.I): score-=4
    return score


def contents_ranges(text):
    """Exact explicitly named whole ranges; partial/unspecified-year entries abstain."""
    synopsis=text.partition('Bibliographic information:')[0]
    marker=re.search(r'\bcollect(?:s|ing)\s*:?\s+',synopsis,re.I)
    if not marker: return []
    clause=re.split(r'(?<=[.!?])\s+(?=[A-Z])',synopsis[marker.end():],maxsplit=1)[0]
    # Material-from applies to the remainder of a collecting clause.
    clause=re.split(r'\bmaterial\s+from\b',clause,maxsplit=1,flags=re.I)[0]
    pattern=(r'(?:^|[,;]\s*|\band\s+)(?P<series>[^#;,\n]{1,160}?)\s+'
             r'\((?P<year>\d{4})\)\s*#?(?P<first>\d+(?:\.[A-Za-z0-9]+)?(?:[A-Za-z])?)'
             r'(?:[-–](?P<last>\d+))?(?![\w-])')
    matches=list(re.finditer(pattern,clause,re.I));result=[]
    for i,m in enumerate(matches):
        tail=clause[m.end():matches[i+1].start() if i+1<len(matches) else len(clause)]
        # Qualifiers apply to the current entry, not the next comma-delimited entry.
        qualifier=re.split(r'[,;]|\band\b',tail,maxsplit=1,flags=re.I)[0]
        if re.search(r'\b(?:story|stories|material|excerpt|partial)\b',qualifier,re.I): continue
        series=m['series'].strip()
        if re.search(r'\bmaterial\b',series,re.I): continue
        first,last=m['first'],m['last']
        if last and (not first.isdigit() or not 0<=int(last)-int(first)<=150): continue
        quote=clause[m.start('series'):m.end()]
        result.append(dict(value=f'{series} ({m["year"]}) #{first}'+('-'+last if last else ''),quote=quote))
    return result


def quality_report(result, packet, responses, status):
    fields={};conflict=packet.get('constraints',{}).get('contentsConflict',False)
    for key in ['summary','stories','characters','issues','pages','review','readingOrder']:
        if key not in result:
            fields[key]=dict(state='not_completed',reason='Stage did not complete; see saved error.');continue
        value=result[key] if isinstance(result[key],list) else result[key]['value']
        if value is not None and value!=[]:
            fields[key]=dict(state='draft',reason='Source-backed draft; semantic review still required.');continue
        if conflict and key in ['issues','pages','review']:
            reason='Conflicting catalog/source contents.'
        elif key=='review': reason='No unambiguous matching review was established from the supplied sources.'
        elif key=='readingOrder': reason='No supported reading-order guidance was established from the supplied sources.'
        elif key=='issues': reason='No unambiguous whole-issue range parsed; missing year/format or partial material may require review.'
        elif key=='pages': reason='No unique page count with an exact bibliographic ISBN match.'
        else: reason='No usable source-supported value was selected; inspect source coverage and extraction.'
        fields[key]=dict(state='withheld',reason=reason)
    return dict(readyForPublication=False,status=status,fields=fields,
        characterScope='Explicit source mentions, including backstory/comparisons; not verified on-page appearances.',
        auditWarnings=[log['warning'] for log in responses if log.get('warning')],
        possibleAliases=possible_short_names(result.get('characters',[])),
        suggestedNames=[c['value'] for log in responses for c in log.get('suggestedCharacters',[])],
        withheldNames=[c['claim']['value'] for log in responses for c in log.get('withheldCharacters',[])])
