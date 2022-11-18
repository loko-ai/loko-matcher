def longest_match(matches):
    return max(matches,key=lambda m:len(m))

def shortest_match(matches):
    return max(matches,key=lambda m:-len(m))

def best_match(matches):
    return max(matches,key=lambda m:m.score)

def match_picker(matches,f):
    return max(matches,key=f)