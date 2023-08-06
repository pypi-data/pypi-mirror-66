# jedi_toolz
> Collection of utilities to work with pandas, Excel, and other data applications and tools.


This file will become your README and also the index of your documentation.

## Install

`pip install jedi_toolz`

## How to use

Create an example.ini file. The ini file can be stored anywhere and contain login credentials, odbc arguments, default folders, etc.

set_path can be used to set the location of the .ini file at runtime OR the JEDI_TOOLZ_PATH environment variable can be set to persit the changes across usages.

```python
example = set_path(example_ini())
print("#", f"{example.name}")
print(example.open().read())
```

    # example.ini
    [test1]
    value1 = 5
    value2 = 6
    
    [test2]
    valuea = ABC
    valueb = 123
    


```python
as_dict()
```




    {'test1': {'value1': '5', 'value2': '6'},
     'test2': {'valuea': 'ABC', 'valueb': '123'}}



```python
as_records()
```




    [{'section': 'test1', 'option': 'value1', 'value': '5'},
     {'section': 'test1', 'option': 'value2', 'value': '6'},
     {'section': 'test2', 'option': 'valuea', 'value': 'ABC'},
     {'section': 'test2', 'option': 'valueb', 'value': '123'}]



```python
select("test1")
```




    {'value1': '5', 'value2': '6'}



```python
select("test1", "value2")
```




    '6'


