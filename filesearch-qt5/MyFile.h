#ifndef MYFILE_H
#define MYFILE_H
#include "MyTime.h"
#include <QDate>
#include <QDateTime>
class MyFile{
private:
    QString name;
    QString path;
    double size;
    MyTime editTime;
    QString type;
public:
    MyFile(QString _name,QString _path,double _size,MyTime _editTime,QString _type);
    QString getName();
    QString getPath();
    QString getSize();
    double getDoubleSize();
    QDateTime getMyEditTime();
    QString getEditTime();
    QString getType();
    QDate getDate();
    QString toString();
};
#endif // MYFILE_H
