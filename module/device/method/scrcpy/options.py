import typing as t


class ScrcpyOptions:
    frame_rate = 10

    @classmethod
    def command_v27(cls, jar_path='/data/local/tmp/scrcpy-server.jar') -> t.List[str]:
        """
        Generate the commands to run scrcpy server 2.x (key=value options).

        Server >= 2.5 is required for Android 14 QPR3 / Android 15+,
        which removed SurfaceControl.createDisplay.
        Protocol reference: py-scrcpy-client v0.5.0 (tested on Android 15).
        """
        commands = [
            f'CLASSPATH={jar_path}',
            'app_process',
            '/',
            'com.genymobile.scrcpy.Server',
            '2.7',  # Scrcpy server version
            'log_level=info',
            'max_size=1280',
            # 20Mbps, the maximum output bitrate of scrcpy
            f'video_bit_rate={20000000}',
            f'max_fps={cls.frame_rate}',
            # Always true
            'tunnel_forward=true',
            # Send raw h264 stream, without frame meta
            'send_frame_meta=false',
            # Always true for controlling via scrcpy
            'control=true',
            # 2.x enables audio by default, which client cannot parse
            'audio=false',
            'show_touches=false',
            'stay_awake=false',
            'power_off_on_close=false',
            'clipboard_autosync=false',
        ]
        return commands


if __name__ == '__main__':
    print(' '.join(ScrcpyOptions.command_v27()))
