<div>
  <p>
  	  <a href="https://pypistats.org/packages/spbdl"><img src="https://img.shields.io/pypi/dm/spbdl.svg"></a>
  	  <a href="https://travis-ci.com/boidushya/spbdl/"><img src="https://travis-ci.com/Boidushya/spbdl.svg?branch=master&amp;status=passed" /></a>
	  <a href="https://pypi.org/project/spbdl/"><img src="https://img.shields.io/pypi/v/spbdl.svg" alt="pypi"></a>
	  <a href="https://pypi.python.org/pypi/spbdl/"><img src="https://img.shields.io/pypi/pyversions/spbdl.svg" /></a>
  </p>
</div>

# SPBDL

Download images (custom/random) from shitpostbot database!

# SPBDL Module Installation:

#### Install with pip:
```
pip install spbdl
```
#### Install from source:
```
$ git clone https://github.com/boidushya/spbdl  
$ cd spbdl
$ python setup.py install
```

# USAGE:
```python
import spbdl
import requests

def dl(url):
    r = requests.get(url)
    with open("randomImage.jpg","wb") as f:
        f.write(r.content)
#Random image download
url = spbdl.randImg()
#Queried image download:
url2 = spbdl.getImg("epic") #Uses the default arguments for getting image url
url3 = spbdl.getImg("epic",review="accepted",sort='top', order='created_at',direction="ASC") #Passes custom arguments for getting image url
dl(url)
#dl(url2)
#dl(url3)
```

# ALLOWED VALUES FOR getImg ARGUMENTS:

* ##### query:
	* `<your search query>` (required)
* ##### review:
	* `accepted` (default)
	* `awaiting-yes`
	* `pending`
	* `awaiting-no`
	* `denied`
	* `all`
* ##### sort:
	* `random` (default)
	* `top`
	* `bottom`
* ##### order:
	* `total_rating` (default)
	* `last_reviewed_at`
	* `created_at`
* ##### direction:
	* `DESC` (default)
	* `ASC`
