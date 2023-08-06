# Falcon Query Parameter Verifier

A simple falcon hook to check if a request contains all required query parameters.

***

## Installation / Requirements

Installation:

**PyPi**

```
pip install falcon_params_verifier
```

**.whl**

A ``.whl`` is provided in the releases tab in Github. 

## Sample Usage

*Sample code*

```python
import falcon
import falcon_params_verifier 
from falcon_params_verifier import ParamVerifier # This can also be used.

class SampleResource(object):
    def __init__(self):
        self._required_params = [
            "userId",
        ]
    # Add the hook
	@falcon.before(falcon_params_verifier.ParamVerifier(self._required_params))
    def on_get(self, req, resp):
        req.media = {
            "message": "Whoo hoo, you made a proper request!"
        }
```

***

If a query parameter is missing, the module will automatically raise an ``falcon.HTTPBadRequest``.

