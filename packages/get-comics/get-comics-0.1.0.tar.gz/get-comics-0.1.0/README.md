# get.comics.anywhere

`get-comics-anywhere` is a CLI app which can be run on any UNIX system with the required dependencies.  
With the app, you can download chapters from any comics available on the [comicextra.com](https://www.comicextra.com/) website.  
Below is a quick demo with a set of useful commands:
- `get-comics -h` will give you the list of available commands
- `get-comics "Comic Title"` will prompt you to enter a chapter, and download it as a .zip file
- `get-comics -a` will list all available titles
- `get-comics -l W` will list all available titles starting with the letter `W`  


<p style="text-align:center;"><img src="gif-get-comics.gif" style="border-radius:15px;" /></p> 

## How to download

### Download from source code

Feel free to clone this repository.  
From the root of the repository, run:  
```
sudo sh install.sh
```  
You will be able to run the CLI app from anywhere in the terminal, with `get-comics`.  

To uninstall the app:  
```
pip3 uninstall get-comics
```  

You can download the app as follow:  
`pip install get-comics-anywhere`  

## Requirements

You will need the following dependencies:  
- `node-js`
- `selenium`

# Documentation

## Structure of the repository


