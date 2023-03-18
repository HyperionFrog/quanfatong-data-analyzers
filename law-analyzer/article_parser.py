import re, copy
from cn2an import cn2an


class Article:
    id = 0
    contents = []


def divideArticles(contents):
    begin_idx, end_idx = 0, 0
    article_pattern = re.compile("第(\S+)条\s+\S+")
    article_register = Article()

    articles = []

    def isStartOfArticle(idx, contents):
        return article_pattern.match(contents[idx])

    def isEndOfArticle(idx, contents):
        return idx == len(contents) - 1 or article_pattern.match(contents[idx + 1])

    def isEndOfContents(idx, contents):
        return idx == len(contents) - 1

    for idx, line in enumerate(contents):
        if isStartOfArticle(idx, contents):
            begin_idx = idx
            article_register.id = cn2an(article_pattern.match(line).group(1))
            if article_register.id == 1164:
                pass
        if isEndOfContents(idx, contents) or isEndOfArticle(idx, contents):
            end_idx = idx
            article_register.contents = contents[begin_idx: end_idx + 1]
            try:
                text = re.match("第\S+条\s+(\S+)", article_register.contents[0].replace(" ", "")).group(1)
                article_register.contents[0] = text
            except:
                pass
            articles.append(copy.deepcopy(article_register))

    return articles


def parseArticles(contents):
    articles = divideArticles(contents)

    return articles
