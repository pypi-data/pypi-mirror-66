import re
import json

from subtitle_sync.utils.traverseDialogue import traverseDialogue
from subtitle_sync.utils.removeStopWords import (
    removeStopwordsScript,
    removeStopwordsSubs,
)

def getUniqueWordsSubs(subsWithoutStopwords):
    uniqueWords = {}
    for subtitle in subsWithoutStopwords:
        for word in subtitle["lemma"]:
            uniqueWords.setdefault(
                word, {"count": 0, "content": []},
            )
            uniqueWords[word]["count"] += 1
            uniqueWords[word]["content"].append(
                {
                    "lemma": subtitle["lemma"],
                    "dialogue": subtitle["content"],
                    "timestamp": (subtitle["start"], subtitle["end"]),
                }
            )
    uniqueWords = {k: v for k, v in uniqueWords.items() if v["count"] <= 2}
    return uniqueWords


def getUniqueWordsScript(scriptWithoutStopWords):
    uniqueWords = {}
    for index, section in enumerate(scriptWithoutStopWords):
        for lemmaWord in section["lemma"]:
            uniqueWords.setdefault(lemmaWord, {"count": 0, "content": [],})
            uniqueWords[lemmaWord]["count"] += 1
            uniqueWords[lemmaWord]["content"].append(
                {
                    "lemma": section["lemma"],
                    "dialogue": section["dialogue"],
                    "index": index,
                }
            )
    uniqueWords = {k: v for k, v in uniqueWords.items() if v["count"] <= 2}
    return uniqueWords


def getMatchingUniqueWords(uniqueWords, subsUniqueWords):
    matchingUniqueWords = []

    def getNumberOfSameWords(scriptContent, subsContent):
        count = 0
        for scriptLemma in set(scriptContent["lemma"]):
            for subtitleLemma in set(subsContent["lemma"]):
                if scriptLemma == subtitleLemma:
                    count += 1
        return count

    for subsWord, subsValue in subsUniqueWords.items():
        for scriptWord, scriptValue in uniqueWords.items():
            if subsWord == scriptWord:
                for index, subsContent in enumerate(subsValue["content"]):
                    if index >= len(scriptValue["content"]):
                        continue

                    scriptContent = scriptValue["content"][index]
                    # number of words in subtitle and screenplay dialogue that's the same
                    count = getNumberOfSameWords(scriptContent, subsContent)

                    otherWordsCount = len(
                        set(scriptContent["lemma"] + subsContent["lemma"])
                    )
                    minDialogueLength = min(
                        len(scriptContent["lemma"]), len(subsContent["lemma"]),
                    )

                    isOneWord = "$" in subsWord[-1]
                    isManyCount = count > 5
                    checkCheck = otherWordsCount - count <= minDialogueLength

                    if isOneWord or isManyCount or checkCheck:
                        if (
                            len(matchingUniqueWords) > 0
                            and matchingUniqueWords[-1]["word"] == subsWord
                        ):
                            matchingUniqueWords[-1]["content"].append(
                                {
                                    "timestamp": subsContent["timestamp"],
                                    "index": scriptContent["index"],
                                }
                            )
                        else:
                            matchingUniqueWords.append(
                                {
                                    "word": subsWord,
                                    "content": [
                                        {
                                            "timestamp": subsContent["timestamp"],
                                            "index": scriptContent["index"],
                                        }
                                    ],
                                }
                            )

    return matchingUniqueWords


def getScriptWithUniqueWordsTimestamp(script, matchingUniqueWords):
    for matchingUniqueWord in matchingUniqueWords:
        for content in matchingUniqueWord["content"]:
            script[content["index"]]["timestamp"] = content["timestamp"]
    return script


def getSubsWithUniqueWordsTimestamp(subsWithoutStopwords, subsUniqueWords):
    for subtitle in subsWithoutStopwords:
        for word in subtitle["lemma"]:
            if word in subsUniqueWords:
                if "unique" in subtitle:
                    subtitle["unique"].append(word)
                else:
                    subtitle["unique"] = [word]
    return subsWithoutStopwords


def markScriptWithRareWordsTimestamp(nlp, script, subtitle):
    subsWithoutStopwords = removeStopwordsSubs(nlp, subtitle)
    subsUniqueWords = getUniqueWordsSubs(subsWithoutStopwords)

    scriptWithoutStopWords = removeStopwordsScript(nlp, script)
    scriptUniqueWords = getUniqueWordsScript(scriptWithoutStopWords)

    matchingUniqueWords = getMatchingUniqueWords(scriptUniqueWords, subsUniqueWords)

    scriptWithUniqueWordsTimestamp = getScriptWithUniqueWordsTimestamp(
        scriptWithoutStopWords, matchingUniqueWords
    )
    subsWithUniqueWordsTimestamp = getSubsWithUniqueWordsTimestamp(
        subsWithoutStopwords, subsUniqueWords
    )
    return (script, scriptWithUniqueWordsTimestamp, subsWithUniqueWordsTimestamp)
