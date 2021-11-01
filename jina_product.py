from jina import  DocumentArrayMemmap, Flow, Executor, requests, Document, DocumentArray,Client
from jina.types.document.generators import from_files
from flash.image import ImageEmbedder
from jina.types.request import Response

import pandas as pd
import numpy as np


docs_array=DocumentArray(from_files('../images/*.jpg'))

class FlashImageEncoder(Executor):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._embedder=ImageEmbedder(embedding_dim=1024)

    @requests
    def predict(self,docs:DocumentArray,**kwargs):
        embeds=self._embedder.predict(docs.get_attributes('uri'))
        for doc, embed in zip(docs,embeds):
            doc.embedding=embed.numpy()

class SimpleIndexer(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dam = DocumentArrayMemmap(self.workspace)

    @requests(on='/index')
    def index(self, docs: DocumentArray, **kwargs):
        self._dam.extend(docs)

    @requests(on='/search')
    def search(self, docs: DocumentArray, **kwargs):
        docs.match(self._dam)

f = (
    Flow(cors=True, port_expose=12345, protocol="http")
        .add(uses=FlashImageEncoder, name="Encoder")
        .add(uses=SimpleIndexer, name="Indexer")
)

with f:
    f.post('/index', docs_array)
    f.block()


def print_matches(resp: Response):  # the callback function invoked when task is done
    for idx, d in enumerate(resp.docs[0].matches[:3]):  # print top-3 matches
        print(f'[{idx}]{d.scores["Mobiles"].value:2f}: "{d.text}"')

