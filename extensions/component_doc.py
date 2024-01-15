matcher_doc =  '''### Description
MATCHER is a component used to extract entities from documents using rules. Inside there is a set of specific objects for a certain type of research.

It is possible to individually recall these objects for match bases and from the composition of them it is possible to realize more complex and articulated rules. Matcher objects work a list of tokens obtained from the text by means of a tokenizer and are validated by means of specific checkers. Alternatively, you can directly pass a tokenized text, if you want to customize the sentences tokenization.


### Configuration

Available services allow you to select the MATCHER instance to use. 
rule is the field in which to insert the rules to be applied to the received text in input. The matcher are divided into:

##### INDIVIDUAL TOKENS
- simple(value): it is used to match a specific token 

- regex(regex,flags=re.IGNORECASE,junk="",terminate="$"): it allows to match tokens using a regex. 

- fuzzy(ent,t=.8): the token is matched by analogy, and “t” parameter indicates the minimum threshold. 

- syn(options): it allows to match any of the tokens inserted into it.

- all(): gives back individually all the tokens present in the document.

- condition(cond): within it requires a condition and is used in combination with other matchers.

##### **MULTI TOKEN**
- span(matcher,m,n,separator="",strategy="longest"): set a minimum value (m) and a maximum value (n), it can match plus tokens that meet the conditions imposed in the matcher (join tokens to try to match the rule, between one token and the other you can set a separator).

- phrase(matchers): more matchers can be inserted inside. The tokens must sequentially respect all the matchers inserted inside the object; it returns the tokens that have respected the conditions. 

- perm(matchers): similar to Phasematcher but the conditions do not have to be respected in order, the matchers are exchanged.

- rep(matcher,minlen=1,maxlen=100): repeats the match inserted inside the object until the tokens all respect the condition set sequentially. It stops when the condition is no longer respected: the minimum and maximum of times can be indicated in the creation of the object.

- skip(start_matcher,end_matcher,max_skip=5,skipcond=MatchAll()): returns the tokens that within a range (max_skip) can match initial (start_matcher) and final (end_matcher) condition. You can set, for tokens between initial and final match, a condition that they must comply (skip_cond). 

- expand(matcher,left=10,right=10): starting from the matchate token, based on the range set within the object, it also matches a certain number of tokens left (left) and a certain number of tokens right (right). 

- context(*matchers,max_dist=100): returns all tokens in a context bounded by matchers within the object, if the distance does not exceed that of max_dist.

##### **CHOICE OF DIFFERENT CONDITIONS** 

- oneof(*matchers): more matchers can be inserted inside. It matches all tokens that respect at least one of the matcher within it (if a token matches in more matcher, returns it several times).
 
- backoff(*matchers): given a series of matchers, it returns what that matches first, leaving out all the others. 

- chain(matcher1,matcher2): it applies the second matcher to the tokens extracted from the first. It is used in combination with expand, skip, and context.

##### NORMALIZATION OF TOKENS
- norm(matcher,fun): it normalizes the tokens (via a function) that are passed into the matcher present within it. Only for control, does not transform them.

- lower(matcher): it allows passing all the tokens to the matcher inserted inside the object in lowercase. Only for the control, does not transform them.

##### **FILTER FUNCTIONS**
- filter(matcher,cond): it applies a filter to the candidates (matched tokens) after applying the matcher, it returns the candidates who meet the (boolean) condition set in the filter. The filter is a function that takes in input m and n, where n is the document length.

expandfilter(matcher,cond,left=10,right=10): it allows to apply a filter, starting from an initial matcher, also to the tokens external to it (the number depends on the parameters "left" and "right"). Useful if you want to filter candidates that respect the created rules.

##### **POST-PROCESSING**
- exclude(matcher): the tokens that match the condition within the object, will not then be displayed within the candidates. 

- post(matcher,f): it applies the function (f) to tokens extracted from the matcher with the aim of cleaning them up. The difference with the norm is that in this case the tokens are modified only for display. 

- token(fun=None): it is used to create new functions.

### Input
The component accepts as input a string that represents the text to be analyzed. 

### Output
The output structure consists of two keys: tokens and matches. Tokens returns the tokenization of the received text in input and a boolean indicates whether the token is part of matches. Matcher is represented with a list.
Each match contains the position of the first token that makes up the match (start), the position of the last (end), the score reached, the submatches and the list of tokens that make up the match. Taking as an example a simple input: "Hello 1010 world" and supposing to extract consecutive numbers within this sentence, the output will be:
```json
{"tokens": [["Hello", False], ["1010", True], ["world", False]], 
"matches":[{"start": 1, "end": 2, "score": 1, "submatches": None, 
"tokens": ["1010"]}]}
```
We then got a single match consisting of a single token, "1010", with score 1.'''