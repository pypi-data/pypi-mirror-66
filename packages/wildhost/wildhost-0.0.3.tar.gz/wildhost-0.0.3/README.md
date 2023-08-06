# Wildhost

[![CircleCI](https://circleci.com/gh/circleci/circleci-docs.svg?style=svg)](https://circleci.com/gh/circleci/circleci-docs)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/bunnymq.svg)](https://pypi.python.org/pypi/bunnymq/)
[![PyPI version fury.io](https://badge.fury.io/py/wildhost.svg)](https://pypi.python.org/pypi/bunnymq/)

Checks wildcard domain names.

## Install
```
pip install wildhost
```

## Usage
Import the module

```python
>>> import wildhost
```
Pass a hostname to the `check` function.

```python
>>> wildhost.check('foo.bar.domain.tld')
```

If none of the levels of the name are wildcards, `None` will be returned.
```python
>>> wildhost.check('mail.google.com')
```

This returns `None` as neither `google.com` nor `mail.google.com` are wildcards.

For a wildcard name, the _lowest_ level wildcard name will be returned.
```python
>>> wildhost.check('foo.bar.spam.grok.sharefile.com')
'sharefile.com'
```

## Performance
The module caches the wildcard results and uses them in further checks. For example:

```python
>>> wildhost.check('foo.bar.spam.grok.sharefile.com')  # this will be a fresh check
'sharefile.com'
>>> wildhost.check('boom.blast.sharefile.com')  # this will use the cache
'sharefile.com'
```

Once `sharefile.com` is known to be a wildcard, any further subdomains of `sharefile.com` will be evaluated as wildcards as well. This is determined from a static check and therefore very fast.

However, there is a caveat. In an _unlikely_ scenario, `api.sharefile.com` will be missed, if it happens to be a valid subdomain.

In such cases, when in doubt, use the `wildcard.check_fresh` function to ignore the cache.
```python
>>> wildcard.check_fresh('api.sharefile.com')
```

This will return `None` if it is, in fact, not a wildcard.

> `check_fresh` needs to make network requests, where as `check` caches the results and is very fast. Choose one that is suitable for the problem at hand.
