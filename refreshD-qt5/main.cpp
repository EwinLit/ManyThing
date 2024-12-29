#include <QCoreApplication>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QVariant>
#include <QDir>
#include <QDirIterator>
#include <QFileInfo>
#include <QQueue>
#include <QDateTime>
#include <QOperatingSystemVersion>
#include <QDebug>

QQueue<QString> directory;
QSqlDatabase db;
QString workPath;

QString parse(QDateTime);
void insertItem(QString,QString,double,QString,QString);
void bfsDirectory(QString);


int main()
{

    QOperatingSystemVersion osVersion = QOperatingSystemVersion::current();
        if(osVersion.type()==QOperatingSystemVersion::Windows){
            workPath = "D://Code//Qt//ManyThing//.filesearch//";
        }
        else{
            workPath = QDir::homePath()+"/.filesearch/";
        }
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(workPath+"files.db");
    db.open();
    bfsDirectory(workPath);
    db.close();
    return 0;
}

QString parse(QDateTime dt){
    int year = dt.date().year();
    int month = dt.date().month();
    int day = dt.date().day();
    int hour = dt.time().hour();
    int minute = dt.time().minute();
    int second = dt.time().second();
    QString monthString = month<10?"0"+QString::number(month):QString::number(month);
        QString dayString = day<10?"0"+QString::number(day):QString::number(day);
        QString hourString = hour<10?"0"+QString::number(hour):QString::number(hour);
        QString minuteString = minute<10?"0"+QString::number(minute):QString::number(minute);
        QString secondString = second<10?"0"+QString::number(second):QString::number(second);
        return QString::number(year)+QString("/")+monthString+QString("/")+dayString+QString("-")
                +hourString+QString(":")+minuteString+QString(":")+secondString;
}

void insertItem(QString name, QString path, double size, QString time, QString type){
    QSqlQuery query;
    QString cmd = QString("INSERT INTO file (name, path, size, type, time) VALUES (\"%1\",\"%2\",%3,\"%4\",\"%5\")")
            .arg(name).arg(path).arg(size).arg(type).arg(time);
    query.exec(cmd);
}

void bfsDirectory(QString path){

    directory.clear();
    directory.append(path);
    while(directory.empty()==false){
        QDir dir(directory.front());
        directory.pop_front();
        if (!dir.exists() || !dir.isReadable()) {
            continue;
        }
        QDirIterator it(path, QDir::Dirs | QDir::Files | QDir::NoDotAndDotDot, QDirIterator::Subdirectories);
        while (it.hasNext()) {
            QString currentPath = it.next();
            QFileInfo fileinfo(currentPath);
            if (QFileInfo(currentPath).isDir()) {
                directory.append(currentPath);
            }
            else{
                insertItem(fileinfo.fileName(),fileinfo.absolutePath(),fileinfo.size()*0.001,parse(fileinfo.lastModified()),fileinfo.suffix());
            }
        }
    }
}
