from loko_extensions.model.components import Arg, Component, save_extensions, Input, Output

from extensions.component_doc import matcher_doc

rule = Arg(name="rules", type="code", label="Rules", required=True)
include_tokens = Arg(name="include_tokens", type="boolean", label="Include Tokens Information", value=True)
# include_matches_location = Arg(name="include_matches_location", type="boolean", label="Include Matches Location", value=True)


args = [include_tokens, rule]#include_matches_location

input_matcher = [Input(label="extract matches", id="extract_matches", to="extract_matches", service="extract_matches")]
output_matcher = [Output(label="extract matches", id="extract_matches")]

matcher = Component(name="Matcher", description=matcher_doc, inputs=input_matcher, outputs=output_matcher, args=args, icon="RiHeartsLine")


if __name__ == '__main__':
    save_extensions([matcher])

    # RiFocus2Fill