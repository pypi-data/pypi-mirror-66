# Name for JSON
A filter to get the json file content from filename in a command line terminal. Type less with a file name along with ```tansa```, while the tansa takes care of frustrating search. 

## Quick Start
### Installation
The simplest installation method.

	pip install tansa

### Sample
While sample.json is in your current/nested directory,

	$ tansa sample

which will display json contents.

	[{'sample.json':{key:value}, 'sample2.json':{key:value}}]

## Development
The tansa takes one argument as a file name to look for. Customers are free from entering the exact file name such as suffix because the tansa append ```*``` to the input as its suffix.


### Test
In progress

### Contact
If it turns out that you may have found a bug, please open [an issue](https://github.com/k0a8t1o6/tansa/issues/new/choose).
