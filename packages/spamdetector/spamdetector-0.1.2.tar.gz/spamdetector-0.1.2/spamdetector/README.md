### Using Machine Learning Models as a Package

#### Spamdetector ML Package


#### Usage of Package

```python
>>> from spamdetector import CommentClassifier
>>> cc = CommentClassifier()
>>> cc.text = "This is a great project"
>>> cc.predict()

```

#### Loading Different Models and Classify
```python
>>> from spamdetector import CommentClassifier
>>> cc = CommentClassifier()
>>> cc.text = "This is a great project"
>>> cc.load('nb')

```

```python
>>> from spamdetector import CommentClassifier
>>> cc = CommentClassifier()
>>> mytext = "This is a great Project"
>>> cc.classify(mytext)
```
