require("posix")

-- The message printed by the module whatis command
whatis("spark v2.1.1")

-- The message printed by the module help command
help([[
This module loads Apache Spark. It should work on all nodes.
]])

-- Get user variable
local user = os.getenv("USER")

-- Ge Python path
local pythonpath = os.getenv("PYTHONPATH")

-- get base path for the fakepack package
local basepath = "/glade/p/work/abanihi/cy/installs/spark/2.2.0"   -- base path
local homedir = pathJoin(basepath, "spark-2.2.0-bin-hadoop2.7")    -- home path

local libpath  = pathJoin(homedir,"python/lib")               -- libraries
local binpath  = pathJoin(homedir,"bin")
local sparkscripts = pathJoin(basepath, "scripts")
--
setenv("SPARK_HOME", homedir)
setenv("SPARK_BASE_DIR", basepath)
-- update the user environment and paths
prepend_path("PYTHONPATH", pathJoin(homedir, "python"))
prepend_path("PYTHONPATH", pathJoin(homedir, "python/lib/py4j-0.10.4-src.zip"))
prepend_path("PATH",binpath)
prepend_path("LD_LIBRARY_PATH",libpath)
prepend_path("PATH", sparkscripts)