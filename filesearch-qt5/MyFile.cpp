#include <MyFile.h>


MyFile::MyFile(QString _name,QString _path,double _size,MyTime _editTime,QString _type){
    this->name = _name;
    this->path = _path;
    this->size = _size;
    this->editTime = _editTime;
    this->type = _type;
}

QString MyFile::getName(){
    return this->name;
}

QString MyFile::getPath(){
    return this->path;
}
QString MyFile::getSize(){
    return QString::number(this->size,'f',2)+QString("KB");
}
double MyFile::getDoubleSize(){
    return this->size;
}

QDateTime MyFile::getMyEditTime(){
    return QDateTime(this->getDate(),QTime(this->editTime.getHour(),this->editTime.getMinute(),this->editTime.getSecond()));
}

QString MyFile::getEditTime(){
    return this->editTime.toString();
}
QString MyFile::getType(){
    return this->type;
}
QDate MyFile::getDate(){
    return QDate(this->editTime.getyear(),this->editTime.getmonth(),this->editTime.getday());
}
QString MyFile::toString(){
    return QString("Type: ")+getType()+QString(";  Size: ")+getSize()+QString(";  Edit Time: ")+getEditTime()+QString(";  Path: ")+getPath()+QString(".");
}

