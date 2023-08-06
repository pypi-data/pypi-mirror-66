
from emora_stdm import DialogueFlow


component = DialogueFlow('goal')
component.add_system_transition('goal', 'start', '#GOAL(component) #GATE()')
component.add_system_transition('exit', 'SYSTEM:root', '')
component.knowledge_base().load_json_file('common.json')
component.knowledge_base().load_json_file('component.json')

system = {
    'state': 'start'
}

user = {
    'state': 'user'
}

component.load_transitions(system)
component.load_global_nlu(user)

if __name__ == '__main__':
    component.run(debugging=True)