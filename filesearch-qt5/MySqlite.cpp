#include "MySqlite.h"

MySqlite::MySqlite(){

}

bool MySqlite::connectDataBase(QString dataBaseName){

    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(dataBaseName);
    if (!db.open()) {
      QMessageBox::information(nullptr,"DataBase","Failed To Open DataBase");
      return false;
    }
    QSqlQuery query;
    QString cmd = QString("CREATE TABLE \"file\" ("
                                             "\"name\"	TEXT,"
                                             "\"path\"	TEXT,"
                                             "\"size\"	REAL,"
                                             "\"type\"	TEXT,"
                                             "\"time\"	TEXT,"
                                             "PRIMARY KEY(\"name\",\"path\")"
                                         ")");
    query.exec(cmd);
    cmd = QString("CREATE TABLE \"keyword\" ("
                                        "\"word\"	TEXT,"
                                        "\"path\"	TEXT,"
                                        "\"name\"	TEXT,"
                                        "\"id\"	INTEGER,"
                                        "PRIMARY KEY(\"id\")"
                                    ")");
    query.exec(cmd);
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
        QString name = query.value("name").toString();
        QString path = query.value("path").toString();
        double size = query.value("size").toDouble();
        QString type = query.value("type").toString();
        MyTime editTime = MyTime(query.value("time").toString());
        myFiles.append(MyFile(name,path,size,editTime,type));
    }
    return myFiles;
}

void MySqlite::insertItem(QString name, QString path, double size, QString time, QString type){
    QSqlQuery query;
    QString cmd = QString("INSERT INTO file (name, path, size, type, time) VALUES (\"%1\",\"%2\",%3,\"%4\",\"%5\")")
            .arg(name).arg(path).arg(size).arg(type).arg(time);
    query.exec(cmd);
}


void MySqlite::deleteTable(){
    QSqlQuery query;
    QString cmd = QString("DELETE FROM %1 WHERE 1").arg("file");
    query.exec(cmd);
}

