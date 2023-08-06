<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. Logo</a></li>
<li><a href="#sec-2">2. Check Test</a></li>
<li><a href="#sec-3">3. Pypi</a></li>
<li><a href="#sec-4">4. Dame Music</a></li>
<li><a href="#sec-5">5. License</a></li>
</ul>
</div>
</div>

Webutils from Tests by David Arroyo Menéndez

# Logo<a id="sec-1" name="sec-1"></a>

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Seller_of_eggs.jpg/320px-Seller_of_eggs.jpg)](https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Seller_of_eggs.jpg/320px-Seller_of_eggs.jpg)

# Check Test<a id="sec-2" name="sec-2"></a>

-   Execute all tests:

    $ ./testsbycommands.sh

# Pypi<a id="sec-3" name="sec-3"></a>

-   To install from local:

$ pip install -e .

-   To install create tar.gz in dist directory:

$ python3 setup.py register sdist

-   To upload to pypi:

$ twine upload dist/damenumpy-0.1.tar.gz

-   You can install from Internet in a python virtual environment to check:

$ python3 -m venv /tmp/dw
$ cd /tmp/dw
$ source bin/activate
$ pip3 install damewebutils

# Dame Music<a id="sec-4" name="sec-4"></a>

[Listen music &#x2026;](https://www.youtube.com/playlist?list=PLeobXV-Yyn-LvQydcnr46ZkGh1V6tDGEk)

# License<a id="sec-5" name="sec-5"></a>

This document is under a [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/deed)

[![img](http://i.creativecommons.org/l/by/3.0/80x15.png)](http://creativecommons.org/licenses/by/4.0/deed)