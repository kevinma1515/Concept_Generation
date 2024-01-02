import openai
from config import API
from pathlib import Path
import csv
from tqdm import tqdm
import pandas as pd

design_tasks = {"a lightweight exercise device that can be used while traveling": 'exercise',
                # "an innovative product to froth milk": 'froth',
                "a device that disperses a light coating of a powedered substance over a surface": 'powder',
                "a new way to measure the passage of time": 'time',
                "a device to fold washcloths, hand towels, and small hand towels": 'towels'}

system_prompt = """
You are an expert design engineer.
"""

prompt_initial = """
Generate 50 design solutions for {design_task}.
"""

prompt = """
Given the following prompt and design solution, please expand the design solution to add more detail to it. Explain the reasoning and assumptions behind your solution. Answer by just continuing to expand on the solution provided, without any intro text. Be brief and answer in around 15 words.

Prompt: generate a solution for {design_task}.
Solution: {solution}"""


if __name__ == '__main__':
    openai.api_key = API
    verbose = True
    # verbose = False

    for design_task, name in design_tasks.items():

        # prompt for 50 design solutions
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_initial.replace('{design_task}', design_task)},
            ],
        )
        answer = response['choices'][0]['message']['content']
        if verbose:
            print(prompt_initial)
            print(answer + "\n")

        design_solutions = answer.split('\n')


        answers = []
        for solution in tqdm(design_solutions[:50]):
            solution = solution.split(". ")[1]

            user_prompt = prompt.replace('{solution}', solution).replace('{design_task}', design_task)

            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    ],
            )
            answer = response['choices'][0]['message']['content']
            if answer[:9] == "Solution:":
                answer = answer[10:]
            if verbose:
                print(user_prompt)
                print(answer + "\n")
            answers.append(solution + ' ' + answer)

        answers = [x.replace('\n', '\\n') for x in answers]

        df = pd.DataFrame(answers)
        df.to_csv(f'data/critique_{name}.csv', index=False, header=False)

    print("done")
