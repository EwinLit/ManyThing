#ifndef MYTIME_H
#define MYTIME_H
#include <QString>
#include <QDateTime>
class MyTime{
private:
    int year,month,day;
    int hour,minute,second;
public:
    MyTime();
    MyTime(QDateTime _time);
    MyTime(QString _time);
    MyTime(int year,int month,int day,int _hour,int _minute,int _second);
    MyTime& operator=(const MyTime& obl);
    bool operator>(const MyTime& obj);
    bool operator<=(const MyTime& obj);
    int getyear();
    int getmonth();
    int getday();
    int getHour();
    int getMinute();
    int getSecond();
    QString toString();
};
#endif // MYTIME_H
