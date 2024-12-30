#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QList>
#include <QStringList>
#include <QDebug>
#include <QClipboard>
#include <QApplication>
#include <QMessageBox>
#include <QProcess>
#include <QDir>
#include <QDirIterator>
#include <QTextStream>
#include <QHeaderView>
#include <QFile>
#include <QQueue>
#include <QOperatingSystemVersion>
#include "MySqlite.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    bool success;
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    QList<MyFile> myFileList;
    MySqlite dataBase;
    int sortStatus;
    QString pythonPath;
    QString workPath;
    QString bfsPath;
    QString splitSymbol;
    QQueue<QString> directory;

    //mainwindow.cpp
    void refreshTable(bool reverse);
    void echoInfo(QString info);
    void setIcon(int choice);
    void setTestBrowser(int row);

    //support.cpp
    void localize();
    void sortName();
    void sortSize();
    void sortPath();
    void sortEditTime();
    void sortType();
    void filtrate(bool enableDate,QString name,QString type,QDate date);
    void search(QString keyWord);
    void handleCell(int row,int colum);
    void about();
    void reverse(bool rever);
    void refreshDataBase();
    void refreshKeyWord();
    void horizontalSort(int row);
    void executePython(QString scriptPath);
    void bfsDirectory(QString path);
};

#endif // MAINWINDOW_H
