import re


def formatSubs(nlp, subtitles):
    formattedSubtitles = []
    hasPunctuationAtEnd = True
    hasEllipsesAtEnd = False
    for subtitle in subtitles:
        newContent = subtitle.content
        TAG_RE = re.compile(r"([a-zA-Z]+:\n?)?<[^>]+>")
        newContent = TAG_RE.sub("", newContent.lower())

        if ("[" in newContent[0] or "[" in newContent[1]) and "]" in newContent[-1]:
            continue

        newContent = re.sub("[\[].*?[\]]", "", newContent).strip()
        newContent = newContent[2:] if "--" == newContent[0:2] else newContent
        newContent = newContent.replace("--", ".")

        if "-" not in newContent[0] and "\n-" not in newContent:
            newContent = newContent.replace("\n", " ")

        hasPunctuationBeforeLine = (
            any(newContent[newContent.index("\n") - 1] == x for x in [".", "!", "?"])
            if "\n" in newContent
            else False
        )

        if not hasPunctuationAtEnd:
            formattedSubtitles[-1]["content"] += " " + newContent.replace("...", "")
            formattedSubtitles[-1]["end"] = subtitle.end
        else:
            if hasEllipsesAtEnd and "..." in newContent:
                newContent = newContent.replace(
                    "...", formattedSubtitles[-1]["content"] + " "
                )
            if "-" in newContent[0]:
                newContent = newContent[1:]
            if "\n-" in newContent:
                newContent = newContent.replace("\n-", " ")
            if "\n" in newContent:
                newContent = newContent.replace("\n", " ")

            newContent = re.sub(" \s+", " ", newContent)
            doc = nlp(newContent)
            sentences = [sent.string.strip() for sent in doc.sents]
            for sentence in sentences:
                if (
                    len(sentences) == 1
                    and len(sentence.split(" ")) == 1
                    and "..." not in sentence
                ):
                    sentence = sentence.replace(".", "") + "$"
                formattedSubtitles.append(
                    {
                        "content": sentence.replace("...", ""),
                        "start": subtitle.start,
                        "end": subtitle.end,
                        "index": subtitle.index,
                    }
                )

        hasPunctuationAtEnd = any(
            newContent[-1] == x for x in [".", "!", "?", '"', "♪"]
        )
        hasEllipsesAtEnd = newContent[-3:] == "..."

    return formattedSubtitles


def formatScript(nlp, script):
    currentTimestamp = None
    previousTimestamp = None
    newScript = []

    for pageIndex, page in enumerate(script):
        for sceneIndex, content in enumerate(page["content"]):
            if "scene_number" in content:
                for sectionIndex, scene in enumerate(content["scene"]):
                    if scene["type"] == "CHARACTER" or scene["type"] == "DUAL_DIALOGUE":
                        dialogues = ""

                        def decoupleDialogue(dialogueList):
                            dialogue = " ".join(
                                list(filter(lambda x: "(" != x[0], dialogueList))
                            )
                            return dialogue

                        if scene["type"] == "CHARACTER":
                            dialogues = decoupleDialogue(scene["content"]["dialogue"])
                        else:
                            dialogues = decoupleDialogue(
                                scene["content"]["character1"]["dialogue"]
                            )
                            dialogues += decoupleDialogue(
                                scene["content"]["character2"]["dialogue"]
                            )

                        # remove interrupt(ed) dialogues "--"
                        if "--" == dialogues[0:2]:
                            dialogues = dialogues[2:]
                        if "--" == dialogues[-2:]:
                            dialogues = dialogues[0:-2] + "."

                        doc = nlp(dialogues)
                        sentences = [sent.string.strip() for sent in doc.sents]
                        for sentence in sentences:
                            if len(sentences) == 1 and len(sentence.split(" ")) == 1:
                                sentence = sentence.replace(".", "") + "$"
                            newScript.append(
                                {
                                    "dialogue": sentence.strip().lower(),
                                    "pageIndex": pageIndex,
                                    "sceneIndex": sceneIndex,
                                    "sectionIndex": sectionIndex,
                                }
                            )
                            if "," in sentence:
                                breakCommas = sentence.strip().lower().split(",")
                                for miniSentence in breakCommas:
                                    newScript.append(
                                        {
                                            "dialogue": miniSentence,
                                            "pageIndex": pageIndex,
                                            "sceneIndex": sceneIndex,
                                            "sectionIndex": sectionIndex,
                                        }
                                    )
    return newScript
