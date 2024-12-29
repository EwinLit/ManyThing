#include "mainwindow.h"

void MainWindow::search(QString keyWord){
    setIcon(0);
    myFileList = dataBase.queryKeyWord(keyWord);
    refreshTable(false);
}

void MainWindow::sortName(){
    setIcon(1);
    std::sort(myFileList.begin(),myFileList.end(),[](MyFile a,MyFile b) {return a.getName()<b.getName();});
    refreshTable(false);
}
void MainWindow::sortSize(){
    setIcon(2);
    std::sort(myFileList.begin(),myFileList.end(),[](MyFile a,MyFile b) {return a.getDoubleSize()<b.getDoubleSize();});
    refreshTable(false);
}

void MainWindow::sortType(){
    setIcon(3);
    std::sort(myFileList.begin(),myFileList.end(),[](MyFile a,MyFile b) {return a.getType()<b.getType();});
    refreshTable(false);
}

void MainWindow::sortEditTime(){
    setIcon(4);
    std::sort(myFileList.begin(),myFileList.end(),[](MyFile a,MyFile b) {return a.getMyEditTime()<b.getMyEditTime();});
    refreshTable(false);
}

void MainWindow::sortPath(){
    setIcon(5);
    std::sort(myFileList.begin(),myFileList.end(),[](MyFile a,MyFile b) {return a.getPath()<b.getPath();});
    refreshTable(false);
}

void MainWindow::filtrate(bool enableDate,QString name,QString type,QDate date){
    int i=0;
    while(i<myFileList.size()){
        MyFile myfile = myFileList.at(i);
        if(name!=""&&(myfile.getName().contains(name)==false)) myFileList.removeAt(i);
        else if(type!=""&&myfile.getType().contains(type)==false) myFileList.removeAt(i);
        else if(enableDate==true&&myfile.getDate()!=date) myFileList.removeAt(i);
        else i++;
    }
    refreshTable(false);
}

void MainWindow::handleCell(int row, int colum){
    MyFile myFile = myFileList.at(row);
    QClipboard *clipboard = QApplication::clipboard();
    if(colum ==0) {clipboard->setText(myFile.getName());echoInfo(myFile.toString()+QString("   File Name Copied."));}
    else if(colum ==1) {clipboard->setText(myFile.getPath());echoInfo(myFile.toString()+QString("   File Path Copied."));}
    else if(colum ==2) {clipboard->setText(myFile.getSize());echoInfo(myFile.toString()+QString("   File Size Copied."));}
    else if(colum ==3) {clipboard->setText(myFile.getType());echoInfo(myFile.toString()+QString("   File Type Copied."));}
    else if(colum ==4) {clipboard->setText(myFile.getEditTime());echoInfo(myFile.toString()+QString("   File Edit Time Copied."));}
    else return;
    setTestBrowser(row);
}

void MainWindow::reverse(bool rever){
    if(rever) refreshTable(true);
    else refreshTable(false);
}

void MainWindow::about(){
    QMessageBox::information(nullptr,"About","Group Member:\n尹继营\n童瑜嫣\n贾   辉");
}


void MainWindow::refreshDataBase(){
    dataBase.deleteTable();
    echoInfo("Refreshing Database...");
    bfsDirectory(bfsPath);
    echoInfo("Refresh Database Finished.");
}

void MainWindow::refreshKeyWord(){
    executePython(workPath+"refresh.py");
}

void MainWindow::horizontalSort(int row){
    row++;
    if(row == 1) {
        if(row!=sortStatus&&row!=-sortStatus) {
            sortStatus = row;
            sortName();
        }
        else {
            sortStatus*=-1;
            reverse(sortStatus<0?true:false);
        }
    }
    else if(row == 2) {
        if(row!=sortStatus&&row!=-sortStatus) {
            sortStatus = row;
            sortPath();
        }
        else {
            sortStatus*=-1;
            reverse(sortStatus<0?true:false);
        }
    }
    else if(row == 3) {
        if(row!=sortStatus&&row!=-sortStatus) {
            sortStatus = row;
            sortSize();
        }
        else {
            sortStatus*=-1;
            reverse(sortStatus<0?true:false);
        }
    }
    else if(row == 4) {
        if(row!=sortStatus&&row!=-sortStatus) {
            sortStatus = row;
            sortType();
        }
        else {
            sortStatus*=-1;
            reverse(sortStatus<0?true:false);
        }
    }
    else if(row == 5) {
        if(row!=sortStatus&&row!=-sortStatus) {
            sortStatus = row;
            sortEditTime();
        }
        else {
            sortStatus*=-1;
            reverse(sortStatus<0?true:false);
        }
    }
    else return;
}

void MainWindow::executePython(QString scriptPath){
    QProcess process;
    process.start(pythonPath,QStringList()<<scriptPath);
    if (!process.waitForStarted()) {
        QMessageBox::information(nullptr,"Error","Failed to start Python script.");
        return;
    }
    if (!process.waitForFinished()) {
        QMessageBox::information(nullptr,"Error","Python script execution failed.");
        return;
    }
    QMessageBox::information(nullptr,"Refresh","Refresh Finished");
}

void MainWindow::bfsDirectory(QString path){
    directory.clear();
    directory.append(path);
    while(directory.empty()==false){
        QDir dir(directory.dequeue());
        if (!dir.exists() || !dir.isReadable()) {
            continue;
        }
        QDirIterator it(dir.path(), QDir::Dirs | QDir::Files | QDir::NoDotAndDotDot, QDirIterator::Subdirectories);
        while (it.hasNext()) {
            QString currentPath = it.next();
            QFileInfo fileinfo(currentPath);
            if (fileinfo.isDir()) {
                directory.append(currentPath);
            }
            else{
                dataBase.insertItem(fileinfo.fileName(),fileinfo.absolutePath(),fileinfo.size()*0.001,MyTime(fileinfo.lastModified()).toString(),fileinfo.suffix());
            }
        }
    }
}

void MainWindow::localize(){
    QOperatingSystemVersion osVersion = QOperatingSystemVersion::current();
    if(osVersion.type()==QOperatingSystemVersion::Windows){
        pythonPath = "C://Users//bitap//AppData//Local//Programs//Python//Python39//python.exe";
        workPath = "D://Code//Qt//ManyThing//.filesearch//";
        bfsPath = "D://Code//";
        splitSymbol = "//";
    }
    else{
        pythonPath = "python";
        workPath = QDir::homePath()+"/.filesearch/";
        bfsPath = QDir::homePath();
        splitSymbol = "/";
    }
}




