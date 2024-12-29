# 如何安装
## Python部分
requirements
```
# NLP关键词提取相关
pip install nltk
pip install PyPDF2
pip install python-docx
pip installtransformers

# 安装maturin及其依赖的Rust工具链
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install maturin

# 从源码构建pytorch
wget https://github.com/pytorch/pytorch/releases/download/v2.4.0/pytorch-v2.4.0.tar.gz
tar xvf pytorch-v2.4.0.tar.gz
cd pytorch-v2.4.0/
bash build.sh

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
3. 进入克隆的目录，运行项目中的install.sh
```
cd ManyThing
chmod u+x install.sh
./install.sh
```
4. 运行生成在主目录下的start.sh
```
~/start.sh
```
