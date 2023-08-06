stop_nlu = [
    "$off_phrase=[!#ONT(ontturn), #ONT(ontoff)]",
    "$off_phrase=[!#ONT(ontturn), to, #ONT(ontoff)]",
    "$off_phrase=[!{alexa,echo,computer}?, #ONT(ontoff)]",
    "[$off_phrase=[!{alexa,echo,computer}, #ONT(ontturn), {#ONT(ontoffpaired),#ONT(ontoff)}]]",
    "[$off_phrase=[!{alexa,echo,computer}, #ONT(ontturn), to, {#ONT(ontoffpaired),#ONT(ontoff)}]]",
    "[$off_phrase={goodnight, good night,shut up}]",
    "$off_phrase=[!{alexa,echo,computer}?, {cancel,abandon}]",
    "[$off_phrase=[!{done,finished,over} {talking,chatting} {now,with you}]]",
    "[$off_phrase=[!{wanna,want to} {finish,end,stop} {this conversation}]]",
    "[$off_phrase=[!{wanna,want to} {be} {done,finished}]]",
]

receive_how_are_you = "{" \
                      "[how are you]," \
                      "[how you doing]," \
                      "[what about you]," \
                      "[whats up with you]," \
                      "[how you are]," \
                      "[how about you]" \
                      "}"

feelings_pos_and_not_received_how_are_you = "{" \
                                            "[!#ONT_NEG(negation), -%s, [#ONT(pos_feel)]]," \
                                            "[! -%s, [#ONT(negation)], [#ONT(neg_feel)]]" \
                                            "}" % (receive_how_are_you, receive_how_are_you)

feelings_neg_and_not_received_how_are_you = "{" \
                                            "[!#ONT_NEG(negation), -%s, [#ONT(neg_feel)]]," \
                                            "[! -%s, [#ONT(negation)], [{#ONT(pos_feel),#ONT(neut_feel)}]]" \
                                            "}" % (receive_how_are_you, receive_how_are_you)

feelings_neutral_and_not_received_how_are_you = "[!#ONT_NEG(negation), -%s, [#ONT(neut_feel)]]" % (
    receive_how_are_you)
feelings_pos_and_received_how_are_you = "{" \
                                        "[!#ONT_NEG(negation), [#ONT(pos_feel)], [%s]]," \
                                        "[#ONT(negation), #ONT(neg_feel), %s]" \
                                        "}" % (receive_how_are_you, receive_how_are_you)

feelings_neg_and_received_how_are_you = "{" \
                                        "[!#ONT_NEG(negation), [#ONT(neg_feel)], [%s]]," \
                                        "[#ONT(negation), {#ONT(pos_feel),#ONT(neut_feel)}, %s]" \
                                        "}" % (receive_how_are_you, receive_how_are_you)

feelings_neutral_and_received_how_are_you = "[!#ONT_NEG(negation), [#ONT(neut_feel)], [%s]]" % (
    receive_how_are_you)