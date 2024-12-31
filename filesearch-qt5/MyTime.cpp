#include "MyTime.h"

MyTime::MyTime(QDateTime _time){
    this->year = _time.date().year();
    this->month = _time.date().month();
    this->day = _time.date().day();
    this->hour = _time.time().hour();
    this->minute = _time.time().minute();
    this->second = _time.time().second();
}

MyTime::MyTime(QString _time){
    //2001/01/01-01:01:01
    this->year = _time.mid(0,4).toInt();
    this->month = _time.mid(5,2).toInt();
    this->day = _time.mid(8,2).toInt();
    this->hour = _time.mid(11,2).toInt();
    this->minute = _time.mid(14,2).toInt();
    this->second = _time.mid(17,2).toInt();
}

MyTime::MyTime(int _year,int _month,int _day,int _hour,int _minute,int _second){
   this->year = _year;
   this->month = _month;
   this->day = _day;
   this->hour = _hour;
   this->minute = _minute;
   this->second = _second;
}

MyTime::MyTime(){
    this->year = 0;
    this->month = 0;
    this->day = 0;
    this->hour = 0;
    this->minute = 0;
    this->second = 0;
}

bool MyTime::operator>(const MyTime& obj){
    if(this->year>obj.year) return true;
    if(this->month>obj.month) return true;
    if(this->day>obj.day) return true;
    if(this->hour>obj.hour) return true;
    if(this->minute>obj.minute) return true;
    if(this->second>obj.second) return true;
    return false;
}

bool MyTime::operator<=(const MyTime& obj){
    if(this->year>obj.year) return false;
    if(this->month>obj.month) return false;
    if(this->day>obj.day) return false;
    if(this->hour>obj.hour) return false;
    if(this->minute>obj.minute) return false;
    if(this->second>obj.second) return false;
    return true;
}

MyTime& MyTime::operator=(const MyTime& obj){
    this->year = obj.year;
    this->month = obj.month;
    this->day = obj.day;
    this->hour = obj.hour;
    this->minute = obj.minute;
    this->second = obj.second;
    return *this;
}

int MyTime::getyear(){
    return this->year;
}

int MyTime::getmonth(){
    return this->month;
}

int MyTime::getday(){
    return this->day;
}

int MyTime::getHour(){
    return this->hour;
}

int MyTime::getMinute(){
    return this->minute;
}
int MyTime::getSecond(){
    return this->second;
}

QString MyTime::toString(){
    QString monthString = month<10?"0"+QString::number(this->month):QString::number(this->month);
    QString dayString = day<10?"0"+QString::number(this->day):QString::number(this->day);
    QString hourString = hour<10?"0"+QString::number(this->hour):QString::number(this->hour);
    QString minuteString = minute<10?"0"+QString::number(this->minute):QString::number(this->minute);
    QString secondString = second<10?"0"+QString::number(this->second):QString::number(this->second);
    return QString::number(year)+QString("/")+monthString+QString("/")+dayString+QString("-")
            +hourString+QString(":")+minuteString+QString(":")+secondString;
}



