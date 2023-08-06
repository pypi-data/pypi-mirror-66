from __future__ import unicode_literals, print_function
import json
import re
import argparse

import srt
import spacy

from subtitle_sync.formatText import formatSubs, formatScript
from subtitle_sync.markScriptWithRareWordsTimestamp import (
    markScriptWithRareWordsTimestamp,
)
from subtitle_sync.utils.furtherSyncScript import furtherSyncScript


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Screenplay PDF into JSON")

    parser.add_argument(
        "-s",
        metavar="screenplay",
        type=str,
        help="screenplay PDF filename",
        required=True,
    )

    # start from skipPage set up by user.  default to 0
    args = parser.parse_args()
    movieTitle = args.s

    subtitle = open("{}.srt".format(movieTitle), "r")
    subtitle = list(srt.parse(subtitle.read()))

    script = open("{}.json".format(movieTitle), "rb")
    script = json.load(script)

    nlp = spacy.load("en_core_web_lg")
    nlp.add_pipe(nlp.create_pipe("sentencizer"))

    subtitle = formatSubs(nlp, subtitle)
    script = formatScript(nlp, script)

    (
        script,
        scriptWithTimestamp,
        subsWithTimestamp,
    ) = markScriptWithRareWordsTimestamp(nlp, script, subtitle)

    minPrevTimestamp = (
        scriptWithTimestamp[0]["timestamp"][0]
        if "timestamp" in scriptWithTimestamp[0]
        else 99999
    )
    for content in scriptWithTimestamp:
        if minPrevTimestamp > (
            content["timestamp"][0] if "timestamp" in content else 99999
        ):
            print("------")
            print(minPrevTimestamp)
            print(content)
            print("------")
            minPrevTimestamp = min(content["timestamp"][0], minPrevTimestamp)

    file0 = open("mvp_results/{}_time.json".format(movieTitle), "w+")
    json.dump(scriptWithTimestamp, file0, indent=4, ensure_ascii=False)
    x = 0
