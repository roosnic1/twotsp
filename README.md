#the "twotsp" Project


##Goal
Find the almost two best paths that never use the same edge through a number of points

##Members 
Jérémie Blaser, Martin Eigenmann and Nicolas Roos

##Install
```python
pip install -r requirements.txt
```
###Install wxPython2.9 on a Mac
Download wxPython2.9 for Python2.7 64Bit from http://downloads.sourceforge.net/wxpython/wxPython2.9-osx-2.9.4.0-cocoa-py2.7.dmg

Open the dmg and install the package. Find the wxredirect.pth e.g(/Library/Python/2.7/site-packages/wxredirect.pth). 
Change to your virtualenv site-packages directory
```python
cd /Users/koki/.virtualenvs/twotsp/lib/python2.7/site-packages/
```
Create a link to the wxredirect.pth.
```python
ln -s /Library/Python/2.7/site-packages/wxredirect.pth wxredirect.pth
```

Change to your virtualenv bin directory
```python
cd /Users/koki/.virtualenvs/twotsp/bin/
```
create a file called fwpy with the following content:
```python
#What real Python executable to use
PYVER=2.7
PYTHON=/System/Library/Frameworks/Python.framework/Versions/$PYVER/bin/python$PYVER

# find the root of the virtualenv, it should be the parent of the dir this script is in
ENV=`$PYTHON -c "import os; print os.path.abspath(os.path.join(os.path.dirname(\"$0\"), '..'))"`

# now run Python with the virtualenv set as Python's HOME
export PYTHONHOME=$ENV
exec $PYTHON "$@"
```


##Execute
Normal Execution:
```python
python main.py
```

Gui Execution:
```python
fwpy gui.py
```