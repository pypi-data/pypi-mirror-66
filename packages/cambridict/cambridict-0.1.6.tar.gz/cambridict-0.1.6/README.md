# Cambridge Dictionary
Search the meaning of the word from Cambridge Dictionary online, and get the result in JSON format

## Installation

You can install the `cambridict` from PyPI:

```
pip install cambridict
```

## How to use

```python
import json

from cambridict import Cambridge

d = Cambridge('EV')

word = 'take'
data = d.search(word)

result = '{0}.json'.format(word)
with open(result, 'w') as fp:
    json.dump(data, fp, indent=4)

```

Sample output [take.json](https://github.com/tegieng7/cambridict/blob/master/tests/take.json)

## Supported dictionaries

| Name | Dictionary                                                                            |
|------|---------------------------------------------------------------------------------------|
| `EE` | [English](https://dictionary.cambridge.org/dictionary/english/)                       |
| `EV` | [English-Vietnamese](https://dictionary.cambridge.org/dictionary/english-vietnamese/) |

