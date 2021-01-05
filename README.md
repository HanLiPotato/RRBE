client.py里第四行sys.path.append(r'C:/Users/10712/Desktop/RRBE/RRBE_CS')改为自己文件里边的RRBE_CS的路径

第438行self.local_pwd = os.getenv('HOME') if os.name == 'posix' else 'C:\\Users\\10712\\Desktop'改为自己电脑上的本地路径
