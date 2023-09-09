import json
import math
from typing import List

import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = ''

_DESCRIPTION = """\
Выдержки из руководства пользователя для генерации ответов по запросу пользователя.\
"""
_LICENSE = ''

_URL = "https://huggingface.co/datasets/nodlnodl/kb"
_URLS = {
    "train": _URL + "kb.json",
}


class LFQAKBConfig(datasets.BuilderConfig):
    """билдер конфиг"""

    def __init__(
            self, language="ru", snippets_length=50, snippets_overlap=25, **kwargs
    ):
        """
        билдер кофинг
        """
        super(LFQAKBConfig, self).__init__(**kwargs)
        self.language = language
        self.snippets_length = snippets_length
        self.snippets_overlap = snippets_overlap


class LFQASnippets(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [LFQAKBConfig(
        name="LFQAKnowledgeBase",
        version=datasets.Version("1.0.0"),
        language="en",
        snippets_length=50,
        snippets_overlap=25,
    )]

    test_dummy_data = False

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "title": datasets.Value("string"),
                    "heading1": datasets.Value("string"),
                    "heading2": datasets.Value("string"),
                    "heading3": datasets.Value("string"),
                    "heading4": datasets.Value("string"),
                    "heading5": datasets.Value("string"),
                    "text": datasets.Value("string"),

                }
            ),
            supervised_keys=None,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        downloaded_files = dl_manager.download_and_extract(_URLS)

        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files['train']})]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding='utf-8') as f:
            lfqa = json.load(f)
            for article in lfqa:
                id_ = article.get('id', '')
                title = article['title']
                heading1 = article['heading1']
                heading2 = article['heading2']
                heading3 = article['heading3']
                heading4 = article['heading4']
                heading5 = article['heading5']
                text = article['text']
                yield id_, {
                    "title": title,
                    "heading1": heading1,
                    "heading2": heading2,
                    "heading3": heading3,
                    "heading4": heading4,
                    "heading5": heading5,
                    "text": text
                }
