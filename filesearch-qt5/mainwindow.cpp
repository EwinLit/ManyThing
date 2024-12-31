#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{

    localize();

    sortStatus = 0;
    ui->setupUi(this);

    this->setWindowTitle("File Searcher");
    this->setWindowIcon(QIcon(":/icon.png"));
    ui->dateEdit->setDate(QDate::currentDate());

    ui->tableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);

    search("");

    connect(ui->actionRefreshDataBase,&QAction::triggered,this,[&](){refreshDataBase();});
//    connect(ui->actionRefreshKeyWord,&QAction::triggered,this,[&](){refreshKeyWord();});

    connect(ui->actionQuit,&QAction::triggered,this,[&](){MainWindow::close();});
    connect(ui->actionName,&QAction::triggered,this,[&](){sortName();});
    connect(ui->actionPath,&QAction::triggered,this,[&](){sortPath();});
    connect(ui->actionSizz,&QAction::triggered,this,[&](){sortSize();});
    connect(ui->actionEdit_Time,&QAction::triggered,this,[&](){sortEditTime();});
    connect(ui->actionType,&QAction::triggered,this,[&](){sortType();});
    connect(ui->actionReverse,&QAction::triggered,this,[&](){reverse(true);});
    connect(ui->actionAbout,&QAction::triggered,this,[&](){about();});

    connect(ui->pushButton,&QPushButton::clicked,this,[&](){search(ui->lineEdit->text());});
    connect(ui->pushButton_2,&QPushButton::clicked,this,[&](){filtrate(ui->checkBox->isChecked(),ui->lineEdit_2->text(),ui->lineEdit_3->text(),ui->dateEdit->date());});

    connect(ui->tableWidget->horizontalHeader(),&QHeaderView::sectionClicked,this,[&](int row){horizontalSort(row);});
    connect(ui->tableWidget,&QTableWidget::cellClicked,this,[&](int row,int colum){handleCell(row,colum);});
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::refreshTable(bool rever){
    if(rever == true) setIcon(6);
    ui->tableWidget->clear();
    ui->tableWidget->setColumnCount(5);
    ui->tableWidget->setHorizontalHeaderLabels(QStringList()<<"Name"<<"Path"<<"Size"<<"Type"<<"Edit Time");
    ui->tableWidget->setColumnWidth(0,150);
    ui->tableWidget->setColumnWidth(1,400);
    ui->tableWidget->setColumnWidth(2,120);
    ui->tableWidget->setColumnWidth(3,100);
    ui->tableWidget->setColumnWidth(4,200);
    ui->tableWidget->verticalHeader()->setVisible(false);
    ui->tableWidget->setSelectionMode(QAbstractItemView::NoSelection);
    int size = myFileList.size();
    ui->tableWidget->setRowCount(size);
    for(int i=0;i<size;i++){
        MyFile myFile = myFileList.at(i);
        int row = rever?size-1-i:i;
        ui->tableWidget->setItem(row,0,new QTableWidgetItem(myFile.getName()));
        ui->tableWidget->setItem(row,1,new QTableWidgetItem(myFile.getPath()));
        ui->tableWidget->setItem(row,2,new QTableWidgetItem(myFile.getSize()));
        ui->tableWidget->setItem(row,3,new QTableWidgetItem(myFile.getType()));
        ui->tableWidget->setItem(row,4,new QTableWidgetItem(myFile.getEditTime()));
    }
    echoInfo(QString::number(myFileList.size())+QString("  Objects."));

}

void MainWindow::echoInfo(QString info){
    ui->statusBar->showMessage(info);
}


void MainWindow::setIcon(int choice){
    QIcon icon(":/red.png");
    QIcon voidIcon;
    if(choice == 6){
        ui->actionReverse->setIcon(icon);
        return;
    }
    ui->actionName->setIcon(voidIcon);
    ui->actionSizz->setIcon(voidIcon);
    ui->actionEdit_Time->setIcon(voidIcon);
    ui->actionType->setIcon(voidIcon);
    ui->actionPath->setIcon(voidIcon);
    ui->actionReverse->setIcon(voidIcon);
    if(choice == 0) return;
    else if(choice == 1) ui->actionName->setIcon(icon);
    else if(choice == 2) ui->actionSizz->setIcon(icon);
    else if(choice == 3) ui->actionType->setIcon(icon);
    else if(choice == 4) ui->actionEdit_Time->setIcon(icon);
    else if(choice == 5) ui->actionPath->setIcon(icon);
    else return;
}

void MainWindow::setTestBrowser(int row){
    ui->textBrowser->clear();
    MyFile myfile = myFileList.at(row);
    QString path(myfile.getPath()+splitSymbol+myfile.getName());
    QFile file(path);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text)) return;
    QTextStream in(&file);
    in.setCodec("UTF-8");
    int count = 50;
    QStringList lines;
    while(!in.atEnd()){
        if(--count<=0) break;
        lines.append(in.readLine());
    }
    file.close();
    count = lines.size();
    for(int i=0;i<count;i++){
        ui->textBrowser->append(lines.at(i));
    }

}









