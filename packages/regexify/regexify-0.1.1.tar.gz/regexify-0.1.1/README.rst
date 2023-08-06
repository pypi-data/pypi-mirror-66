
|Contributors| |Forks| |Stargazers| |Issues| |MIT License|
.. raw:: html
   <!-- PROJECT LOGO -->
.. raw:: html
   <div>
.. raw:: html
   <p>
.. raw:: html
   </p>
.. raw:: html
   <h3 align="center">
regexify
.. raw:: html
   </h3>
.. raw:: html
   <p>
Utilities/containers for deploying regular expressions.
.. raw:: html
   </p>
.. raw:: html
   </div>
.. raw:: html
   <!-- TABLE OF CONTENTS -->
Table of Contents
-----------------
-  `About the Project <#about-the-project>`__
-  `Getting Started <#getting-started>`__
   -  `Prerequisites <#prerequisites>`__
   -  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Roadmap <#roadmap>`__
-  `Contributing <#contributing>`__
-  `License <#license>`__
-  `Contact <#contact>`__
-  `Acknowledgements <#acknowledgements>`__
About the Project
-----------------
This package contains a few useful functions and classes for
building/using regular expressions.
.. raw:: html
   <!-- GETTING STARTED -->
Getting Started
---------------
Prerequisites
~~~~~~~~~~~~~
-  Python 3.7+
Installation
~~~~~~~~~~~~
Install using pip:
``pip install regexify``
Usage
-----
See the test files for example usage.
Pattern Trie
~~~~~~~~~~~~
Compile multiple terms into a single pattern.
.. code:: python
   import re
   from regexify import PatternTrie
   data = ['there', 'hi', 'python', 'pythons', 'hiya']
   trie = PatternTrie(*data)
   pat = re.compile(trie.pattern)
Versions
--------
Uses `SEMVER <https://semver.org/>`__.
See https://github.com/dcronkite/regexify/releases.
.. raw:: html
   <!-- ROADMAP -->
Roadmap
-------
See the `open issues <https://github.com/dcronkite/regexify/issues>`__
for a list of proposed features (and known issues).
.. raw:: html
   <!-- CONTRIBUTING -->
Contributing
------------
Any contributions you make are **greatly appreciated**.
1. Fork the Project
2. Create your Feature Branch
   (``git checkout -b feature/AmazingFeature``)
3. Commit your Changes (``git commit -m 'Add some AmazingFeature'``)
4. Push to the Branch (``git push origin feature/AmazingFeature``)
5. Open a Pull Request
.. raw:: html
   <!-- LICENSE -->
License
-------
Distributed under the MIT License.
See ``LICENSE`` or https://dcronkite.mit-license.org for more
information.
.. raw:: html
   <!-- CONTACT -->
Contact
-------
Please use the `issue tracker <https://github.com/dcronkite/regexify/issues>`__.
.. raw:: html
   <!-- ACKNOWLEDGEMENTS -->
Acknowledgements
----------------
.. raw:: html
   <!-- MARKDOWN LINKS & IMAGES -->
.. raw:: html
   <!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
.. raw:: html
   <!-- [product-screenshot]: images/screenshot.png -->
.. |Contributors| image:: https://img.shields.io/github/contributors/dcronkite/regexify.svg?style=flat-square :target: https://github.com/dcronkite/regexify/graphs/contributors
.. |Forks| image:: https://img.shields.io/github/forks/dcronkite/regexify.svg?style=flat-square :target: https://github.com/dcronkite/regexify/network/members
.. |Stargazers| image:: https://img.shields.io/github/stars/dcronkite/regexify.svg?style=flat-square :target: https://github.com/dcronkite/regexify/stargazers
.. |Issues| image:: https://img.shields.io/github/issues/dcronkite/regexify.svg?style=flat-square :target: https://github.com/dcronkite/regexify/issues
.. |MIT License| image:: https://img.shields.io/github/license/dcronkite/regexify.svg?style=flat-square :target: https://kpwhri.mit-license.org/