0.2.1 (2020-04-22)
------------------
**Fixed**

- Updated deployment credentials

0.2.0 (2020-04-22)
------------------
**Breaking**

- Support has been dropped for Python 2.6, 3.0, 3.1, 3.2, 3.3, 3.4

**Added**

- Support for Python 3.6, 3.7
- History from backups can now be applied to profiles (@outdooracorn)

**Fixed**

- Error writing backup files (#1)

0.1.8 (2016-09-20)
------------------
**Added**

- History retrieval requests are now automatically retried 3 times if any error is returned (timeouts, server overloaded, etc..), a prompt will be displayed if the request fails more than 3 times

**Fixed**

- Failed profile requests were incorrectly being cached

0.1.7 (2016-09-19)
------------------
**Fixed**

- Records could be duplicated if watched history changes while the scanner is running

0.1.6 (2016-09-19)
------------------
**Fixed**

- Added missing "six" requirement

0.1.5 (2016-09-19)
------------------
**Changed**

- History records are now removed in batches of 200 items (to avoid read timeouts)

**Fixed**

- Connection errors weren't being caught correctly during history removal

0.1.4 (2016-09-17)
------------------
**Fixed**

- Issue deploying github releases (possible)

0.1.3 (2016-09-17)
------------------
**Fixed**

- Issue deploying github releases

0.1.2 (2016-09-17)
------------------
**Changed**

- Updated package metadata

0.1.1 (2016-09-17)
------------------
**Fixed**

- PyPI deployment issue in [.travis.yml]

0.1.0 (2016-09-17)
------------------
Initial release
