## resolve-hash

Allow to resolve a hash to a known URL representation.

### Usage

`resolve-hash <hash>` outputs URL matching the hash

**Output:** URL matching the hash, if found

**Exit code:**
  * 0 if the hash has been found
  * 1 if the hash has NOT been found

**Example:**

```shell
$ resolve-hash 8d8645468228
https://devcentral.nasqueron.org/rKERUALD8d8645468228

$ resolve-hash 00000000000000
https://github.com/seungwonpark/ghudegy-chain/commit/00000000000000c06d2e8c36f247206a9a4b1c63

$ resolve-hash not_a_hash
$ echo $?
1
```

### Why this package?

Terminator has a comprehensive plugins' system to offer extra features,
like resolve console output as links.

Meanwhile, it's sometimes convenient to open a link in a browser,
especially if the VCS hash is resolved to the code review system. 

### Hash sources

#### VCS
* Phabricator, browsing your .arcrc file to know the instances you work with
* Gerrit, if explicitly configured
* GitHub
* GitLab, if you provide a token, as search queries must be authenticated

### Configuration

You can provide a configuration by creating a `$HOME/.config/resolve-hash.conf` file.

Configuration is a YAML file.

| Variable            | Description                   | Format          |
|---------------------|-------------------------------|-----------------|
| gerrit              | URL to your Gerrit instances  | List of strings |
| gitlab_public_token | Personal token for GitLab.com | string          |

Example:

```yaml
gerrit:
  - https://gerrit.wikimedia.org/r/

gitlab_public_token: glpat-sometoken
```

### Use as a library

You can use the package as a library to resolve hashes in your application:

```python
from resolvehash.vcs import phabricator

url = phabricator.query_phabricator_instances("/home/luser/.arcrc", "8d8645468228")
print(url)
```

### Extend the code

#### How to add a new VCS source?

If you wish to add a new VCS source, add a method in VcsHashSearch,
then add it to `get_search_methods`.

#### How to add a hash source?

If you wish to extend this script by searching Foo in addition to VCS,
you can create a class FooHashSearch with the following methods:

  * `__init__(self, config, needle_hash)`: constructor called by the script
  * `search(self)`: perform your search, return a URL or None

#### How can I contribute?

You can commit your changes to the upstream by following instructions at
https://agora.nasqueron.org/How_to_contribute_code

The canonical repository is https://devcentral.nasqueron.org/source/resolve-hash.git

### License

BSD-2-Clause, see `LICENSE` file.
