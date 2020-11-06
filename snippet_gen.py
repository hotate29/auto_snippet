import os
import sys
import glob
import json
import re
from logging import basicConfig,INFO,getLogger

import config

basicConfig(level=INFO)
logger = getLogger(__name__)
target_files = [(path, config.ext_lang[path[-2:]])
                for path in glob.glob(f"**/{config.target}/**") if path[-2:] in config.ext_lang]
comment_get = re.compile(r"#\s*.*")
remove_hash = re.compile(r"#\s*")

snippets = {}
for path, lang in target_files:
    with open(path, "r", encoding="utf-8") as f:
        li = f.read()
        all_comment = comment_get.findall(li)
        if len(all_comment) < 2:
            logger.info(f"skip {path}")
            continue
        logger.info(f"collection {path}")
        title_comment, prefix_comment, *comments, = all_comment
        snippet_title = remove_hash.sub("", title_comment)
        snippet_prefix = remove_hash.sub("", prefix_comment)
        snippet = li.replace(title_comment+"\n", "").replace(prefix_comment+"\n", "")
        assert isinstance(config.indent, int)
        indent = " " * config.indent
        snippet = snippet.replace(indent,r"\t").splitlines()
        snippets[snippet_title] = {
            "scope": lang,
            "prefix": snippet_prefix,
            "body": snippet
        }

with open("/snippet.code-snippets","w",encoding="utf-8") as f:
    a = json.dumps(snippets,indent=4).replace(r"\\t",r"\t")
    f.write(a)
logger.info("done!")
