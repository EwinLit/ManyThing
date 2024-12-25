#include "MySqlite.h"

MySqlite::MySqlite(){

}

bool MySqlite::connectDataBase(QString dataBaseName){

    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(dataBaseName);
    db.setConnectOptions("QSQLITE_OPEN_READONLY");
    if (!db.open()) {
      QMessageBox::information(nullptr,"DataBase","Failed To Open DataBase");
      return false;
    }
    return true;
}

QList<MyFile> MySqlite::queryKeyWord(QString keyWord){
    QList<MyFile> myFiles;
    if(keyWord == ""){
        myFiles = queryFile("","");
    }
    QSqlQuery query;
    QString cmd = QString("SELECT * FROM %1 WHERE word = \"%2\"").arg("keyword").arg(keyWord);
    if(query.exec(cmd) == false) return myFiles;
    while(query.next()){
        myFiles.append(queryFile(query.value(1).toString(),query.value(2).toString()));
    }
    return myFiles;
}

QList<MyFile> MySqlite::queryFile(QString _path,QString _name){
    QList<MyFile> myFiles;
    QSqlQuery query;
    QString cmd = QString("SELECT * FROM %1").arg("file");
    if(_path!=""||_name!=""){
        cmd = cmd + QString(" WHERE name = \"%1\" AND path = \"%2\"").arg(_name).arg(_path);
    }
    if(query.exec(cmd) == false) return myFiles;
    while(query.next()){
        QString name = query.value(1).toString();
        QString path = query.value(0).toString();
        double size = query.value(2).toDouble();
        QString type = query.value(3).toString();
        MyTime editTiem = MyTime(query.value(4).toString());
        MyFile myfile(path,name,size,editTiem,type);
        myFiles.append(myfile);
    }
    return myFiles;
}

void MySqlite::test(){
    return;
    QSqlQuery query;
    for(int i=0;i<45000;i++){
        QString cmd = QString("INSERT INTO file (name, path, size, type, time) VALUES (%1,%2,%3,%4,%5)")
                .arg(QString("\"test")+QString::number(i+5000)+QString("\"")).arg("\"1\"").arg(10.01).arg("\"exe\"").arg("\"2001/01/01-01:01:01\"");
        query.exec(cmd);
    }
}

