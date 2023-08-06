## Curl2

Curl code convert to some programming languages

Thanks for curlconverter!

Currently supported languages: go, python, node, php, r, strest, rust, elixir, dart, json, ansible, matlab, etc.

## Install curl2
```
pip3 install -U curl2
```

## How to use
### Python
```
curl2 -c "curl https://leesoar.com"
```

* OutPut
```python
import requests

response = requests.get('https://leesoar.com/')

```

### Go
```
curl2 -c "curl https://leesoar.com -l go"
```

* OutPut
```go
package main

import (
        "fmt"
        "io/ioutil"
        "log"
        "net/http"
)

func main() {
        client := &http.Client{}
        req, err := http.NewRequest("GET", "https://leesoar.com", nil)
        if err != nil {
                log.Fatal(err)
        }
        resp, err := client.Do(req)
        if err != nil {
                log.Fatal(err)
        }
        bodyText, err := ioutil.ReadAll(resp.Body)
        if err != nil {
                log.Fatal(err)
        }
        fmt.Printf("%s\n", bodyText)
}

```

### node
```
curl2 -c "curl https://leesoar.com -l node"
```

* OutPut
```node
var request = require('request');

var options = {
    url: 'https://leesoar.com'
};

function callback(error, response, body) {
    if (!error && response.statusCode == 200) {
        console.log(body);
    }
}

request(options, callback);

```


### php
```
curl2 -c "curl https://leesoar.com -l php"
```

* OutPut
```php
<?php
include('vendor/rmccue/requests/library/Requests.php');
Requests::register_autoloader();
$headers = array();
$response = Requests::get('https://leesoar.com', $headers);
```

