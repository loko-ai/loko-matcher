import os

import gradio as gr
from ds4biz_matcher.business import parser
from ds4biz_matcher.business.matchers import RegexMatcher, Skipper, OrMatcher, FuzzyMatcher, PhraseMatcher
from ds4biz_matcher.business.tokenizers import SimpleTokenizer, MatchPreservingTokenizer
from loguru import logger

numbers = Skipper(RegexMatcher("\d+"), RegexMatcher("\d+"), 10, skipcond=RegexMatcher("[\d+\-\._/]"))

points = PhraseMatcher(OrMatcher(FuzzyMatcher("num"), "n"), ".")

st = MatchPreservingTokenizer(SimpleTokenizer(sep="\\s+", puncts=".,;:!?\"'()"), PhraseMatcher("sig", ".", "ra"),
                              numbers, points)



def get_results(text, rule):
    tokens = st.tokenize(text)
    m = parser.get_matcher(rule)
    indices = set()
    ret = []
    for m in parser.get_matcher(rule).all(tokens):
        ret.append(m)
        indices.update(list(range(m.start, m.end)))

    ii = []
    for i, el in enumerate(tokens):
        if i in indices:
            ii.append((el, "+"))
        else:
            ii.append((el, None))

    return ii



examples = [["Hello everyone", '"Hello"'], ["Hello everyone", 'lower("hello")']]


# demo = gr.Interface(get_results, [gr.Textbox(lines=10), "text"], gr.HighlightedText(),
#                    examples=examples)


def read_file(file):
    logger.debug(f"READING FILE")
    try:
        if not file:
            logger.debug("siamo quiiiii")
            return ""
        with open(file.name, encoding="utf-8") as f:
            content = f.read()
            return content

    except Exception as inst:
        logger.error(f"error while reading a file. File name: {file.name}, error: {inst} ")
        raise Exception("File extension not supported. Try with a txt or json file")


with gr.Blocks() as DEMO:
    with gr.Row():
        with gr.Column():
            text_input = gr.Text(lines=10, label="Text")
            rule_input = gr.Text(lines=10, label="Rule")

            with gr.Row():
                submit = gr.Button("Analyze")
                clear = gr.Button("Clear")

        results = gr.HighlightedText(label="Results")
    with gr.Row():
        file_input = gr.File(file_types=[".txt"], label="Upload")

        with gr.Accordion(label="examples", open=False):
            examples = gr.Examples(examples=examples,
                                   inputs=[text_input, rule_input])
    file_input.change(read_file, file_input, text_input)
    submit.click(get_results, inputs=[text_input, rule_input], outputs=results)
    clear.click(lambda: ("", "", "", None), outputs=[text_input, rule_input, results, file_input])


