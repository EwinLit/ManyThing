rm -rf ~/.filesearch
mkdir ~/.filesearch
cp -r ./filesearch-qt5 ~/.filesearch/
cp -r ./database_work ~/.filesearch
cp -r ./extract_keywords ~/.filesearch
cd ~/.filesearch/filesearch-qt5
qmake filesearch.pro
make clean
make
echo ~/.filesearch/filesearch-qt5/filesearch > ~/filesearch.sh
chmod 777 ~/filesearch.sh
