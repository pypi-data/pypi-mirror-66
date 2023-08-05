[![PyPI version](https://badge.fury.io/py/similar-sentences.svg)](https://badge.fury.io/py/similar-sentences)

# similar-sentences

Install the package

```python
pip install similar-sentences
```

```python
from SimilarSentences import SimilarSentences
model = SimilarSentences('model.zip',"predict")
text = 'How are you doing?'
suggestions = model.predict(text, 2, "simple")
print(suggestions)
```
Output looks like

```python

````
