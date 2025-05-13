import graphviz

def generate_no_deterministict_automata_graphic(title, data_frame):
    dot = graphviz.Digraph(comment=title)

    for row in data_frame.itertuples(index=True):

        if row.RESULT == 1.0:
            dot.node(row.STATES, row.STATES, style='filled', fillcolor='gray')
        else:
            dot.node(row.STATES, row.STATES)

        zero_input_states = row[2].replace(",","")

        for state in list(zero_input_states):
            dot.edge(row.STATES, state, label='0')

        one_input_states = row[3].replace(",", "")

        for state in list(one_input_states):
            dot.edge(row.STATES, state, label='1')


    dot.render(directory='renders'.replace('\\','/'), filename=title)
def generate_deterministict_automata_graphic(title, data_frame):
    dot = graphviz.Digraph(comment=title)

    for row in data_frame.itertuples(index=True):

        if row.RESULT == 1.0:
            dot.node(row.STATES, row.STATES, style='filled', fillcolor='gray')
        else:
            dot.node(row.STATES, row.STATES)

        dot.edge(row.STATES, row[2], label='0')
        dot.edge(row.STATES, row[3], label='1')

    dot.render(directory='renders'.replace('\\','/'), filename=title)

