server.py第14行连的是我自己电脑的数据库，如果需要可以我来开服务器，你们直接运行client.py。或者改一下这句话，但是需要自己再建立数据库和表，server.py后边的sql语句也需要自己改。

client.py运行起来后，本地默认在盘，在437行self.local_pwd = os.getenv('HOME') if os.name == 'posix' else 'D:\\'  可根据需要自行更改
