PyYAML-Tags
===
Adds to PyYAML custom tags support


Branch   | CI status
---------|-------------------
master   | [![Build Status](https://travis-ci.org/meiblorn/pyyaml-tags.svg?branch=master)](https://travis-ci.org/meiblorn/pyyaml-tags)
develop  | [![Build Status](https://travis-ci.org/meiblorn/pyyaml-tags.svg?branch=develop)](https://travis-ci.org/meiblorn/pyyaml-tags)

## Getting Started

**PyYAML-Tags** is a library for advanced YAML processing in Python. It's built on the mature and full-featured [**PyYAML**](https://pyyaml.org) library. 

It comes with 6 predefined tags and allows you to write your own. Use only those tags that you need or connect all at once with a great and simple decorators and meta API.

### Installing

`pip install pyyaml-tags`

### Usage

The most sweet part of the `readme.md` file :)

Library offers 6 predefined tags: `include`, `env`, `random_int`, `randmom_float`, `random_str`, `time_now`.

#### API

By default all the PyYAML tags are in the **`disabled`** state. 
It means that they will not work after you install the library. 

To use tags you need to require them first. 
Just run the following code anywhere in your program:
```python
from yaml_tags import tag_registry

tag_registry.require() # enable all tags 
# or
tag_registry.require(tags='__all__') # same as above
# or
tag_registry.require('include,env,random_int') # enable 'include', 'env' and 'random_int' tags
# or
tag_registry.require(tags=['include', 'env']) # enable 'include', 'env' tags
# or
tag_registry.require('include', 'env', 'time_now') # enable 'include', 'env' and 'time_now' tags

```

then call yaml.load() in your program (_anywhere_):
```python
import yaml

with open('data/a/b/c.yml') as fh:
    data = yaml.load(fh)

print(data)
```
and check — it works !

#### Tags

-   ##### `include` tag
    
    `include` tag allows you to include one yaml files into another.
    
    ###### Sample:
    ```yaml
    humans:
      managers: <% include(path="path/to/managers.yaml") %>
      accountants: <% include(path="path/to/**/accountant*.yaml", recursive=True, encoding='ascii') %>
    aliens: <% include(aliens.txt)
    robots: 
      - <% include(main-robot.yaml) %> 
      - <% include(robots/robot*.yaml) %> 
    ```
    
    ###### Signature
    Parameter | Required | Type | Default | Description
    ----------|----------|------|---------|--------------------------------------------
    path      | yes      | str  |         | Path to file. Supports **glob** syntax
    recursive | no       | bool | False   | If **glob** is used, defines is glob recursive or not
    encoding  | no       | str  | utf-8   | Files encoding

-   ##### `env` tag
    
    `env` tag allows you to pass environment variables values into yaml files
    
    ###### Sample:
    ```yaml
    welcome: Hello, <% env('WORLD_VAR') %> !
    java_home: <% env('JAVA_HOME') %>
    ```
    
    ###### Signature
    Parameter | Required | Type | Default | Description
    ----------|----------|------|---------|--------------------------
    var       | yes      | str  |         | Environment variable name

-   ##### `random_int` tag
    
    `random_int` tag generates random **integer** values and passes them into yaml file
    
    ###### Sample:
    ```yaml
    rolls:
      - roll_1: <% random_int %> # feel free to omit brackets. It's ok
      - roll_2: And this is <% random_int() %> !! Am I lacky ? 
      - roll_3: <% random_int(0, 10) %> 
      - roll_4: <% random_int(-50) %> 
      - final: Final one: <% random_int(-10, 10) %> 
    ```
    
    ###### Signature
    Parameter | Required | Type | Default       | Description
    ----------|----------|------|---------------|-------------
    a         | no       | int  | 0             | Left bound
    b         | no       | int  | `sys.maxsize` | Right bound

-   ##### `random_float` tag
    
    `random_float` tag generates random **float** values (between 0 and 1) and passes them into yaml file
    
    ###### Sample:
    ```yaml
    rolls:
      - roll_1: <% random_float %> # Feel free to omit brackets
      - roll_2: Is it PI? <% random_float() %> ?? Nope ...
    ```

-   ##### `random_str` tag
    
    `random_str` tag generates random **str** values of desired length and passes them into yaml file
    
    ###### Sample:
    ```yaml
    rolls:
      - roll_1: <% random_str %> # Feel free to omit brackets
      - roll_2: <% random_str(10) %>
      - roll_3: My value is <% random_str(5, True) %>
      - roll_5: And mine is <% random_str(20, False, True) %>
      - roll_6: <% random_str(uppercase=True) %>
      - roll_7: Hoho !!! <% random_str(10, lowercase=True) %> Haha !!!
    ```
    
    ###### Signature
    Parameter | Required | Type  | Default   | Description
    ----------|----------|-------|-----------|--------------------------
    length    | no       | int   | 10        | String length
    uppercase | no       | bool  | False     | Convert text to uppercase
    lowercase | no       | bool  | False     | Convert text to lowercase

-   ##### `time_now` tag
    
    `time_now` tag gets current timestamp in a desired format and passes it into yaml file
    
    ###### Sample:
    ```yaml
    context:
      - timestamp: <% time_now %> # Feel free to omit brackets
      - datetime: <% time_now(False) %> 
      - datetime_fmt: <% time_now(timestamp=False, fmt="%Y-%m-%d %H:%M:%S") %> 
    ```
    
    ###### Signature
    Parameter | Required | Type  | Default           | Description
    ----------|----------|-------|-------------------|----------------------------------
    timestamp | no       | bool  | True              | Paste raw timestamp
    fmt       | no       | str   | %Y-%m-%d %H:%M:%S | Format to use when timestamp=False



#### Write your own tags

To write your own tag use one of the following Python templates:

-   Using `tag_registry`
    
    ```python
    from yaml_tags import BaseTag, tag_registry
    
    @tag_registry.register('my_own_tag') # you can set tag name here
    class MyOwnTag(BaseTag):
        # tag_name = 'my_own_tag' # or set it here as alternative
        
        def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   param1=None, param2=None, param3=False, param4='utf-8',
                   *args, **kwargs):
            
            if not param1:
                raise ValueError("Param1 is required")
            
            # your computations here
            result = "smth"
            
            if some_condition(result): # it doesn't matter what condition is this
                return result # w/o prefix and suffix
            
            return _prefix + result + _suffix
    ```

-  Using `TagAutoRegister` meta class. `tag_name` attribute is mandatory here.

    ```python 
    from six import with_metaclass
    from yaml_tags import BaseTag, TagAutoRegister
    
    class MyOwnTag(with_metaclass(TagAutoRegister(), BaseTag)):
        tag_name = 'my_own_tag' # tag name
        
        def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   param1=None, param2=None, param3=False, param4='utf-8',
                   *args, **kwargs):
            
            if not param1:
                raise ValueError("Param1 is required")
            
            # your computations here
            result = "smth"
            
            if some_condition(result): # it doesn't matter what condition is this
                return result # w/o prefix and suffix
            
            return _prefix + result + _suffix
    ```

Then just require your own tag somewhere:
```python
from yaml_tags import tag_registry

tag_registry.require('my_own_tag')
# or
tag_registry.require(tags='__all__') # require all
```

And use it in your yaml files like this:
```yaml
my_own_data: <% my_own_tag(param1="test", param2=2, param3=True, param4='ascii') %>
```

That's all !

## Running the tests

We are using [Tox](https://tox.readthedocs.io/en/latest). It is a generic virtualenv management and test command line tool.

### Unit tests


- To run tests just type `tox` in the command shell. 
- To run tests for a specific Python version use the following commands:
	- For Python 2: `tox -e py2` (or `py27`)
	- For Python 3: `tox -e py3` (or `py34`, `py35`, `py36`, `py37`)


### Coding style tests

To check your codestyle just run `tox -e pep8` in your command shell.

### Coverage

For coverage use `tox -e codecov` command.


## Built With

* [PyYAML](https://pyyaml.org) -  Full-featured YAML framework for the Python programming language.
* [AST](https://docs.python.org/3/library/ast.html) - Helps Python applications to process trees of the Python abstract syntax grammar.
* [Path.py](https://github.com/jaraco/path.py) - Path objects for the Python 2.x

## Contributing

You are welcome to contribute ! Just submit your PR and become a part of PyYAML community!

Please read [contributing.md](contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Vadim Fedorenko** - [Meiblorn](https://github.com/meiblorn) -*Initial work*

See also the list of [authors](authors.md) who participated in this project.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* It's my first Python opensource project. Hah.