setlocal EnableDelayedExpansion

ECHO "### Start TESTING"
ECHO "### [JAVA] Infos about JDK locations"
ECHO "JAVA_HOME = %JAVA_HOME%"
ECHO "JDK_HOME = %JDK_HOME%"
ECHO "ARCH = %ARCH%"
ECHO "OSX_ARCH = %OSX_ARCH%"
ECHO "RECIPE_DIR = %RECIPE_DIR%"

ECHO "### [JAVA] Try run java"
java -version
if errorlevel 1 exit 1

ECHO "### [JAVA] Try run %JAVA_HOME%"
%JAVA_HOME%/bin/java.exe -version
if errorlevel 1 exit 1

ECHO "### [EXE] RUN ILP SOLVER TEST"
%PYTHON% "%RECIPE_DIR%\test_script.py"
if errorlevel 1 exit 1

echo Success!
exit 0