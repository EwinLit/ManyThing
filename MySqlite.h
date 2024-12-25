#ifndef SQLITE_H
#define SQLITE_H
#include <QSqlDatabase>
#include <QMessageBox>
#include <QSqlQuery>
#include <QVariant>
#include "MyFile.h"
class MySqlite{
private:
    QSqlDatabase db;
    QList<MyFile> queryFile(QString path,QString name);
public:
    MySqlite();
    bool connectDataBase(QString dataBaseName);
    QList<MyFile> queryKeyWord(QString keyWord);
    void test();
};

#endif // SQLITE_H
