from cx_Freeze import setup, Executable


include_files = ["laudo_sars_cov"]

build_exe_options = {"packages": ["os", "tkinter", "json", "requests", "smtplib", "email", "fpdf", "sys",
                    "threading", "datetime"], "include_files": include_files}

base = "Win32GUI"

setup(  name = "koboMail",
        version = "1.0",
        description = "Application to send emails based on kobo data.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base, shortcutName="koboMail",
            shortcutDir="DesktopFolder")])