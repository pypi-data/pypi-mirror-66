# LCSB-PBIN

Small library to send a paste on the LCSB private bin.

This one is a bit modified and does not allow paste to be sent without authentication.

## Install 

pip install lcsb_pbin

## Usage

```python
import lcsb_pbin
link = lcsb_pbin.paste(
    "https://privatebin.lcsb.uni.lu",
    """
# Header
lorem ipsum
    """,
    "lums-username",
    "lums-password",
    paste_password='passw0rd',
    formatter="markdown",
    opendiscussion=True,
    burnafterreading=False,
    expire="1month",
    debug=False,
)
print(link)
```