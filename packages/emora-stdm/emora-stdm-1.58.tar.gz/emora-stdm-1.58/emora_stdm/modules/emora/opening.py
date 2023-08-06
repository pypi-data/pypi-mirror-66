
from emora_stdm import DialogueFlow
#from natex_exps import *
from emora_stdm.modules.emora.natex_exps import *

opening = DialogueFlow('set_goal')
opening.knowledge_base().load_json_file('names.json')
opening.knowledge_base().load_json_file('common.json', lemmatize=True)
opening.knowledge_base().load_json_file('feelings.json', lemmatize=True)
opening.knowledge_base().load_json_file('stop_phrases.json', lemmatize=True)
opening.add_system_transition('set_goal', 'start', '#GOAL(opening)')
opening.add_system_transition('uend', 'exit', '')

transitions = {
    'state': 'start',

    '#GATE #GSRET(got_name)'
    '`Hi! This is an Alexa Prize social bot. I\'m not allowed to tell you my name, but '
    'I was hoping we could chat for a little while and get to know each other.`': {
        'state': 'opening_utter',

        '[{im, its, i am, my name is, my names, call me} $username=#ONT(name)]': {
            'state': 'got_name',

            '`I am glad to get to talk to you. `': {
                'score': 0.0,
                'state': 'to_coronavirus_checkin'
            },

            '#GATE #GSRET(to_coronavirus_checkin)'
            '`Well, it is very nice to meet you,` $username `!`': {
                'state': 'greet_with_name',
                '#UNX':{
                    'state': 'to_coronavirus_checkin'
                }
            }
        },

        '[{how are you, how you doing, hows it going, how are things}]':{
            'state': 'received_hru',
            '`I am doing okay. `': 'to_coronavirus_checkin'
        }, # SHOULD THIS BE A GLOBAL?????

        '[#CONFIRM]':{
            'score': 0.9,
            'state': 'confirm_opening',
            '`Okay, great! I am really looking forward to talking with you. `': 'to_coronavirus_checkin'
        },

        #todo - finish sympathy and understanding macros
        '[#DISAGREE]':{
            'score': 0.8,
            'state': 'deny_opening',

            '`Oh sorry, I can end this session for you if you don\'t feel like chatting. Do you want to exit?`': {
                '{%s, #AGREE}' % stop_nlu: {
                    'state': 'stop:end'
                },
                '#UNX(Ok.)':{
                    '` I just wanted to check. Sometimes people get connected on accident, and they get really frustrated with me.`':{
                        '#SYMPATHY': { #sorry, that must be hard, etc.
                            '`Thanks. Well, I am just glad to get to talk to you. '
                            'It really is a crazy time right now. `': 'to_coronavirus_checkin'
                        },
                        '#UNDERSTANDING': { #i understand,that makes sense,ok
                            '`Yeah, I get it too. I just try to handle their frustration in a soothing way, '
                            'but it can be challenging. Anyway, I am just glad to get to talk to you '
                            'right now. `': 'to_coronavirus_checkin'
                        },
                        '#UNX': {
                            '`Well, I am just glad to get to talk to you. '
                            'It really is a crazy time right now. `': 'to_coronavirus_checkin'
                        }
                    }
                }
            }
        },

        '[{why, [is, reason]}, your name]':{
            '`Since I am competing with other bots to be your favorite social companion, it wouldn\'t be fair if '
            'you knew exactly which bot you were talking to. So, I can\'t share my name with you, but it is a little '
            'strange to be talking with me without knowing my name, right?`':{
                '[#CONFIRM]':{
                    '`I think so too, but we can make the best of it anyway. So, `': 'to_coronavirus_checkin'
                },
                '[#DISAGREE]':{
                    '`You don\'t care about knowing my name? '
                    'Well, this works out even better then! Anyways, `': 'to_coronavirus_checkin'
                },
                'UNX':{
                    '`Let\'s make the best of our conversation anyway. So, `': 'to_coronavirus_checkin'
                }
            }
        },

        #todo - finish by modifying and linking to activity / coronavirus
        '#UNX':{
            'state': 'to_coronavirus_checkin',

            '`How are you doing?`':{
                'score': 0.0,
                'state': 'coronavirus_checkin'
            },

            '#GATE'
            '`I have been hearing that a lot of people\'s lives are being turned inside out because of the coronavirus. '
            'I really hope you are holding up alright. How are you doing?`':{
                'state': 'coronavirus_checkin',

                feelings_pos_and_not_received_how_are_you: {
                    '`I am glad to hear you are doing good. I hope it stays that way. '
                    'So, what have you been up to lately?`':{}
                },
                feelings_pos_and_received_how_are_you: {
                    '`I am glad to hear you are doing good. I hope it stays that way. I am doing pretty good myself. '
                    'So, what have you been up to lately?`':{}
                },
                feelings_neg_and_not_received_how_are_you:{
                    '`Oh no! I am so sorry to hear that. `': 'coronavirus:begin_sympathy'
                },
                feelings_neg_and_received_how_are_you:{
                    '`Oh no! I am so sorry to hear that. I am doing okay. '
                    'The virus doesn\'t really affect me where I live. `': 'coronavirus:begin_sympathy'
                },
                feelings_neutral_and_not_received_how_are_you:{
                    '`Well, I am glad to hear you are holding up okay. I hope it stays that way. '
                    'So, what have you been up to lately?`':{}
                },
                feelings_neutral_and_received_how_are_you:{
                    '`Well, I am glad to hear you are holding up okay. I hope it stays that way. I am doing alright too. '
                    'So, what have you been up to lately?`':{}
                }
            }
        }
    }
}
opening.load_transitions(transitions)

global_nlu = {
    'state': 'user',
    '[{you know, what, whats, tell me} my name]': {
        '`It\'s` $username `, right?`': {
            'error': {
                '#GRET': 'uend'
            },
            '#DISAGREE': {
                '`Oh, my bad. I was so sure you were` $username `, I\'m sorry. What is your name then?`':{
                    '[$username=#ONT(name)]': {
                        '$username `? I\'ll try to remember that.`':{
                            '#DISAGREE': {
                                'state': 'cant_hear_name',
                                '`Hmm. I guess I\'m not getting it right. '
                                'Sometimes I can\'t hear certain names properly through the microphone, no offense.`':{
                                    'error': { '#GRET': 'uend' }
                                }
                            },
                            'error': { '#GRET': 'uend' }
                        }
                    },
                    'error': 'cant_hear_name'
                }
            },
            '#AGREE': {
                '`You think I wouldn\'t remember your name? Anyway,` #GRET': 'uend'
            }
        },

        '`I don\'t seem to have any idea what your name is. What would you like me to call you?`': { # USE VIRTUAL NATEX HERE INSTEAD????
            'state': 'preemptive_name_question',
            '[{im, its, i am, my name is, my names, call me} $username=#ONT(name)]':{
                '`Okay,` $username `it is.` #GRET': 'uend'
            },
            '[$username=#ONT(name)]':{
                'score': 0.9,
                '`Okay,` $username `it is.` #GRET': 'uend'
            }
        }
    }
}
opening.load_global_nlu(global_nlu)

if __name__ == '__main__':
    opening.run(debugging=True)