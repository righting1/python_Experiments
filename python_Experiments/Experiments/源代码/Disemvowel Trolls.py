def disemvowel(string_):
    return "".join([x if x.lower() not in "aeiou" else "" for x in string_ ])
