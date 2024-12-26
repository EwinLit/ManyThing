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
#include <QTextStream>
#include <QHeaderView>
#include <QFile>
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

    //mainwindow.cpp
    void refreshTable(bool reverse);
    void echoInfo(QString info);
    void setIcon(int choice);
    void setTestBrowser(int row);

    //support.cpp
    void sortName();
    void sortSize();
    void sortPath();
    void sortEditTime();
    void sortType();
    void filtrate(QString name,QString type,QDate date);
    void search(QString keyWord);
    void openFile(int row,int colum);
    void handleCell(int row,int colum);
    void about();
    void help();
    void reverse(bool rever);
    void refreshDataBase();
    void horizontalSort(int row);
    void executePython(QString scriptPath);
    void installTools();
};

#endif // MAINWINDOW_H
