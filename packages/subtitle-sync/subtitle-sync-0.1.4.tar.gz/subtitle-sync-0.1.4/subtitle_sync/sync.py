from __future__ import unicode_literals, print_function
import json
import re
import argparse
import copy

import srt
import spacy

from subtitle_sync.formatText import formatSubs, formatScript
from subtitle_sync.markScriptWithRareWordsTimestamp import (
    markScriptWithRareWordsTimestamp,
)
from subtitle_sync.utils.furtherSyncScript import furtherSyncScript
from subtitle_sync.utils.traverseDialogue import traverseDialogue


def sync(moviePath, subsPath):
    # subtitle = open(subsPath, "r")
    # subtitle = list(srt.parse(subtitle.read()))

    script = open(moviePath, "rb")
    script = json.load(script)
    pureScript = copy.copy(script)

    # nlp = spacy.load("en_core_web_lg")
    # nlp.add_pipe(nlp.create_pipe("sentencizer"))

    # subtitle = formatSubs(nlp, subtitle)
    # script = formatScript(nlp, script)

    # (
    #     script,
    #     scriptWithTimestamp,
    #     subsWithTimestamp,
    # ) = markScriptWithRareWordsTimestamp(nlp, script, subtitle)

    scriptWithTimestamp = open("her1.json", "r")
    scriptWithTimestamp = json.load(scriptWithTimestamp)

    index = 0
    for pageIndex, page in enumerate(pureScript):
        for contentIndex, content in enumerate(page["content"]):
            if "scene_info" in content:
                for sceneIndex, scene in enumerate(content["scene"]):
                    if scene["type"] == "CHARACTER" or scene["type"] == "DUAL_DIALOGUE":

                        testDialogues = ""
                        if scene["type"] == "DUAL_DIALOGUE":
                            testDialogues = [
                                scene["content"]["character1"]["dialogue"],
                                scene["content"]["character2"]["dialogue"],
                            ]
                        else:
                            testDialogues = [scene["content"]["dialogue"]]

                        for line in scriptWithTimestamp:
                            if (
                                any(
                                    [
                                        line["dialogue"]
                                        in " ".join(
                                            list(
                                                filter(
                                                    lambda x: "(" != x[0], testDialogue,
                                                )
                                            )
                                        ).lower()
                                        for testDialogue in testDialogues
                                    ]
                                )
                                and "timestamp" in line
                            ):
                                pureScript[pageIndex]["content"][contentIndex]["scene"][
                                    sceneIndex
                                ]["content"]["timestamp"] = line["timestamp"]

    # minPrevTimestamp = (
    #     scriptWithTimestamp[0]["timestamp"][0]
    #     if "timestamp" in scriptWithTimestamp[0]
    #     else 99999
    # )
    # for content in scriptWithTimestamp:
    #     if minPrevTimestamp > (
    #         content["timestamp"][0] if "timestamp" in content else 99999
    #     ):
    #         print("------")
    #         print(minPrevTimestamp)
    #         print(content)
    #         print("------")
    #         minPrevTimestamp = min(content["timestamp"][0], minPrevTimestamp)
    return pureScript


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Screenplay PDF into JSON")

    parser.add_argument(
        "-m",
        metavar="screenplay",
        type=str,
        help="screenplay json path",
        required=True,
    )

    parser.add_argument(
        "-s", metavar="subs", type=str, help="subtitle json path", required=True,
    )

    # start from skipPage set up by user.  default to 0
    args = parser.parse_args()
    moviePath = args.m
    subsPath = args.s
    scriptWithTimestamp = sync(moviePath, subsPath)
    file0 = open("timestamped.json", "w+")
    json.dump(scriptWithTimestamp, file0, indent=4, ensure_ascii=False)
