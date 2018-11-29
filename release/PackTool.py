__author__ = 'shixuekai'


import sys, os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtQuick import QQuickView

from ConfigManager import  ConfigManager
from DownloadUnziper import DownloadUnziper
from LOG import LOG
from ReleaseUpdater import ReleaseUpdater
from VersionManager import VersionManager
from IniProducer import IniProducer
from TemplateParser import TemplateParser
from InstallPackager import InstallPackager
from UpdateRater import UpdateRater
from UpdateManager import UpdateManager




def main():
    try:
        app = QGuiApplication(sys.argv)

        app.setApplicationName("斗鱼客户端发版")
        app.setWindowIcon(QIcon("./image/app_icon.ico"))
        app.processEvents()
        view = QQuickView()

        context = view.rootContext()

        ############ object define #########
        ###LOG
        log = LOG()
        context.setContextProperty("_log", log)

        current = os.getcwd()
        ###ConfigManager
        config_manager = ConfigManager(current+"\\config\\config.json", view)
        context.setContextProperty("_config_manager", config_manager)

        ###TemplateParser
        template_parser = TemplateParser(current+"\\config\\template.json", view)
        context.setContextProperty("_template_parser", template_parser)

        ###VersionManager
        version_manager = VersionManager(current+"\\config\\version.json", view)
        context.setContextProperty("_version_manager", version_manager)

        ###UpdateManager
        update_manager = UpdateManager(current+"\\config\\update.json", view)
        context.setContextProperty("_update_manager", update_manager)

        ###DownloadUnziper
        downloader = DownloadUnziper(view)
        context.setContextProperty("_downloader", downloader)

        ###IniProducer
        ini_producer = IniProducer(view)
        context.setContextProperty("_ini_producer", ini_producer)

         ###ReleaseUpdater
        release_updater = ReleaseUpdater(view)
        context.setContextProperty("_release_updater", release_updater)

        ###InstallPackager
        install_packager = InstallPackager(view)
        context.setContextProperty("_install_packager", install_packager)

        #UpdateRater
        update_rater = UpdateRater(view)
        context.setContextProperty("_update_rater", update_rater)

        ############ signals connect slots #########
        config_manager.print.connect(log.print)
        config_manager.finalPathChanged.connect(release_updater.onFinalPath)

        template_parser.print.connect(log.print)
        template_parser.updateChanged.connect(ini_producer.onUpdateChanged)
        template_parser.versionAbstractCountChanged.connect(version_manager.onVersionAbstractCount)
        template_parser.versionAbstractChanged.connect(ini_producer.onEnableVersionAbstract)
        template_parser.updateInfoChanged.connect(ini_producer.onUpdateInfoPrefix)
        template_parser.deletedSuffixCascadeChanged.connect(release_updater.onDeletedSuffixAscade)
        template_parser.deletedSuffixChanged.connect(release_updater.onDeletedSuffix)
        template_parser.deletedFileCascadeChanged.connect(release_updater.onDeletedFileAscade)
        template_parser.deletedFileChanged.connect(release_updater.onDeletedFile)
        template_parser.deletedFolderChanged.connect(release_updater.onDeletedFolder)
        template_parser.deletedWorkplaceSuffixChanged.connect(release_updater.onDeletedWorkplaceSuffix)
        template_parser.deletedWorkplaceFileChanged.connect(release_updater.onDeletedWorkplaceFile)
        template_parser.srcPathChanged.connect(release_updater.onSrcPath)
        template_parser.destPathChanged.connect(release_updater.onDestPath)
        template_parser.neededFilesChanged.connect(release_updater.onNeededFiles)
        template_parser.filePackageChanged.connect(release_updater.onFilePackage)
        template_parser.resetPrgConfigChanged.connect(release_updater.onResetPrgConfig)
        template_parser.peSignedChanged.connect(release_updater.onPeSignedChanged)


        template_parser.deletedSuffixCascadeChanged.connect(install_packager.onDeletedSuffixAscade)
        template_parser.deletedSuffixChanged.connect(install_packager.onDeletedSuffix)
        template_parser.deletedFileCascadeChanged.connect(install_packager.onDeletedFileAscade)
        template_parser.deletedPackageFileChanged.connect(install_packager.onDeletedFile)
        template_parser.deletedFolderChanged.connect(install_packager.onDeletedFolder)
        template_parser.peSignedChanged.connect(install_packager.onPeSignedChanged)

        downloader.print.connect(log.print)

        release_updater.print.connect(log.print, type = Qt.QueuedConnection)
        release_updater.versionChanged.connect(config_manager.onLastVersionChanged)
        release_updater.minHideVersionChanged.connect(config_manager.onMinHideVersionChanged)
        release_updater.addItem.connect(update_manager.onAddItem)

        version_manager.print.connect(log.print)
        version_manager.lastNVersionAbstract.connect(ini_producer.onLastNVersionAbstract)

        ini_producer.print.connect(log.print)
        ini_producer.addItem.connect(version_manager.addItem)


        install_packager.print.connect(log.print)


        update_manager.print.connect(log.print)
        update_manager.dataChanged.connect(update_rater.onUpdateVersionData)

        update_rater.print.connect(log.print)




        context.setContextProperty("_main_window", view)

        view.setSource(QUrl('./qml/main.qml'))
        app.aboutToQuit.connect(app.quit)
        root = view.rootObject()
        root.finalPathChanged.connect(config_manager.onFinalPath)
        root.finalPathChanged.connect(release_updater.onFinalPath)

        view.show()


        ret = template_parser.Parse()

        #解析config.json
        ret = config_manager.Parse()

        #解析version.json
        ret = version_manager.Parse()

        #解析update.json
        ret = update_manager.Parse()

        #update_rater.OpenExcel("D:\\learn\\release\\PC客户端启动版本更新率数据.xlsx")


        app.exec_()
    except Exception as e:
        print("main except: "+str(e))




if __name__ == '__main__':
    main()

else:
    print('bushimain')