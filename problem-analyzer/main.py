import json, docx, re, copy, os

# 所有实现遵循以可读性换性能的原则，不作过度优化

with open("LawData.json", "r", encoding="utf-8") as file:
    problems = json.loads(file.read())

sample = problems[3]


def splitAnswers(problem):
    problem["daan"] = problem["daan"].split(",")
    return problem


def splitChoices(problem):
    problem["xuanxiang"] = problem["xuanxiang"].split('\n')
    problem["xuanxiang"] = [choice.rstrip() for choice in problem["xuanxiang"]]
    return problem


def extractArticles(problem):
    article_pattern.match(problem['jiexi'])


problems = list(map(lambda problem: splitAnswers(problem), problems))
problems = list(map(lambda problem: splitChoices(problem), problems))
print(problems)

article_pattern = re.compile(r"《(.+)》第(.+)条")