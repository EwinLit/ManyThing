#ifndef SQLITE_H
#define SQLITE_H
#include <QSqlDatabase>
#include <QMessageBox>
#include <QSqlQuery>
#include <QVariant>
#include <QFile>
#include <QDebug>
#include "MyFile.h"
class MySqlite{
private:
    QSqlDatabase db;
    QList<MyFile> queryFile(QString path,QString name);
public:
    MySqlite();
    QSqlQuery viewKeyWord();
    void connectDataBase(QString dataBaseName);
    void disconnectDataBase();
    QList<MyFile> queryKeyWord(QString keyWord);
    void deleteTable();
    void insertItem(QString name,QString path,double size,QString time,QString type);
};

#endif // SQLITE_H
