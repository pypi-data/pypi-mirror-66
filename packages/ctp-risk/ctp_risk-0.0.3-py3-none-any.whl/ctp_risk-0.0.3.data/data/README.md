# ctp_risk_api

#### 项目介绍
风控接口封装

#### 软件架构
软件架构说明


#### 安装教程

* 官方文档 FtdcRiskUserApiStruct 需增加 #include <string> 否则报错

#### 使用说明

* 修改g_c.py中的 src_dir = '../riskapi_32' 编译32or64位dll

* 生成
  * linux
    ```bash
    g++ -shared -fPIC -o ./riskapi.so ./trade.cpp ./libriskuserapi.so
    ```

#### 32位与64位C++文件区别
* 32位需声明 WINAPI __cdecl