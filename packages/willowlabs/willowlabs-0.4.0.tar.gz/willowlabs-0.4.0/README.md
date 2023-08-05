# Willow Labs Python API
Python client library for Willow Labs APIs

## Installation
``` pip install -U willowlabs ```

## Example usage
```
     from willowlabs.company_information.client import CompanyInformationClient
   client = CompanyInformationClient("client_config.yaml")
   company_basic_results = client.get_basic_company_information(organisation_number)
   company_ownership_results = client.get_company_ownership(organisation_number, record_year)
```

## Documentation
[Read the docs](https://willow-labs-python-api.readthedocs.io/en/doc_release/)


## Versions
### 0.4.0 (current) 
Relased 16.04.2020.

Change in import structure.

### 0.3.0  
Relased 15.04.2020.

Bugg fixes.

### 0.2.0 
Relased 04.04.2020.

First beta version: Basic funcunality.

## License
[MIT](https://opensource.org/licenses/MIT)
