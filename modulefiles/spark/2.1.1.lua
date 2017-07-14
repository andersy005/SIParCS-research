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
local basepath = "/glade/p/work/abanihi/spark-2.1.1-bin-hadoop2.7"   -- base path
-- look for a package for specific compiler version
-- if not found use default version

local libpath  = pathJoin(basepath,"lib")               -- libraries
local binpath  = pathJoin(basepath,"bin")

local localspark = "~/cheyenne/spark/spark-cluster-scripts"
--
setenv("SPARK_HOME",basepath)
setenv("SPARK_CONF_DIR", "~/cheyenne/spark/conf")
setenv("SPARK_HOSTFILE", "~/cheyenne/spark/conf")

-- update the user environment and paths
prepend_path("PYTHONPATH", pathJoin(basepath, "python"))
prepend_path("PYTHONPATH", pathJoin(basepath, "python/lib/py4j-0.10.4-src.zip"))
prepend_path("PATH",binpath)
prepend_path("LD_LIBRARY_PATH",libpath)
prepend_path("PATH", localspark)