import QtQuick 2.7
import QtQuick.Controls 2.3

Dialog {
    id: ceDialog
    title: "配置文件各个字段说明"
    width: 600
    height: 400
    padding: 0
    margins: 0

    ScrollView {
        id: ceScrollView
        width: ceDialog.width
        height: ceDialog.height - 48
        clip: true


        ScrollBar.horizontal.policy: ScrollBar.AsNeeded
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        TextArea {
            id: ceTextArea
            renderType: Text.NativeRendering
            font.family: font_yahei
            font.pixelSize: 14
            selectByMouse: true

            background: Rectangle{
                color: "#eeeeee"
            }
            text: '
url: zdb下载路径的根目录，一般为https://sta-op.douyucdn.cn/dyadmin-ext/client-download/pc/
appCode: 区分其他PC应用的编码, 例如直播客户端是Douyu_Live_PC_Client
lastVersion: 需要下载的zdb的版本号，由9位数字组成，例如201809290
zdbFile: zdb文件名，一般为ProgramConfig.zdb.zip
zdbButton: 是否显示下载zdb按钮
srcPath: 过度文件夹名，例如dy_pcclient
destPath: 生成的版本文件所在的文件夹， 例如public
finalPath: 版本文件所在的文件夹，可以是绝对路径，也可以是相对路径
deletedSuffixCascade: 要删除的文件后缀集合，级联到子文件夹，例如.map, .pdb
deletedSuffix: 要删除的文件后缀集合，例如.map, .pdb
deletedFileCascade: 要删除的文件后缀集合
deletedFile: 要删除的文件后缀集合，例如version.ini, logging.conf, logging_p2p.conf
deletedWorkplaceSuffix: 在工作区，要删除的文件后缀集合，例如.log, .zd
deletedWorkplaceFile: 在工作区，要删除的文件集合，例如.map, .pdb
neededFiles: 打包需要的文件集合，例如FilePackage.exe, ResetPrgConfig.exe, sqlite3.dll, zlib1.dll
filePackage: filePackage文件名，一般为FilePackage.exe
resetPrgConfig: ResetPrgConfig文件名，一般为ResetPrgConfig.exe
'
        }

    }
}
