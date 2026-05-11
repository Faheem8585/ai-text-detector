import re


AI_PHRASES = [
    r"\bin conclusion\b",
    r"\bit is important to note\b",
    r"\bit'?s worth noting\b",
    r"\bdelve(?:s|d)?\s+(?:into|deeper)\b",
    r"\bnavigating the\b",
    r"\bmultifaceted\b",
    r"\bin today'?s (?:digital|fast[- ]paced|modern|interconnected|complex) world\b",
    r"\bunderscores? the (?:importance|need|significance)\b",
    r"\bplays? a (?:crucial|pivotal|vital|significant|key) role\b",
    r"\bharness(?:ing|es)? the power of\b",
    r"\bin the realm of\b",
    r"\brich tapestry\b",
    r"\bever[- ]evolving\b",
    r"\bever[- ]changing\b",
    r"\bnuanced understanding\b",
    r"\bat the forefront of\b",
    r"\bpaving the way\b",
    r"\ba testament to\b",
    r"\bnot only .{1,40} but also\b",
    r"\bin the ever[- ]changing landscape\b",
    r"\bunlock(?:ing)? the (?:potential|secrets|power)\b",
    r"\bcornerstone of\b",
    r"\bfoster(?:ing|s)? (?:a|an) .{0,30} environment\b",
    r"\bembark(?:ing|s)? on a journey\b",
    r"\bas an ai language model\b",
    r"\bi (?:do not|don'?t) have personal\b",
    r"\bcrucial to (?:consider|understand|recognize|note)\b",
    r"\bin summary\b",
    r"\bto sum (?:up|it up)\b",
    r"\boverall,?\b",
    r"\bgame[- ]chang(?:er|ing)\b",
    r"\bcutting[- ]edge\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bseamless(?:ly)? (?:integrat|connect|combin)",
    r"\b(?:revolutioniz|transform)(?:e|es|ing|ed) the way\b",
    r"\bdive (?:deep(?:er)?|into)\b",
    r"\b(?:meticulous|comprehensive|robust) (?:analysis|understanding|approach)\b",
    r"\bleverag(?:e|ing|es) (?:the|cutting|advanced)\b",
    r"\boptimiz(?:e|ing|es) (?:performance|efficiency|outcomes)\b",
    r"\bsynerg(?:y|ies|istic)\b",
    r"\bholistic (?:approach|view|understanding|perspective)\b",
    r"\b(?:moreover|furthermore|additionally),\s",
    r"\bbe that as it may\b",
    r"\bwithout further ado\b",
    r"\bit goes without saying\b",
    r"\bat the end of the day\b",
    r"\bwhen all is said and done\b",
    r"\bthe importance of .{0,40} cannot be overstated\b",
    r"\bcaters to (?:a|the) (?:wide|diverse|broad) (?:range|array|variety)\b",
    r"\bbridg(?:e|ing|es) the gap\b",
    r"\btap into\b",
    r"\bwealth of (?:information|knowledge|experience)\b",
    r"\bworld of possibilities\b",
    r"\bjourney of (?:discovery|exploration|self[- ]discovery)\b",
    r"\bstrike(?:s)? a balance\b",
    r"\bthink outside the box\b",
    r"\bvibrant (?:community|culture|ecosystem)\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in AI_PHRASES]


def signature_frequency(text):
    matches = []
    for rx in _COMPILED:
        for m in rx.finditer(text):
            matches.append(m.group(0))
    words = max(len(text.split()), 1)
    density = len(matches) / (words / 100.0)
    score = max(0.0, min(1.0, density / 1.5))
    return round(score, 4), matches[:30]
