# A Wikipedia Plain Text Extractor with Link Annotations (and stuff)

This is port of @jodaiber's [Annotated-WikiExtractor](https://github.com/jodaiber/Annotated-WikiExtractor) which is built upon [Wikipedia Extractor by Medialab](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor).


# Usage

```
$
$ mkdir extracted-new
$ bzip2 -dc enwiki-latest-pages-articles.xml.bz2 | python3 extract.py extracted-new/
```
