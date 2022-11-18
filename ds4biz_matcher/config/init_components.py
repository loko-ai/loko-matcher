from loko_extensions.model.components import Component, save_extensions, Input, Arg

component = Component("Matcher", inputs=[Input(id="text", service="loko_extract")], icon="RiHeartsLine",
                      args=[Arg(name="rule", type="code", value="regex('.*')"),
                            Arg(name="include_tokens", type="boolean", value=False)])

save_extensions([component])
