# FAQ 常见问题

这里列举了一些常见问题.

## [Import fails on Windows: ``ImportError: DLL load failed: The specified module could not be found.``](https://github.com/opencv/opencv-python?tab=readme-ov-file#frequently-asked-questions)

将 Windows Server 升级至 2022 或者更新版本。对于腾讯云服务器用户，请开启桌面体验。

<hr/>

If the import fails on Windows, make sure you have [Visual C++ redistributable 2015](https://www.microsoft.com/en-us/download/details.aspx?id=48145) installed. If you are using older Windows version than Windows 10 and latest system updates are not installed, [Universal C Runtime](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows) might be also required.

Windows N and KN editions do not include Media Feature Pack which is required by OpenCV. If you are using Windows N or KN edition, please install also [Windows Media Feature Pack](https://support.microsoft.com/en-us/help/3145500/media-feature-pack-list-for-windows-n-editions).

If you have Windows Server 2012+, media DLLs are probably missing too; please install the Feature called "Media Foundation" in the Server Manager. Beware, some posts advise to install "Windows Server Essentials Media Pack", but this one requires the "Windows Server Essentials Experience" role, and this role will deeply affect your Windows Server configuration (by enforcing active directory integration etc.); so just installing the "Media Foundation" should be a safer choice.

If the above does not help, check if you are using Anaconda. Old Anaconda versions have a bug which causes the error, see [this issue](https://github.com/opencv/opencv-python/issues/36) for a manual fix.

If you still encounter the error after you have checked all the previous solutions, download [Dependencies](https://github.com/lucasg/Dependencies) and open the ``cv2.pyd`` (located usually at ``C:\Users\username\AppData\Local\Programs\Python\PythonXX\Lib\site-packages\cv2``) file with it to debug missing DLL issues.

<hr/>


# 以下部分问题仅供参考

为什么NarutoScript不运行

```
INFO | No task pending
INFO | Wait until 2021-10-27 21:10:54 for task `Commission`
```

因为 NarutoScript 已经完成了所有任务，现在无事可干，只能等待委托科研等结束。

```
CRITICAL | No task waiting or pending
CRITICAL | Please enable at least one task
```

正如 log 里描述的，你需要开启至少一项任务才能开始运行。


## 为什么我打开另一个模拟器时NarutoScript会断开连接

因为你有两个不同版本的ADB

不同版本的ADB之间会互相结束对方. 大部分模拟器 (夜神模拟器, 雷电模拟器, 逍遥模拟器, MuMu模拟器) 都会使用自己的ADB, 而不会使用配置在环境变量中的ADB. 所以当它们启动时, 就会结束NarutoScript正在使用的 adb.exe. 解决这个问题:

- 将模拟器中的ADB替换为NarutoScript使用的ADB.

  如果你使用傻瓜式安装包安装的NarutoScript, 找到位于 `<你的NarutoScript安装目录>\toolkit\Lib\site-packages\adbutils\binaries` 下的ADB. 如果你使用的高级方法安装的NarutoScript, 找到位于环境变量中的ADB, 把它替换为你自己的.

  以夜神模拟器为例, 夜神模拟器安装目录下有两个ADB,  `adb.exe` 和 `nox_adb.exe` 备份它们并删除. 复制两份 `adb.exe` 到夜神模拟器安装目录, 重命名为 `adb.exe` 和 `nox_adb.exe`.