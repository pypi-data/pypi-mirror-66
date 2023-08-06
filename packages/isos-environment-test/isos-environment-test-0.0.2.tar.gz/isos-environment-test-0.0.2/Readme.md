# Isos Technology Python Atlassian Cloud Automation Environment Test

## Requirements
- Python >= 3.7.7
- atlassian-python-api >= 1.15.6
- requests >= 2.22.0
- console-menu >= 0.6.0

## To install / test environment
1. Ensure you have python 3 version 3.7.7 or greater installed.
2. Generate an Atlassian API Token following these [directions](https://confluence.atlassian.com/cloud/api-tokens-938839638.html).
3. Run the following commands in Terminal or Powershell and follow the prompts:

   ```
   # You might have to run as Administrator or sudo depending on your setup.
   
   python3 setup.py install --user
   python3 -m isos-env-test
   ```

## To install / test with virtualenv
1. Ensure you have python 3 version 3.7.7 or greater installed
2. Generate an Atlassian API Token following these [directions](https://confluence.atlassian.com/cloud/api-tokens-938839638.html)
3. Install virtualenv:  
`pip3 install virtualenv`
4. Create and source a virtualenv:  
   ```
   virtualenv env
   source env/bin/activate
   ```
5. Run the following commands in Terminal or Powershell and follow the prompts:  
   ```
   python setup.py install
   python -m isos-env-test
   ```