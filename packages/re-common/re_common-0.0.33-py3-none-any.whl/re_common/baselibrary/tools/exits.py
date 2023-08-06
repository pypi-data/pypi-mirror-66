# 解压然后复制到另一个文件夹
from re_common.baselibrary.utils.basedir import BaseDir
from re_common.baselibrary.utils.basefile import BaseFile

for filepath in BaseDir.get_dir_all_files(r'F:\db32\gz'):
    print(filepath)
    outfilepath = self.pages_big_json_mid + "\\" + BaseFile.get_file_name(filepath)
    BaseFile.rename_file(filepath, outfilepath)
    jieya = outfilepath.replace(".gz","")
    g = BaseGzip(bufsize=2 * 1024 * 1024 * 1024)
    g.decompress(outfilepath, jieya)
    BaseFile.remove_file(outfilepath)
    print("解压完毕{}".format(jieya))

# 解析判断存在，写入新的big_json
# for filepath in BaseDir.get_dir_all_files(self.pages_big_json_mid):
#     for line in BaseFile.read_file_rb_mode_yield(filepath):
#
#         json_data = json.loads(line)
#         cid = json_data['cid']
#         pagenum = json_data['pagenum']
#         a_tup = (cid,pagenum)
#         if a_tup not in self.info_list:
#             self.info_list.append(a_tup)
#             self.do_path = BaseFile.change_file(self.do_path, size=2 * 1024 * 1024 * 1024)
#             BaseFile.add_file_ab_mode(line,self.do_path)
#             print("写入{}".format(self.do_path))
#         else:
#             print("{}{}存在".format(cid,pagenum))