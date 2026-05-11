import math
import re
import zlib

_COMMON = (
    "the of and to a in is it you that he was for on are with as i his they "
    "be at one have this from or had by hot but some what there we can out "
    "other were all your when up use word how said an each she which do their "
    "time if will way about many then them would write like so these her long "
    "make thing see him two has look more day could go come did my no most "
    "over only its new also after our work first well way even any new want "
    "because these give us through just into him know take people year your "
    "some good think where most much should very well still own through being "
    "made before great such here back must where right too any same big does "
    "tell why ask men read need land different home us move try kind hand "
    "picture again change off play spell air away animal house point page "
    "letter mother answer found study learn america world high every near add "
    "food between own below country plant last school father keep tree never "
    "start city earth eye light thought head under story saw left don't few "
    "while along might close something seem next hard open example begin life "
    "always those both paper together got group often run important until "
    "children side feet car mile night walk white sea began grow took river "
    "four carry state once book hear stop without second later miss idea "
    "enough eat face watch far indian real almost let above girl sometimes "
    "mountain cut young talk soon list song being leave family body music "
    "color stand sun question fish area mark dog horse birds problem complete "
    "room knew since ever piece told usually didn't friends easy heard order "
    "red door sure become top ship across today during short better best "
    "however low hours black products happened whole measure remember early "
    "waves reached"
).split()
_RANK = {w: i for i, w in enumerate(_COMMON)}


def _word_surprisal(token):
    rank = _RANK.get(token.lower())
    if rank is None:
        return math.log2(50_000)
    return math.log2(rank + 2)


def _compression_ratio(text):
    raw = text.encode("utf-8")
    if len(raw) < 32:
        return 0.5
    return 1.0 - (len(zlib.compress(raw, level=6)) / len(raw))


def _type_token_ratio(tokens):
    if not tokens:
        return 1.0
    return len(set(tokens)) / len(tokens)


def sentence_predictability(sentence):
    tokens = re.findall(r"[A-Za-z']+", sentence)
    if not tokens:
        return 50.0
    avg = sum(_word_surprisal(t) for t in tokens) / len(tokens)
    return round(2 ** avg, 2)


def predictability_score(sentences):
    proxies = [sentence_predictability(s) for s in sentences if s.strip()]
    if not proxies:
        return 0.0, []

    full_text = " ".join(sentences)
    all_tokens = re.findall(r"[A-Za-z']+", full_text.lower())
    if not all_tokens:
        return 0.0, proxies

    common_hits = sum(1 for t in all_tokens if t in _RANK)
    common_ratio = common_hits / len(all_tokens)
    common_signal = max(0.0, min(1.0, (common_ratio - 0.30) / 0.35))

    comp_signal = max(0.0, min(1.0, (_compression_ratio(full_text) - 0.45) / 0.30))
    ttr = _type_token_ratio(all_tokens)
    ttr_signal = max(0.0, min(1.0, (0.65 - ttr) / 0.30))

    score = 0.55 * common_signal + 0.25 * comp_signal + 0.20 * ttr_signal
    return round(score, 4), proxies
