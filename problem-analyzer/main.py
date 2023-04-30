import json, docx, re, copy, os
from functools import reduce
import operator

# 所有实现遵循以可读性换性能的原则，不作过度优化

explanation_pattern = re.compile("([ABCD]{1,4})项：(.+)")
article_pattern = re.compile(r"《(.+?)》第(.+?)条")

laws = [file.rstrip(".txt") for file in os.listdir("assets/laws")]


class InvalidLawError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def expandAbbreviationOfLaw(abbreviation):
    global laws
    for law in laws:
        if law.endswith(abbreviation):
            return law

    raise InvalidLawError("没这部法，给它扬了")


def splitAnswers(problem):
    problem["daan"] = problem["daan"].split(",")
    return problem


def splitChoices(problem):
    problem["xuanxiang"] = problem["xuanxiang"].split('\n')
    problem["xuanxiang"] = [choice.rstrip() for choice in problem["xuanxiang"]]

    return problem


def pairChoiceWithExplanation(line):
    global explanation_pattern
    match = explanation_pattern.match(line)

    if match:
        choices = match.group(1)
        explanation = match.group(2)
        choice_explanation_pairs = list(map(lambda choice: (choice, explanation), choices))
        return choice_explanation_pairs
    else:
        return None


def pairChoiceWithArticles(choice_explanation_pair):
    global article_pattern

    articles = article_pattern.findall(choice_explanation_pair[1])
    if articles:
        articles = list(map(lambda article: (expandAbbreviationOfLaw(article[0]), article[1]), articles))
        choice_articles_pair = (choice_explanation_pair[0], articles)
    else:
        choice_articles_pair = (choice_explanation_pair[0], [])

    return choice_articles_pair


def constructLawsField(problem):
    choice_explanation_pairs = filter(None, map(pairChoiceWithExplanation, problem['jiexi'].split('\n')))
    choice_explanation_pairs = reduce(operator.iconcat, choice_explanation_pairs, []) # flatten the list

    try:
        choice_articles_pairs = list(map(pairChoiceWithArticles, choice_explanation_pairs))
    except InvalidLawError:
        return None

    sorted(choice_articles_pairs, key=lambda pair: pair[0])  # sort by choice alphabetically

    problem['laws'] = list(map(lambda pair: pair[1], choice_articles_pairs))
    return problem


with open("assets/LawData.json", "r", encoding="utf-8") as file:
    problems = json.loads(file.read())
    file.close()

problems = map(splitAnswers, problems)
problems = map(splitChoices, problems)
problems = list(filter(None, map(constructLawsField, problems)))

with open("output.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(problems, ensure_ascii=False, indent="\t"))
    file.close()
