# rekisteri

`rekisteri` is a private Terraform Registry that serves Terraform's [Provider Registry Protocol](https://www.terraform.io/docs/internals/provider-registry-protocol.html).

For now, only a local filesystem backend is provided, which means only information from the metadata in those files is available, and there's only 3 endpoints - which comply with Terraform's protocol.

Check the `providers` folder for examples of structure and hierarchy of the files with metadata.

## Requirements

- Python 3.8.3
- Flask 1.1.2

## Running

```
$ FLASK_ENV=development FLASK_APP=main.py flask run
```

## Backends

- Filesystem (yes, really!)

## Examples

To start service discovery, we use Terraform's [mechanisms](https://www.terraform.io/docs/internals/remote-service-discovery.html):

```
$ http http://localhost:5000/.well-known/terraform.json
HTTP/1.0 200 OK
Content-Length: 39
Content-Type: application/json
Date: Thu, 31 Dec 2020 09:33:08 GMT
Server: Werkzeug/1.0.1 Python/3.8.3

{
    "providers.v1": "/v1/providers/"
}
```

To list existing versions for a Provider:

```
http http://localhost:5000/v1/providers/hashicorp/random/versions
HTTP/1.0 200 OK
Content-Length: 225
Content-Type: application/json
Date: Thu, 31 Dec 2020 09:38:27 GMT
Server: Werkzeug/1.0.1 Python/3.8.3

{
    "versions": [
        {
            "platforms": [
                {
                    "arch": "amd64",
                    "os": "linux"
                }
            ],
            "protocols": [
                "4.0",
                "5.1"
            ],
            "version": "2.0.0"
        }
    ]
}
```

To get information for a specific Provider:

```
http http://localhost:5000/v1/providers/hashicorp/random/2.0.0/download/linux/amd64
HTTP/1.0 200 OK
Content-Length: 2643
Content-Type: application/json
Date: Thu, 31 Dec 2020 09:39:13 GMT
Server: Werkzeug/1.0.1 Python/3.8.3

{
    "arch": "amd64",
    "download_url": "https://releases.hashicorp.com/terraform-provider-random/2.0.0/terraform-provider-random_2.0.0_linux_amd64.zip",
    "filename": "terraform-provider-random_2.0.0_linux_amd64.zip",
    "os": "linux",
    "protocols": [
        "4.0",
        "5.1"
    ],
    "shasum": "5f9c7aa76b7c34d722fc9123208e26b22d60440cb47150dd04733b9b94f4541a",
    "shasums_signature_url": "https://releases.hashicorp.com/terraform-provider-random/2.0.0/terraform-provider-random_2.0.0_SHA256SUMS.sig",
    "shasums_url": "https://releases.hashicorp.com/terraform-provider-random/2.0.0/terraform-provider-random_2.0.0_SHA256SUMS",
    "signing_keys": {
        "gpg_public_keys": [
            {
                "ascii_armor": "-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v1\n\nmQENBFMORM0BCADBRyKO1MhCirazOSVwcfTr1xUxjPvfxD3hjUwHtjsOy/bT6p9f\nW2mRPfwnq2JB5As+paL3UGDsSRDnK9KAxQb0NNF4+eVhr/EJ18s3wwXXDMjpIifq\nfIm2WyH3G+aRLTLPIpscUNKDyxFOUbsmgXAmJ46Re1fn8uKxKRHbfa39aeuEYWFA\n3drdL1WoUngvED7f+RnKBK2G6ZEpO+LDovQk19xGjiMTtPJrjMjZJ3QXqPvx5wca\nKSZLr4lMTuoTI/ZXyZy5bD4tShiZz6KcyX27cD70q2iRcEZ0poLKHyEIDAi3TM5k\nSwbbWBFd5RNPOR0qzrb/0p9ksKK48IIfH2FvABEBAAG0K0hhc2hpQ29ycCBTZWN1\ncml0eSA8c2VjdXJpdHlAaGFzaGljb3JwLmNvbT6JATgEEwECACIFAlMORM0CGwMG\nCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEFGFLYc0j/xMyWIIAIPhcVqiQ59n\nJc07gjUX0SWBJAxEG1lKxfzS4Xp+57h2xxTpdotGQ1fZwsihaIqow337YHQI3q0i\nSqV534Ms+j/tU7X8sq11xFJIeEVG8PASRCwmryUwghFKPlHETQ8jJ+Y8+1asRydi\npsP3B/5Mjhqv/uOK+Vy3zAyIpyDOMtIpOVfjSpCplVRdtSTFWBu9Em7j5I2HMn1w\nsJZnJgXKpybpibGiiTtmnFLOwibmprSu04rsnP4ncdC2XRD4wIjoyA+4PKgX3sCO\nklEzKryWYBmLkJOMDdo52LttP3279s7XrkLEE7ia0fXa2c12EQ0f0DQ1tGUvyVEW\nWmJVccm5bq25AQ0EUw5EzQEIANaPUY04/g7AmYkOMjaCZ6iTp9hB5Rsj/4ee/ln9\nwArzRO9+3eejLWh53FoN1rO+su7tiXJA5YAzVy6tuolrqjM8DBztPxdLBbEi4V+j\n2tK0dATdBQBHEh3OJApO2UBtcjaZBT31zrG9K55D+CrcgIVEHAKY8Cb4kLBkb5wM\nskn+DrASKU0BNIV1qRsxfiUdQHZfSqtp004nrql1lbFMLFEuiY8FZrkkQ9qduixo\nmTT6f34/oiY+Jam3zCK7RDN/OjuWheIPGj/Qbx9JuNiwgX6yRj7OE1tjUx6d8g9y\n0H1fmLJbb3WZZbuuGFnK6qrE3bGeY8+AWaJAZ37wpWh1p0cAEQEAAYkBHwQYAQIA\nCQUCUw5EzQIbDAAKCRBRhS2HNI/8TJntCAClU7TOO/X053eKF1jqNW4A1qpxctVc\nz8eTcY8Om5O4f6a/rfxfNFKn9Qyja/OG1xWNobETy7MiMXYjaa8uUx5iFy6kMVaP\n0BXJ59NLZjMARGw6lVTYDTIvzqqqwLxgliSDfSnqUhubGwvykANPO+93BBx89MRG\nunNoYGXtPlhNFrAsB1VR8+EyKLv2HQtGCPSFBhrjuzH3gxGibNDDdFQLxxuJWepJ\nEK1UbTS4ms0NgZ2Uknqn1WRU1Ki7rE4sTy68iZtWpKQXZEJa0IGnuI2sSINGcXCJ\noEIgXTMyCILo34Fa/C6VCm2WBgz9zZO8/rHIiQm1J5zqz0DrDwKBUM9C\n=LYpS\n-----END PGP PUBLIC KEY BLOCK-----",
                "key_id": "51852D87348FFC4C",
                "source": "HashiCorp",
                "source_url": "https://www.hashicorp.com/security.html",
                "trust_signature": ""
            }
        ]
    }
}
```
