This is a script that is meant to change all female hebrew word to male.

It includes basic flask interface.

The script uses Hspell and HspellPy with linginfo.

# Install
Get Hspell and HspellPy (see https://github.com/nirroz93/HspellPy): 
  1. Download Hspell: http://hspell.ivrix.org.il/
  2. Configure: ./configure --enable-shared --enable-linginfo
  3. Build: make
  4. Install: make install
  5. Download HspellPy with lingonfo https://github.com/nirroz93/HspellPy
  6. python setup.py install

any error about libhspell.so can be handled by defining LD_LIBRARY_PATH to include libhspell.so.0 directory (as metioned in HspellPy page)
# Usage
After running the script the flask interface will run listeing to port 5000.
A text can be passed to te script using http://localhost:5000/antiFemine?text="Hebrew text"
You can also pass a url by http://localhost:5000/antiFemine?url="Web page url"
