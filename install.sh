mkdir ~/.filesearch
# cp -R extract_keywords ~/.filesearch
# cp -R database_work ~/.filesearch
cd filesearch-qt5/
qmake-qt5
make clean
make
cp -R . ~/.filesearch
ln -s ~/.filesearch/filesearch ~/Desktop/filesearch
chmod u+x ~/Desktop/filesearch

