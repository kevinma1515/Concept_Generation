import os
import openai
import pandas as pd
import json
import itertools
import numpy as np
os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = os.getenv("OPENAI_API_KEY")


# not necessary
# cleaned_lst = [sentence[3:] for sentence in stripped_lst]

def generate_initial_solns(temp, top_p, message):
    completion = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages = message,
        temperature = temp,
        top_p = top_p)
    text = completion['choices'][0]['message']['content']

    return text

def generate_subseq_solns(temp, top_p, message):
    completion = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages = message,
        temperature = temp,
        top_p = top_p)

    text = completion['choices'][0]['message']['content']

    return text

def split_text(text):
    lst = text.split('\n\n')
    lst = [sentence.strip() for sentence in lst]
    return lst



# (temp, top p)
prompt = "a lightweight exercise device that can be used while traveling"
initial_content = 'You are a design expert who is excellent at ideating far-fetched design ideas. Generate 5 design solutions for ' + prompt
subseq_content = 'You are a design expert who is excellent at ideating far-fetched design ideas. Generate 5 more design solutions for ' + prompt
messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

temp_topP = [(1, 1)]
lst = []
df = pd.DataFrame({'TopP=0|Temperature=0' : [],
                   'TopP=0.5|Temperature=0' : [],
                   'TopP=1|Temperature=0' : [],
                   'TopP=0|Temperature=1' : [],
                   'TopP=0.5|Temperature=1' : [],
                   'TopP=1|Temperature=1' : [],
                   'TopP=0|Temperature=2' : [],
                   'TopP=0.5|Temperature=2' : []})

col_names = ['TopP=0|Temperature=0',
                   'TopP=0.5|Temperature=0',
                   'TopP=1|Temperature=0',
                   'TopP=0|Temperature=1',
                   'TopP=0.5|Temperature=1',
                   'TopP=1|Temperature=1',
                   'TopP=0|Temperature=2',
                   'TopP=0.5|Temperature=2']
count = 0

# only run this one at a time. Otherwise, it will crash.
for parameter in temp_topP:
    messages.append({'role' : 'user', 'content' : initial_content})
    txt = generate_initial_solns(temp = parameter[0], top_p = parameter[1], message = messages)
    print(messages)
    split_text = txt.split('\n\n')
    split_text = [sentence.strip() for sentence in split_text]
    lst.extend(split_text)
    for i in range(9):
        messages.append({'role' : 'assistant', 'content' : txt})
        messages.append( {'role' : 'user', 'content' : subseq_content})
        txt = generate_initial_solns(temp = parameter[0], top_p = parameter[1], message = messages)
        split_text = txt.split('\n\n')
        split_text = [sentence.strip() for sentence in split_text]
        lst.extend(split_text)
        print(messages)

    print(messages)
df = pd.DataFrame(lst)
df.to_csv('farfetched_exercise.csv')