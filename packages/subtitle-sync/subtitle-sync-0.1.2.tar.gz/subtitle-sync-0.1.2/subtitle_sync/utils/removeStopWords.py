import copy


def removeStopwordsSubs(nlp, subtitle):
    subtitleWithoutStopWords = []
    for line in subtitle:
        doc = nlp(line["content"])
        tokens = [token.lemma_ for token in doc if not token.is_punct]
        subtitleWithoutStopWords.append(
            {
                "lemma": tokens,
                "content": line["content"],
                "start": line["start"].seconds,
                "end": line["end"].seconds,
            }
        )

    return subtitleWithoutStopWords


def removeStopwordsScript(nlp, script):
    def removeStopwordsAndReturnLemma(dialogue):
        screenplayWithoutStopWords = []

        # extract lemma from dialogue
        doc = nlp(dialogue.lower())
        tokens = [token.lemma_ for token in doc if not token.is_punct]
        screenplayWithoutStopWords += tokens
        return screenplayWithoutStopWords

    scriptWithoutStopWords = []
    for content in script:
        scriptWithoutStopWords.append(copy.copy(content))
        scriptWithoutStopWords[-1]["lemma"] = removeStopwordsAndReturnLemma(
            content["dialogue"]
        )
    return scriptWithoutStopWords
