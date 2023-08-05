# Willow Labs Python API
Python client library for Willow Labs APIs

## Installation
``` Pip install -U willowlabs ```

## Example usage
```
   import willowlabs as wl
   client = wl.CompanyInformationClient("client_config.yaml")
   company_basic_results = client.get_basic_company_information(organisation_number)
   company_ownership_results = client.get_company_ownership(organisation_number, record_year)
```

## Documentation
[Read the docs](https://willow-labs-python-api.readthedocs.io/en/doc_release/)


## Versions

### 0.2.0 
Relased 04.04.2020.

First beta version: Basic funcunality.

## License
[MIT](https://opensource.org/licenses/MIT)
