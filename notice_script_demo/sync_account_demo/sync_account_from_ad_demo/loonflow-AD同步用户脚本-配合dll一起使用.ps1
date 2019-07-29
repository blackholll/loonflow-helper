#使用教程
#找到MySql.Data.dll的路径（这个文件）

$dll_path = "C:\powershell\dll\mysql\v4.5\MySql.Data.dll"  #dll路径
$mysql_ip = "10.10.3.51"   #实例loonflow的服务器IP
$mysql_port = "3306"       #端口 ，默认是3306
$mysql_account = "root"    #账号默认是root
$mysql_paassword = "Liu@2019"   #密码
$mysql_database_name = "loonflow"   #实例名称，默认是loonflow
$ou_path = "dc=test,dc=com"    #需要同步的OU路径

#-----------------------------------------------------新建导入用户函数-开始---------------------------------------------------------------------------------------
function mysql-insert-loonflow-user($f_username,$f_alias,$f_email,$f_phone,$f_password,$dept_id,$is_active,$is_admin,$creator,$is_deleted,$gmt_created,$gmt_modified)
    {
        [void][system.Reflection.Assembly]::LoadFrom($dll_path)
        #加载mysql组件
        $connectionString = "server=$mysql_ip;uid=$mysql_account;pwd=$mysql_paassword;database=$mysql_database_name;charset='utf8';port=$mysql_port"   #定义连接信息
        $connection = New-Object MySql.Data.MySqlClient.MySqlConnection($connectionString)   #新建对象
        $connection.Open()                                                                   #打开数据库
        $insertsql = "SELECT * from account_loonuser where username='$f_username'"           #查询sql，条件为等于用户名
        Write-Host $insertsql                                                                #打印sql语句方便排错
        $command = New-Object MySql.Data.MySqlClient.MySqlCommand($insertsql, $connectionString)    
        $dataAdapter = New-Object MySql.Data.MySqlClient.MySqlDataAdapter($command)         
        $dataSet = New-Object System.Data.DataSet                                                                              
        $recordCount = $dataAdapter.Fill($dataSet, "data")                                  #获取到查询后的结果，并存到1个变量 
        if ([int]($dataSet.Tables["data"].username).Length -ge '1')     #当查询条目大于等于1时，判定用户已存在
            {
            return $f_username+"    已存在"  #输出判定结果（已存在）在屏幕
            }
        else                                 #否则就执行新建命令
            {
            #加载mysql组件
            $insertsql= "INSERT INTO account_loonuser(username,alias,email,phone,password,dept_id,is_active,is_admin,creator,is_deleted,gmt_created,gmt_modified) VALUES('$f_username','$f_alias','$f_email','$f_phone','$f_password','$dept_id','$is_active','$is_admin','$creator','$is_deleted','$gmt_created','$gmt_modified');" 
            #将变量插入到对应mysql字段
            $insertcommand = New-Object MySql.Data.MySqlClient.MySqlCommand 
            $insertcommand.Connection=$connection 
            $insertcommand.CommandText=$insertsql 
            $insertcommand.ExecuteNonQuery()   #提交mysql语句变更
            $connection.Close()    
            return $f_username+"  新建信息成功"   #返回新建成功的消息
            }
     $connection.Close()   #关闭sql
    }
#-----------------------------------------------------新建导入用户函数-结束---------------------------------------------------------------------------------------

$aduser_all = Get-ADUser -SearchBase $ou_path -Filter * -Properties *   #获取指定OU里面的所有用户
foreach ($aduser in $aduser_all)                                        #循环每1个用户
    {
    $dept_id = [int](($aduser.objectSid).Value -split "-")[-1]   #获取1个唯一ID
    $date = (get-date).ToString('yyyy-MM-dd HH;MM;ss')           #定义当前时间，并格式化

    mysql-insert-loonflow-user -f_username $aduser.SamAccountName -f_alias $aduser.DisplayName -f_email $aduser.UserPrincipalName -f_phone 18888888888 -f_password loonflow@2019 -dept_id $dept_id -is_active 1 -is_admin 0 -creator "任务计划" -is_deleted 0 -gmt_created $date -gmt_modified $date
    #执行函数，导入用户到loonflow，密码是随便写的，反正不能登陆
    }