# 如何安装

## Python部分

requirements

```
# NLP关键词提取相关
nltk
PyPDF2
python-docx
transformers
rustup
maturin
pytorch

# 文件预览相关
PyMuPDF
python-docx
Spire.Doc
```

## QT部分

1. 运行以下指令安装环境：
   
   ```
   dnf install qt5
   dnf install qt5-devel
   ```

2. 运行以下指令克隆项目到本地：
   
   ```
   git clone -b master https://github.com/EwinLit/ManyThing.git
   ```

3. 进入克隆的目录，运行以下指令
   
   ```
   cd ManyThing
   rm -rf ~/.filesearch
   mkdir ~/.filesearch
   cp  ./assets/files.db ~/.filesearch
   cp -r ./filesearch-qt5 ~/.filesearch
   cp -r ./database_work ~/.filesearch
   cp -r ./extract_keywords ~/.filesearch
   cd ~/.filesearch/filesearch-qt5
   qmake-qt5
   make clean
   make
   rm -rf ~/refreshKeyWord.sh
   rm -rf ~/filesearch.sh
   echo "py ~/.filesearch/extract_keywords/refresh.py" > ~/refreshKeyWord.sh
   echo ~/.filesearch/filesearch-qt5/filesearch > ~/filesearch.sh
   chmod 777 ~/filesearch.sh
   ```

# 如何运行

1. 更新数据库keyword表
   
   ```
   ~/refreshKeyWord.sh
   ```

2. 运行生成在主目录下的filesearch.sh
   
   ```
   ~/filesearch.sh
   ```

3. 点击file->refreshDataBase，更新file表
