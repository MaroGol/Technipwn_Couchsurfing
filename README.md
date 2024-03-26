Helpful resources:

- Proxying HTTP requests: https://portswigger.net/burp/communitydownload
- Downloading APK files: apkpure.com
- JADX-GUI for decompiling APKs: https://github.com/skylot/jadx
- Android emulator: https://developer.android.com/studio
- Frida course: https://www.youtube.com/watch?v=CLpW1tZCblo

Tips:
To get the emulator to run with Burp suite: https://blog.ropnop.com/configuring-burp-suite-with-android-nougat
And this useful command after you set up the emulator:

```
Path\To\Emulator\AppData\Local\Android\Sdk\emulator\emulator.exe -avd <device name> -writable-system -http-proxy 127.0.0.1:8080
```